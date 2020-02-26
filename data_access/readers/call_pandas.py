import pandas as pd
from burdock.sql import PandasReader, PrivateReader, CollectionMetadata

pums = pd.read_csv('PUMS.csv')
meta = CollectionMetadata.from_file('PUMS.yaml')

query = 'SELECT married, COUNT(*) AS n FROM PUMS.PUMS GROUP BY married'

reader = PandasReader(meta, pums)
private_reader = PrivateReader(reader, meta, 1.0)

exact = reader.execute_typed(query)
print(exact)

private = private_reader.execute_typed(query)
print(private)



#datasets = '../../../datasets/'
#pums_1000 = datasets + 'data/PUMS_california_demographics_1000/data.csv'
