# SQL Data Access

You can issue SQL queries against CSV files, database engines, and Spark clusters.

## Simple Example

In this sample, we read from the sample PUMS dataset to calculate average income grouped by marital status.

```python
import pandas as pd
from opendp.whitenoise.sql import PandasReader, PrivateReader
from opendp.whitenoise.metadata import CollectionMetadata

pums = pd.read_csv('PUMS.csv')
meta = CollectionMetadata.from_file('PUMS.yaml')

query = 'SELECT married, AVG(income) AS income, COUNT(*) AS n FROM PUMS.PUMS GROUP BY married'

reader = PandasReader(meta, pums)
private_reader = PrivateReader(meta, reader)

result = private_reader.execute_typed(query)
print(result)
```

There are two important concepts to highlight here.  First, we need to instantiate a `Reader` that can execute SQL queries against some data source.  This could be a `PandasReader` (for CSV files), a `SqlServerReader`, `PostgresReader`, `SparkReader`, or any other reader that returns typed tuples from a SQL store.  These readers know nothing about differential privacy.  They are simply adapters that connect us to a storage engine:

```python
# example of calling a reader for exact query results
# no differential privacy code is used
from opendp.whitenoise.sql import SqlServerReader

query = 'SELECT married, AVG(income) AS income, COUNT(*) AS n FROM PUMS.PUMS_large GROUP BY married'

reader = SqlServerReader('127.0.0.1', 'PUMS', 'sa')

exact = reader.execute_typed(query)
print(exact)
``` 

Next, we need to instantiate a `PrivateReader` that wraps the database adapter we created.  The `PrivateReader` will perform preprocessing and postprocessing to ensure differential privacy.

```python
private_reader = PrivateReader(meta, reader)

noisy = private_reader.execute_typed(query)
print(noisy)
```

The `PrivateReader` has the same calling interface as any other `Reader`, but results will be differentially private.  

## Metadata

In order to ensure differential privacy, the `PrivateReader` needs some metadata that describes the data source.  The metadata describes things like data types and ranges of values, and must not be data-dependent.  It is typically provided by the data curator, and can be loaded from a YAML file.

```python
from opendp.whitenoise.metadata import CollectionMetadata

meta = CollectionMetadata.from_file('PUMS.yaml')
print(meta)
```

The metadata specifies which columns can be used in aggregate functions, which column should be treated as the private identifier, and allows the data curator to mandate specialized behavior such as clamping counts and censoring dimensions.  For a list of metadata options, see the reference.

Although YAML is preferred, you can also construct the metadata directly in code:

```python
from opendp.whitenoise.metadata.collection import *

table1 = Table("dbo", "devices", 5000, \
    [\
        String("DeviceID", 0, True),\
        Boolean("Refurbished"), \
        Float("Temperature", 20.0, 70.0)
    ])

meta = CollectionMetadata([table1],"csv")
```
Object documentation for the literal syntax is [here](https://opendifferentialprivacy.github.io/whitenoise-samples/docs/api/system/metadata/collection.html)

## Privacy Parameters

The `PrivateReader` accepts `epsilon` and `delta` privacy parameters which control the privacy budget for each query:

```python
# epsilon is 0.1, delta is 10E-16

private_reader = PrivateReader(meta, reader, 0.1, 10E-16)
```

The epsilon parameter applies to each column in the result. It is not distributed across columns.  Some computations, such as `AVG`, will perform two noisy computations and will incur double epsilon cost.

## Expressions

You can perform simple expressions involving private aggregates:

```sql
SELECT AVG(Income) / 1000 AS IncomeK FROM PUMS
```

Or

```sql
SELECT AVG(Income) / AVG(Age) FROM PUMS GROUP BY married
```

## Histograms

SQL `group by` queries represent histograms binned by grouping key.  Queries over a grouping key with unbounded or non-public dimensions expose privacy risk. For example:

```sql
SELECT last_name, COUNT(*) FROM Sales GROUP BY last_name
```

In the above query, if someone with a distinctive last name is included in the database, that person's record might accidentally be revealed, even if the noisy count returns 0 or negative.  To prevent this from happening, the system will automatically censor dimensions which would violate differential privacy.

## Joins

Future updates will improve support for joins and subqueries.  Joins and subqueries may work under some conditions, but additional work is needed to ensure differential privacy.

## Synopsis

## Installing Sample Databases

