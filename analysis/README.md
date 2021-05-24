# Sample Analysis Notebooks

[<img src="/images/figs/plugin_mean_comparison.png" alt="Relative error distributions" height="100">](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/analysis)
[<img src="/images/figs/example_size.png" alt="Release box plots" height="100">](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/analysis)
[<img src="/images/figs/example_education.png" alt="Histogram releases" height="100">](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/analysis)
[<img src="/images/figs/example_utility.png" alt="Utility simulations" height="100">](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/analysis)
[<img src="/images/figs/example_simulations.png" alt="Bias simulations" height="100">](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/analysis)

## Python Notebooks 
The following notebooks use the SmartNoise Core Rust library and validator through Python bindings.

#### Library Use Overviews
* [Basic PUMS Analysis with SmartNoise](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/basic_data_analysis.ipynb):  Brief tutorial on doing data analysis within the SmartNoise system, with particular examples on how to understand returns from the analysis validator. 
  - Notebook: [`basic_data_analysis.ipynb`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/basic_data_analysis.ipynb)

#### Introductions to Statistical Releases
* [Histograms](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/histograms.ipynb): Demonstrate using the geometric and Laplace mechanisms to generate histograms on continuous, categorical and Boolean variables. 
  - Notebook: [`histograms.ipynb`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/histograms.ipynb)
* [Differentially Private Covariance](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/covariance.ipynb): Demonstrate different approaches to releasing a covariance matrix. 
  - Notebook: [`covariance.ipynb`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/covariance.ipynb)

#### Introductions to Core Concepts
* [Demonstrate the Utility of a Differentially Private Release by Simulation](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/utility_laplace_mean.ipynb): Demonstrate through simulation how the noise of the final answer from a differentially private query on a dataset mean varies by the size of the dataset and the choice of privacy-loss (epsilon) parameter. 
  - Notebook: [`utility_laplace_mean.ipynb`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/utility_laplace_mean.ipynb)
* [Utility of Statistical Releases using the Mental Health in Tech Survey](https://github.com/opendp/smartnoise-samples/blob/master/analysis/tutorial_mental_health_in_tech_survey.ipynb) The purpose of this demo is to showcase the utility of the OpenDP SmartNoise library using the Mental Health in Tech Survey. The notebook will focus on statistical releases in the trusted curator setting. 
  - Notebook: [`tutorial_mental_health_in_tech_survey.ipynb`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/tutorial_mental_health_in_tech_survey.ipynb)

* [Working with Unknown Dataset Sizes](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/unknown_dataset_size.ipynb):  Explain how SmartNoise preserves privacy of dataset size by resizing, demonstrate how to estimate dataset size when unknown, and compare utility of SmartNoise's resizing approach to a standard 'plug-in' approach. 
  - Notebook: [`unknown_dataset_size`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/unknown_dataset_size.ipynb)
* [Accuracy: Pitfalls and Edge Cases](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/accuracy_pitfalls.ipynb): This notebook describes SmartNoise's accuracy calculations, and ways in which an analyst might be tripped up by them. 
  - Notebook: [`accuracy_pitfalls.ipynb`](https://github.com/opendifferentialprivacy/smartnoise-samples/blob/master/analysis/accuracy_pitfalls.ipynb)

