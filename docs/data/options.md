# Private Query Options

You can set options on the PrivateReader to modify the privacy behavior.

```python
import pandas as pd
from burdock.sql import PandasReader, PrivateReader, CollectionMetadata

df = pd.read_csv('PUMS.csv')
meta = CollectionMetadata.from_file('PUMS.yaml')
reader = PandasReader(meta, df)
private_reader = PrivateReader(reader, meta, 1.0)
private_reader.options.reservoir_sample = False

result = private_reader.execute_typed('SELECT COUNT(*) FROM PUMS.PUMS WHERE age < 40')
print(result)
```

## censor_dimensions

If False, disables censoring of dimensions that might uniquely identify an individual.  For example, if you do a GROUP BY query on last_name, even a negative or very small count for that dimension will reveal existence of that last_name in the database.  Only set this value to False if you know that your dimension keys are bounded.  For example, if you are doing GROUP BY state, and you know that all states have records in the database, it is acceptable to disable censoring.

## reservoir_sample

By default, the system ensures that each individual contributes at most `max_contrib` records to any report.  This is accomplished by uniform random sampling, which adds some overhead to the query.  If you are certain that your database can never query more than `max_contrib` records per individual, you can disable reservoir sampling.

## clamp_counts

By default, the system changes noisy negative counts to 0 before reporting. If your scenario allows negative counts, you can report the negative noisy values unchanged.

## clamp_columns

By default, the system clamps numeric values to ensure they don't fall outside the lower and upper bounds specified in the metadata.  You may disable this clamping to fine-tune the variance/bias trade-off.  There may be privacy implications.