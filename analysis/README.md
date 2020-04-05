# Sample Analysis Notebooks

### Python Notebooks 
The following notebooks use the WhiteNoise Core Rust library and validator through Python bindings.

* [Notebook with Tutorial](https://github.com/opendifferentialprivacy/whitenoise-samples/blob/master/analysis/basic_data_analysis.ipynb):  Brief tutorial on doing data analysis within the WhiteNoise system, with particular examples on how to understand returns from the analysis validator.
* [Notebook on Utility](https://github.com/opendifferentialprivacy/whitenoise-samples/analysis/utility_laplace_mean.ipynb): Demonstrate through simulation how the noise of the final answer from a differentially private query on a dataset mean varies by the size of the dataset and the choice of privacy-loss (epsilon) parameter.
* [Notebook on Dataset Size](https://github.com/opendifferentialprivacy/whitenoise-samples/blob/master/analysis/unknown_dataset_size.ipynb):  Explain how WhiteNoise preserves privacy of dataset size by resizing, demonstrate how to estimate dataset size when unknown, and compare utility of WhiteNoise's resizing approach to standard 'plug-in' approach.
