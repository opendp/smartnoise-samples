import random
import math
from pyspark.sql import Row
import numpy as np

def filter_list(group, plist, weights, keys, cols):
    group_match = []
    if group is not None:
        if not isinstance(group, (list, tuple)):
            group = [group]
        group_match = [(k, v) for k, v in zip(keys, group)]
    vals = []
    for row, weight in zip(plist, weights):
        row_vals = row.asDict()
        if all([(row_vals[k] == v) for k, v in group_match]):
            vals.append(tuple(row_vals[col] for col in cols) + tuple([weight]))
    return (group, vals)


class SampleAggregate:
    def __init__(self, df, n_parts=None):
        self.pkn = "partkey_0x011"
        self.df = df
        self.n_parts = n_parts
        self.rows = df.rdd.countApprox(2000, 1.0)
        if n_parts is None:
            if self.rows <= 100:
                raise ValueError("Not enough rows for sample and aggregate")
            self.n_parts = math.floor(self.rows / 100)

    def sample(self, cols):
        """Partitions dataframe into the desired number of partitions
            to support sample-and-aggregate analysis.
            :param cols: List of column names to extract from the DataFrame
        """
        pkn = self.pkn
        def add_part_key(row):
            sys_rand = random.SystemRandom()
            r = sys_rand.uniform(-10.0, 10.0)
            temp = row.asDict()
            temp[pkn] = r
            return Row(**temp)
        sampled = self.df.rdd.map(add_part_key).toDF()
        sampled = sampled.select(cols + [pkn])
        sampled = sampled.repartitionByRange(self.n_parts, pkn)
        self.sampled = sampled.persist()

    def aggregate(self, cols=None, keys=None, groups=None):
        """Aggregates and bootstraps data in each partition.

            :param cols: list of column names that will be needed
                to compute QOI, e.g. ["age", "income"]
            :param keys: list of key names for grouping keys,
                e.g. ["married", "educ"]
            :param groups: list of tuples for all distinct combinations
                of the requested grouping keys.  Tuple order must
                match the order of the list supplied in param keys,
                e.g. [(True, 12), (False, 13), (True, 7)]
            :returns:
                Returns an iterator with an RDD pair, where the first 
                element of the RDD is a tuple representing the grouping
                key values for this group, and the second is a list of
                tuples representing the rows of the partition that match
                the grouping key.

                The last column will always be the weights for each
                row, bootsrapped up to match the original dataset size.

                Note that the returned list of tuples need not include columns for
                the grouping keys.
        """
        n_rows = self.rows
        def load_part(splitIndex, partition, cols=cols, keys=keys, groups=groups):
            groups = groups if groups is not None else [None]
            plist = list(partition)
            weights = np.random.multinomial(n_rows, [1/len(plist)]*len(plist))

            def filter_group(group, plist=plist, weights=weights):
                group_match = []
                if group is not None:
                    if not isinstance(group, (list, tuple)):
                        group = [group]
                    group_match = [(k, v) for k, v in zip(keys, group)]
                vals = []
                for row, weight in zip(plist, weights):
                    row_vals = row.asDict()
                    if all([(row_vals[k] == v) for k, v in group_match]):
                        vals.append(tuple(row_vals[col] for col in cols) + tuple([weight]))
                return (group, vals)
            return [gv for gv in map(filter_group, groups) if gv[1]]
        self.aggregated = self.sampled.rdd.mapPartitionsWithIndex(load_part).persist()

    def apply(self, funcs):
        # applies a list of functions to the group
        def func_to_row(gv, funcs=funcs):
            group, vals = gv
            if not isinstance(funcs, (list, tuple)):
                funcs = [funcs]
            return Row(group=group, val=tuple(func(vals) for func in funcs))
        self.applied = self.aggregated.map(func_to_row).persist()

    def estimate(self, func, eps, delta, sens):
        # clamp each partition theta, aggregate, and add noise
        n_parts = self.n_parts
        def func_to_row(row, func=func):
            group = row[0]
            cols = list(zip(*list(row[1])))
            return Row(group=group, val=tuple(func(col, eps, delta, s, n_parts) for col, s in zip(cols, sens)))
        return self.applied.groupByKey().map(func_to_row)