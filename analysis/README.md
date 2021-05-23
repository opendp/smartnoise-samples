# Sample Analysis Notebooks

## Python Notebooks 
The following notebooks use the SmartNoise Core Rust library and validator through Python bindings.

#### Library Use Overviews
* [Basic PUMS Analysis with SmartNoise](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/basic_data_analysis.ipynb):  Brief tutorial on doing data analysis within the SmartNoise system, with particular examples on how to understand returns from the analysis validator. Notebook: [`basic_data_analysis.ipynb`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/basic_data_analysis.ipynb)

#### Introductions to Statistical Releases
* [Histograms](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/histograms.ipynb): Demonstrate using the geometric and Laplace mechanisms to generate histograms on continuous, categorical and Boolean variables. Notebook: [`histograms.ipynb`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/histograms.ipynb)
* [Differentially Private Covariance](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/covariance.ipynb): Demonstrate different approaches to releasing a covariance matrix. Notebook: [`covariance.ipynb`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/covariance.ipynb)

#### Introductions to Core Concepts
* [Demonstrate the Utility of a Differentially Private Release by Simulation](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/utility_laplace_mean.ipynb): Demonstrate through simulation how the noise of the final answer from a differentially private query on a dataset mean varies by the size of the dataset and the choice of privacy-loss (epsilon) parameter. Notebook: [`utility_laplace_mean.ipynb`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/utility_laplace_mean.ipynb)
* [Working with Unknown Dataset Sizes](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/unknown_dataset_size.ipynb):  Explain how SmartNoise preserves privacy of dataset size by resizing, demonstrate how to estimate dataset size when unknown, and compare utility of SmartNoise's resizing approach to a standard 'plug-in' approach. Notebook: [`unknown_dataset_size`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/unknown_dataset_size.ipynb)
