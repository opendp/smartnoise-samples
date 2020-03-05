import pandas as pd
from burdock.reader.sql.sqlserver import SqlServerReader
from burdock.sql import PrivateReader, CollectionMetadata
from burdock.sql.private_reader import PrivateReaderFlags

meta = CollectionMetadata.from_file('PUMS_large.yaml')

query = 'SELECT married, AVG(income) AS income, COUNT(*) AS n FROM PUMS.PUMS_large GROUP BY married'

query = 'SELECT COUNT(*) AS n FROM PUMS.PUMS_large WHERE age > 92 GROUP BY educ'

reader = SqlServerReader('127.0.0.1', 'PUMS', 'sa')

flags = PrivateReaderFlags()
flags.censor_dims = False
flags.clamp_counts = True

private_reader = PrivateReader(reader, meta, 0.001, [0.95], flags )

exact = reader.execute_typed(query)
print(exact)

private = private_reader.execute_typed(query)
print(private)

