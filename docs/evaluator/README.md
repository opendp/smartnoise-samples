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

```python
import burdock.evaluator
from burdock.mechanisms.laplace import Laplace

eps = 0.1
delta = 0

db_1 = [0.1, 1.0]
db_2 = db_1 + [-10.0]

mechanism = Laplace(eps)

evaluator = Evaluator(mechanism, data)

# ... continued
```

## Evaluating Accuracy

## Evaluating Utility

## Evaluating Bias

## Plugging in a Custom Privacy Algorithm

## Randomly Search Neighboring Databases

## Support for Histograms

## Support for Censoring Dimensions

