import pandas as pd
from opendp.smartnoise.sql import PandasReader, PrivateReader
from opendp.smartnoise.metadata import CollectionMetadata

pums = pd.read_csv('PUMS.csv')
meta = CollectionMetadata.from_file('PUMS.yaml')

query = 'SELECT married, AVG(income) AS income, COUNT(*) AS n FROM PUMS.PUMS GROUP BY married'

query = 'SELECT COUNT(*) AS n, COUNT(pid) AS foo FROM PUMS.PUMS WHERE age > 80 GROUP BY educ'

reader = PandasReader(meta, pums)
private_reader = PrivateReader(meta, reader, 4.0)
private_reader.options.censor_dims = True
private_reader.options.clamp_counts = True

exact = reader.execute_typed(query)
print(exact)

private = private_reader.execute_typed(query)
print(private)
