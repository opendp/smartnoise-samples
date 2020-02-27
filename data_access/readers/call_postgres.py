import pandas as pd
from burdock.reader.sql.postgres import PostgresReader
from burdock.sql import PrivateReader, CollectionMetadata

meta = CollectionMetadata.from_file('PUMS_large.yaml')

query = 'SELECT married, COUNT(*) AS n FROM PUMS.PUMS_large GROUP BY married'

reader = PostgresReader('127.0.0.1', 'PUMS', 'postgres')
private_reader = PrivateReader(reader, meta, 1.0)

private = private_reader.execute_typed(query)
print(private)

exact = reader.execute_typed(query)
print(exact)
