# Sample Analysis Notebooks

## Python Notebooks 
The following notebooks use the WhiteNoise Core Rust library and validator through Python bindings.

#### Library Use Overviews
* [Notebook with Tutorial](https://github.com/opendifferentialprivacy/whitenoise-samples/blob/master/analysis/basic_data_analysis.ipynb):  Brief tutorial on doing data analysis within the WhiteNoise system, with particular examples on how to understand returns from the analysis validator.

#### Introductions to Statistical Releases
* [Notebook on Histograms](https://github.com/opendifferentialprivacy/whitenoise-samples/blob/master/analysis/histograms.ipynb): Demonstrate using the geometric and Laplace mechanisms to generate histograms on continuous, categorical and Boolean variables.
* [Notebook on Covariances](https://github.com/opendifferentialprivacy/whitenoise-samples/blob/master/analysis/covariance.ipynb): Demonstrate different approaches to releasing a covariance matrix.

#### Introductions to Core Concepts
* [Notebook on Utility](https://github.com/opendifferentialprivacy/whitenoise-samples/blob/master/analysis/utility_laplace_mean.ipynb): Demonstrate through simulation how the noise of the final answer from a differentially private query on a dataset mean varies by the size of the dataset and the choice of privacy-loss (epsilon) parameter.
* [Notebook on Dataset Size](https://github.com/opendifferentialprivacy/whitenoise-samples/blob/master/analysis/unknown_dataset_size.ipynb):  Explain how WhiteNoise preserves privacy of dataset size by resizing, demonstrate how to estimate dataset size when unknown, and compare utility of WhiteNoise's resizing approach to standard 'plug-in' approach.
* [Notebook on Accuracy Definition](https://github.com/opendifferentialprivacy/whitenoise-samples/blob/master/analysis/accuracy_pitfalls.ipynb): Explain WhiteNoise's approach to accuracy guarantees and how these compare to accuracy guarantees in the non-private setting.

#### Library Demonstrations
* [Mental Health Survey](https://github.com/opendifferentialprivacy/whitenoise-samples/blob/master/analysis/tutorial_mental_health_in_tech_survey.ipynb): Demonstrate how WhiteNoise can be used to study a set of applied research questions. 
