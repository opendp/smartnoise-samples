# About the Stochastic Evaluator

## Scope

The scope of stochastic evaluation is to find violations of privacy, accuracy, utility, bias properties of black-box algorithms that claim to be differentially private (like a fuzzer). 

In Scope: mechanisms, statistics, models, algorithms, parsing layer
Out of scope: 
* Formally prove privacy properties
* Find all possible violations

## Goals
By building this stochastic evaluator, we intend to automate exploration / fuzzing of cases where one of the promises of a black-box DP algorithm are not met. This’ll be used in - 
* CI/CD testing during development
* Long term fuzzing to look for bugs

## Tests

The tests include - 
* Privacy Test - verifies whether a given differential private query response is adhering to the condition of differential privacy trying out across various neighboring pairs
* Accuracy Test - given confidence level like 95%, on repeatedly querying the responses fall within the confidence interval 95% of the times
* Utility Test - ensures that the confidence interval bounds reported are not too wide and (1-confidence level) of the DP responses do fall outside the bounds
* Bias Test - reports the mean signed deviation of noisy responses as a percentage of actual response on repeated querying

## References
[1] Wilson, R. J., Zhang, C. Y., Lam, W., Desfontaines, D., Simmons-Marengo, D., & Gipson, B. (2019). Differentially Private SQL with Bounded User Contribution. arXiv preprint arXiv:1909.01917.

