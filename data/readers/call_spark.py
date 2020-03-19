import pyspark
from pyspark.sql import SparkSession
from opendp.whitenoise.metadata import CollectionMetadata
from opendp.whitenoise.sql import SparkReader, PrivateReader

spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

meta = CollectionMetadata.from_file('PUMS_large.yaml')
lines = sc.textFile('PUMS_california_demographics/data.csv')

# First we use the metadata to create a CSV reader
table = meta.tables()[0]
typenames = [c.typename() for c in table.columns()]
colnames = [c.name for c in table.columns()]

def convert(val, type):
    if type == 'string' or type == 'unknown':
        return str(val).replace('"', '').replace("'", '')
    elif type == 'int':
        return int(float(str(val).replace('"', '').replace("'", '')))
    elif type == 'float':
        return float(str(val).replace('"', '').replace("'", ''))
    elif type == 'boolean':
        return bool(str(val).replace('"', '').replace("'", ''))
    else:
        raise ValueError("Can't convert type " + type)

# Convert all of the strings to the appropriate types
header = lines.first()
rows = lines.filter(lambda line: line != header)
rows = rows.map(lambda l: [convert(val, type) for val, type in zip(l.split(','), typenames) ] )

# turn it into a Spark DataFrame
df = rows.toDF(colnames)
df.createOrReplaceTempView("PUMS_large")

query = 'SELECT AVG(age) FROM PUMS_large'

reader = SparkReader(spark)
# We need to tell the reader that all tables used in the query are avaialble under default schema named 'PUMS'
reader.compare.search_path = ["PUMS"]

exact = reader.execute_typed(query)

print(exact)

private = PrivateReader(reader, meta, 1.0)
priv = private.execute_typed(query)

print(priv)

