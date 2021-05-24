# SQL Data Access

You can issue SQL queries against CSV files, database engines, and Spark clusters.

## Simple Example

In this sample, we read from the sample PUMS dataset to calculate average income grouped by marital status.

```python
import pandas as pd
from opendp.smartnoise.sql import PandasReader, PrivateReader
from opendp.smartnoise.metadata import CollectionMetadata

pums = pd.read_csv('PUMS.csv')
meta = CollectionMetadata.from_file('PUMS_row.yaml')

query = 'SELECT married, AVG(income) AS income, COUNT(*) AS n FROM PUMS.PUMS GROUP BY married'

reader = PandasReader(pums, meta)
private_reader = PrivateReader(reader, meta, 1.0)

result = private_reader.execute(query)
print(result)
```

There are two important concepts to highlight here.  First, we need to instantiate a `Reader` that can execute SQL queries against some data source.  This could be a `PandasReader` (for CSV files), a `SqlServerReader`, `PostgresReader`, `SparkReader`, or any other reader that returns typed tuples from a SQL store.  These readers know nothing about differential privacy.  They are simply adapters that connect us to a storage engine:

```python
# example of calling a reader for exact query results
# no differential privacy code is used
from opendp.smartnoise.sql import SqlServerReader

query = 'SELECT married, AVG(income) AS income, COUNT(*) AS n FROM PUMS.PUMS_large GROUP BY married'

reader = SqlServerReader('127.0.0.1', 'PUMS', 'sa')

exact = reader.execute_typed(query)
print(exact)
```

Next, we need to instantiate a `PrivateReader` that wraps the database adapter we created.  The `PrivateReader` will perform preprocessing and postprocessing to ensure differential privacy.

```python
private_reader = PrivateReader(reader, meta, 1.0)

noisy = private_reader.execute(query)
print(noisy)
```

The `PrivateReader` has the same calling interface as any other `Reader`, but results will be differentially private.

## Metadata

In order to ensure differential privacy, the `PrivateReader` needs some metadata that describes the data source.  The metadata describes things like data types and ranges of values, and must not be data-dependent.  It is typically provided by the data curator, and can be loaded from a YAML file.

```python
from opendp.smartnoise.metadata import CollectionMetadata

meta = CollectionMetadata.from_file('PUMS.yaml')
print(meta)
```

The metadata specifies which columns can be used in aggregate functions, which column should be treated as the private identifier, and allows the data curator to mandate specialized behavior such as clamping counts and censoring dimensions.  For a list of metadata options, see the reference.

Although YAML is preferred, you can also construct the metadata directly in code:

```python
from opendp.smartnoise.metadata.collection import *

table1 = Table("dbo", "devices", 5000, \
    [\
        String("DeviceID", 0, True),\
        Boolean("Refurbished"), \
        Float("Temperature", 20.0, 70.0)
    ])

meta = CollectionMetadata([table1],"csv")
```
Object documentation for the literal syntax is [here](https://opendifferentialprivacy.github.io/smartnoise-samples/docs/api/system/metadata/collection.html)

## Privacy Parameters

The `PrivateReader` accepts `epsilon` and `delta` privacy parameters which control the privacy budget for each query:

```python
# epsilon is 0.1, delta is 10E-16

private_reader = PrivateReader(reader, meta, 0.1, 10E-16)
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

## Private Synopsis

A private synopsis is a pre-computed set of differentially private aggregates that can be filtered and aggregated in various ways to produce new reports.  Because the private synopsis is differentially private, reports generated from the synopsis do not need to have additional privacy applied, and the synopsis can be distributed without risk of additional privacy loss.  Reports over the synopsis can be generated with non-private SQL, within an Excel Pivot Table, or through other common reporting tools.

You can see a sample [notebook for creating private synopsis](Synopsis.ipynb) suitable for consumption in Excel or SQL.

## Limitations

You can think of the data access layer as simple middleware that allows composition of analysis graphs using the SQL language.  The SQL language provides a limited subset of what can be expressed through the full analysis graph.  For example, the SQL language does not provide a way to set per-field privacy budget.

Because we delegate the computation of exact aggregates to the underlying database engines, execution through the SQL layer can be considerably faster, particularly with database engines optimized for precomputed aggregates.  However, this design choice means that analysis graphs composed with SQL language do not access data in the engine on a per-row basis.  Therefore, SQL queries do not currently support algorithms that require per-row access, such as algorithms based on the geometric mechanism.  This is a limitation that future releases will relax for database engines that support row-based access, such as Spark.

The SQL processing layer has limited support for bounding contributions when individuals can appear more than once in the data.  This includes ability to perform reservoir sampling to bound contributions of an individual, and to scale the sensitivity parameter.  These parameters are important when querying reporting tables that might be produced from subqueries and joins, but require caution to use safely.

For this release, we recommend using the SQL functionality while bounding user contribution to 1 row.  The platform defaults to this option by setting `max_contrib` to 1, and should only be overridden if you know what you are doing.  Future releases will focus on making these options easier for non-experts to use safely.

## Note on SQLite Version

The PandasReader used SQLite under the covers, whereas the other readers use the respective database engines.  The SQLite version that comes with many Python distributions is quite old, and does not support `SELECT DISTINCT`, which is required to limit the number of rows per user.  If you are using conda, you can ensure that you are using the latest SQLite by typing `conda install --yes -c anaconda sqlite`.  If you know that your data has only one row per uses, you can specify `row_privacy` in the metadata, as in the sample above, and the functionality will work with older SQLite versions. 

## Installing Sample Databases

If you would like to test against Postgres or SQL Server instances running in a Docker container with PUMS data imported,  you can build the containers from [source here](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/testing/databases)

## Architecture

The SQL processing layer intercepts SQL queries destined for any SQL-92 backend, and operates as middleware between the engine and the analysis graph.  The interface is designed to be a drop-in replacement for existing DB-API or ODBC workflows; for example, legacy analytics and reporting applications.  The main stages of processing are:

1. **Parser.** The parser converts the query to an AST, using a subset of the SQL-92 grammar.  The parser also takes metadata about the database tables, such as column sensitivity, to augment the AST.
2. **Validator.**  The validator checks the query to make sure it meets requirements for differential privacy, such as computing the types of aggregates that it knows how to protect.
3. **Rewriter.** The rewriter modifies the query to enforce sensitivity bounds, perform reservoir sampling, and convert simple expressions to a pre-processing and post-processing step (for example, applying scalar operations after adding noise).
4. **Database Execution.** The rewritten query is executed by the target database engine. This is just a pass-through call.  The database engine returns the set of exact aggregates, as would be returned in the absence of differential privacy, and with the application of sensitivity clamping and reservoir sampling.
5. **Postprocessing.**  The exact aggregates are fed to the differential privacy algorithms to create differentially private results.
