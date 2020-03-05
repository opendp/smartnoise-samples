# Extending the Data Access APIs

PrivateReader operates by intercepting SQL requests to a Reader implementaion,
rewriting the SQL where necessary, then post-processing the results to add
differntially private noise.  It may work automatically with many SQL-92
sources, but you may want to mke custom Reader implementations to handle
custom connection behavior, or engine-specific semantics

## Creating a DataReader

A data reader is just a pipe that sends SQL to some sort of data processing
engine and returs results in the form of a list of tuples.  This is the 
default behavior for ODBC and DBAPI on Python.

```python
from burdock.reader.sql.base import Reader, NameCompare
from my.engine import my_api

class MyEngineReader(Reader):
    def __init__(self, gateway, catalog, credentials):
        self.gateway = gateway
        self.catalog = catalog
        self.credentials = credentials
        self.engine = "MyEngine"
        self.compare = MyEngineNameCompare()
        self.serializer = MyEngineSerializer()
        self.api = my_api.create_context(gateway, catalog, credentials)

    def execute(self, query):
        return self.api.query(query)

class MyNameCompare(NameCompare):
    def identifier_match(self, other):
        return True

class MyEngineSerializer:
    def serialize(self, sql):
        return sql.replace('RANDOM', 'rand')
```

To implement a Reader, you need to ingerit from the base Reader, and be sure to set the `engine` property.

The constructor can have any setup paramaters that your engine needs.  In this example, we are passing in connection string information needed to connect to a gateway, but you could also have your callers set up some sort of session outside the reader and pass it in.

If you don't need specialized handling for case-sensitive or escaped identifiers, you can omit the specilization of NameCompare, and the base Reader will automatically give you a base NameCompare that is case-sensitivie.

If your engine uses a dialect of SQL that we don't support, you can provide a serializer to automatically fix the dialect befre sending to the engine.

Your main code goes in the `execute` method.  The execute method takes a query as a string, and returns a list of tuples, with the firt tuple being column names, and each following tuple representing a row of values.  The base reader provides other methods that allow compiled ASTs to be executed, and to return TypedRowset objects.

## Using the Reader

To use the reader you created, plug it in just like any other Reader:

```python
from burdock.sql import PrivateReader, CollectionMetadata
from my.engine.reader import MyEngineReader

meta = CollectionMetadata.from_file('Sales.yaml')
reader = MyEngineReader(gateway, 'Sales', credentials)
private = PrivateReader(reader=reader, epsilon=1.0)

query = 'SELECT SUM(Sales) AS Sales GROUP BY Region FROM Sales.RegionalSales'
result = private.execute_typed(query)

print(result)
```
