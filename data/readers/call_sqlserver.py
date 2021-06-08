from opendp.smartnoise.sql import SqlServerReader, PrivateReader
from opendp.smartnoise.metadata import CollectionMetadata

meta = CollectionMetadata.from_file('PUMS_large.yaml')

query = 'SELECT married, AVG(income) AS income, COUNT(*) AS n FROM PUMS.PUMS_large GROUP BY married'

query = 'SELECT COUNT(*) AS n FROM PUMS.PUMS_large WHERE age > 92 GROUP BY educ'

reader = SqlServerReader('127.0.0.1', 'PUMS', 'sa')

private_reader = PrivateReader(reader, meta, 1.0)

exact = reader.execute_typed(query)
print(exact)

private = private_reader.execute_typed(query)
print(private)
