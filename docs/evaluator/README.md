# Using the Stochastic Evaluator

## Installing

To install the evaluator library, use pip:

```sh
pip install burdock
```

You can download sample code and notebooks by cloning this repository:

```sh
git clone https://github.com/privacytoolsproject/burdock-samples.git
cd burdock-samples/evaluator
```

## Evaluating Privacy

To evaluate the privacy of an algorithm, configure the privacy paramaters and pass the algorithm in to the evaluator.

### Evaluating an aggregate

```python
import burdock.evaluation.dp_verification as dp
import burdock.evaluation.aggregation as agg

dv = dp.DPVerification(dataset_size=10000)
ag = agg.Aggregation(t=1, repeat_count=10000)

dp_count, ks_count, ws_count = dv.aggtest(ag.dp_count, 'UserId', binsize="auto", debug = False)
dp_sum, ks_sum, ws_sum = dv.aggtest(ag.dp_sum, 'Usage', binsize="auto")
dp_mean, ks_mean, ws_mean = dv.aggtest(ag.dp_mean, 'Usage', binsize="auto", debug=False, plot=True)
dp_var, ks_var, ws_var = dv.aggtest(ag.dp_var, 'Usage', binsize="auto", debug=False)
```

## Evaluating Accuracy and Utility
```python
import burdock.evaluation.dp_verification as dp
import burdock.evaluation.aggregation as agg

dv = dp.DPVerification(dataset_size=10000)
ag = agg.Aggregation(t=1, repeat_count=10000)

confidence_level = 0.95
# Generating a simulation neighboring pair dataset
d1, d2, d1_metadata, d2_metadata = dv.generate_neighbors(load_csv=True)
# Passing in a sample query
d1_query = "SELECT SUM(Usage) AS Usage FROM d1.d1"
# Generating repeated query DP results
fD_noisy, fD_actual, fD_low, fD_high = ag.run_agg_query(d1, d1_metadata, d1_query, confidence_level)
# Testing accuracy and utility
acc_res, utility_res, within_bounds = self.accuracy_test(fD_actual, fD_low, fD_high, confidence_level)
```

## Evaluating Bias
```python
import burdock.evaluation.dp_verification as dp
import burdock.evaluation.aggregation as agg

# Initializing DP Verification library and Burdock aggregation class that interfaces with Burdock library
dv = dp.DPVerification(dataset_size=10000)
ag = agg.Aggregation(t=1, repeat_count=10000)

# Generating a simulation neighboring pair dataset
d1, d2, d1_metadata, d2_metadata = dv.generate_neighbors(load_csv=True)
# Passing in a sample query
d1_query = "SELECT SUM(Usage) AS Usage FROM d1.d1"
# Generating repeated query DP results
fD_noisy, fD_actual, fD_low, fD_high = ag.run_agg_query(d1, d1_metadata, d1_query, confidence_level)
bias_res, mean_signed_deviation = self.bias_test(fD_actual, fD_noisy)
```

## Plugging in a Custom Privacy Blackbox Algorithm
### This is still in development
```python
import burdock.evaluation.dp_verification as dp
import burdock.evaluation.aggregation as agg

# Initializing DP Verification library and Burdock aggregation class that interfaces with Burdock library
dv = dp.DPVerification(dataset_size=10000)
ag = agg.Aggregation(t=1, repeat_count=10000)

dataset_root = os.getenv('DATASET_ROOT', '/home/ankit/Documents/github/datasets/')
test_csv_path = dataset_root + 'data/PUMS_california_demographics_1000/data.csv'
dp_yarrow_mean_res = dv.yarrow_test(test_csv_path, yarrow.dp_mean, 'income', float, epsilon=self.epsilon, minimum=0, maximum=100, num_records=1000)
dp_yarrow_var_res = dv.yarrow_test(test_csv_path, yarrow.dp_variance, 'educ', int, epsilon=self.epsilon, minimum=0, maximum=12, num_records=1000)
dp_yarrow_moment_res = dv.yarrow_test(test_csv_path, yarrow.dp_moment_raw, 'married', float, epsilon=.15, minimum=0, maximum=12, num_records=1000000, order = 3)
dp_yarrow_covariance_res = dv.yarrow_test(test_csv_path, yarrow.dp_covariance, 'married', int, 'sex', int, epsilon=.15, minimum_x=0, maximum_x=1, minimum_y=0, maximum_y=1, num_records=1000)
```

## Support for complex GROUP BY queries
```python
import burdock.evaluation.dp_verification as dp
import burdock.evaluation.aggregation as agg

# Initializing DP Verification library and Burdock aggregation class that interfaces with Burdock library
dv = dp.DPVerification(dataset_size=10000)
ag = agg.Aggregation(t=1, repeat_count=10000)

d1_query = "SELECT Role, Segment, COUNT(UserId) AS UserCount, SUM(Usage) AS Usage FROM d1.d1 GROUP BY Role, Segment"
d2_query = "SELECT Role, Segment, COUNT(UserId) AS UserCount, SUM(Usage) AS Usage FROM d2.d2 GROUP BY Role, Segment"
dp_res, acc_res, utility_res, bias_res = dv.dp_groupby_query_test(d1_query, d2_query, plot=False, repeat_count=1000)
```

## Plot Histograms
```python
import burdock.evaluation.dp_verification as dp
import burdock.evaluation.aggregation as agg

# Initializing DP Verification library and Burdock aggregation class that interfaces with Burdock library
dv = dp.DPVerification(dataset_size=10000)
ag = agg.Aggregation(t=1, repeat_count=10000)

d1_query = "SELECT Role, Segment, COUNT(UserId) AS UserCount, SUM(Usage) AS Usage FROM d1.d1 GROUP BY Role, Segment"
d2_query = "SELECT Role, Segment, COUNT(UserId) AS UserCount, SUM(Usage) AS Usage FROM d2.d2 GROUP BY Role, Segment"

dp_res, acc_res, utility_res, bias_res = dv.dp_groupby_query_test(d1_query, d2_query, plot=True, repeat_count=1000)
```