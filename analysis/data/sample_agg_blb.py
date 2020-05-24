import random
import math
from pyspark.sql import Row
import numpy as np

class SampleAggregate:
    def __init__(self, df, parts=None):
        self.pkn = "partkey_0x011"
        self.df = df
        self.parts = parts
        self.rows = df.rdd.countApprox(2000, 1.0)
        if parts is None:
            if self.rows <= 100:
                raise ValueError("Not enough rows for sample and aggregate")
            self.parts = math.floor(self.rows / 100)

    def sample(self, cols):
        pkn = self.pkn
        def add_part_key(row):
            sys_rand = random.SystemRandom()
            r = sys_rand.uniform(-10.0, 10.0)
            temp = row.asDict()
            temp[pkn] = r
            return Row(**temp)
        sampled = self.df.rdd.map(add_part_key).toDF()
        sampled = sampled.select(cols + [pkn])
        sampled = sampled.repartitionByRange(self.parts, pkn)
        self.sampled = sampled.persist()

    def aggregate(self, cols=None, keys=None, groups=None):
        n_rows = self.rows
        def load_part(splitIndex, partition, cols=cols, keys=keys, groups=groups):
            """Loads a partition into an in-memory list that
                matches the format expected by whitenoise-core.

                :param cols: list of column names that will be needed
                    by the function, e.g. ["age", "income"]
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
            plist = list(partition)
            weights = np.random.multinomial(n_rows, [1/len(plist)]*len(plist))
            if groups is None:
                groups = [None]
            while len(groups) > 0:
                group_match = []
                group = groups.pop(0)
                if group is not None:
                    if not isinstance(group, (list, tuple)):
                        group = [group]
                    group_match = [(k, v) for k, v in zip(keys, group)]
                vals = []
                #if splitIndex > 10:
                #    continue # return empty for all but 10 partitions
                for row, weight in zip(plist, weights):
                    row_vals = row.asDict()
                    if all([(row_vals[k] == v) for k, v in group_match]):
                        vals.append(tuple(row_vals[col] for col in cols) + tuple([weight]))
                    #if len(vals) > 10000:
                    #    break
                if len(vals) == 0:
                    continue
                else:
                    yield (group, vals)

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
        parts = self.parts
        def func_to_row(row, func=func):
            group = row[0]
            cols = list(zip(*list(row[1])))
            return Row(group=group, val=tuple(func(col, eps, delta, s, parts) for col, s in zip(cols, sens)))
        return self.applied.groupByKey().map(func_to_row)