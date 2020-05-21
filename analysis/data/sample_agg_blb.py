import random
import math
from pyspark.sql import Row

class SampleAggregate:
    def __init__(self, df, parts=None):
        self.df = df
        self.parts = parts
        if parts is None:
            rows = df.rdd.countApprox(2000, 1.0)
            if rows <= 100:
                raise ValueError("Not enough rows for sample and aggregate")
            self.parts = math.floor(rows / 100)

    def sample(self):
        def add_part_key(row):
            sys_rand = random.SystemRandom()
            r = sys_rand.uniform(-10.0, 10.0)
            temp = row.asDict()
            temp["partkey_0x011"] = r
            return Row(**temp)
        sampled = self.df.rdd.map(add_part_key).toDF()
        sampled = sampled.repartitionByRange(self.parts, "partkey_0x011")
        self.sampled = sampled

    def aggregate(self):
        pass