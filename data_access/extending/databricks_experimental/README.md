# Databricks Experimental

Sample of using on Databricks
```python
from pyspark.sql import SparkSession
burdocksc = SparkSession.builder.appName('smoketest').getOrCreate()
meta_path = "/dbfs/mnt/prod-c1/SmokeTest/PUMS.yaml"
query_string = "SELECT COUNT(*) AS c, married AS m FROM PUMS.PUMS GROUP BY married ORDER BY c, m DESC"

spr = SparkDataFrameReader(burdocksc, meta_path)
noised_df = spr.execute(query_string)
display(noised_df)
