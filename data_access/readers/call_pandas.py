import pandas as pd
from burdock.sql import PandasReader, PrivateReader, CollectionMetadata
from burdock.sql.private_reader import PrivateReaderFlags

pums = pd.read_csv('PUMS.csv')
meta = CollectionMetadata.from_file('PUMS.yaml')

query = 'SELECT married, AVG(income) AS income, COUNT(*) AS n FROM PUMS.PUMS GROUP BY married'

query = 'SELECT COUNT(*) AS n, COUNT(pid) AS foo FROM PUMS.PUMS WHERE age > 80 GROUP BY educ'

flags = PrivateReaderFlags()
flags.censor_dims = True
flags.clamp_counts = True

reader = PandasReader(meta, pums)
private_reader = PrivateReader(reader, meta, 4.0, 1/10000, [0.96], flags)

exact = reader.execute_typed(query)
print(exact)

private = private_reader.execute_typed(query)
print(private)



#datasets = '../../../datasets/'
#pums_1000 = datasets + 'data/PUMS_california_demographics_1000/data.csv'
