import pandas as pd
from opendp.smartnoise.sql import PostgresReader, PrivateReader
from opendp.smartnoise.metadata import CollectionMetadata

meta = CollectionMetadata.from_file('PUMS_large.yaml')

query = 'SELECT married, AVG(income) AS income, COUNT(*) AS n FROM PUMS.PUMS_large GROUP BY married'
query = 'SELECT AVG(age) FROM PUMS.PUMS_large'

reader = PostgresReader('127.0.0.1', 'PUMS', 'postgres')
private_reader = PrivateReader(reader, meta, 1.0)

exact = reader.execute_typed(query)
print(exact)

private = private_reader.execute_typed(query)
print(private)
