import pandas as pd
from burdock.reader.sql.sqlserver import SqlServerReader
from burdock.sql import PrivateReader
from burdock.metadata.collection import CollectionMetadata

meta = CollectionMetadata.from_file('PUMS_large.yaml')

query = 'SELECT married, COUNT(*) AS n FROM PUMS.PUMS_large GROUP BY married'

reader = SqlServerReader('127.0.0.1', 'PUMS', 'sa')
private_reader = PrivateReader(reader, meta, 1.0)

private = private_reader.execute_typed(query)
print(private)

exact = reader.execute_typed(query)
print(exact)
