<a href="https://www.linkedin.com/pulse/microsoft-harvards-institute-quantitative-social-science-john-kahan/"><img src="images/WhiteNoise Logo/SVG/Full_color.svg" align="left" height="65" vspace="8" hspace="18"></a>
## WhiteNoise Samples: Differential Privacy Examples, Notebooks and Documentation
See also the accompanying [WhiteNoise-System](https://github.com/opendifferentialprivacy/whitenoise-system) and [WhiteNoise-Core](https://github.com/opendifferentialprivacy/whitenoise-core) repositories for this system.

##

Differential privacy is the gold standard definition of privacy protection.  The WhiteNoise project aims to connect theoretical solutions from the academic community with the practical lessons learned from real-world deployments, to make differential privacy broadly accessible to future deployments.  Specifically, we provide several basic building blocks that can be used by people involved with sensitive data, with implementations based on vetted and mature differential privacy research.  In WhiteNoise Samples we provide example code and notebooks to:
* demonstrate the use of the WhiteNoise platform, 
* teach the properties of differential privacy, 
* highlight some of the nuances of the WhiteNoise implementation.

## Runtime Library and Validator
[Notebooks on Library Usage:](https://github.com/opendifferentialprivacy/whitenoise-samples/tree/master/analysis) A set of notebooks showing how to create differentially private releases using the WhiteNoise library and private analysis validator.  The library and validator are both written in Rust, but the notebooks are Python and demonstrate the use of our Python bindings.

[<img src="images/figs/plugin_mean_comparison.png" alt="Relative error distributions" height="100">](https://github.com/opendifferentialprivacy/whitenoise-samples/tree/master/analysis)
[<img src="images/figs/example_size.png" alt="Release box plots" height="100">](https://github.com/opendifferentialprivacy/whitenoise-samples/tree/master/analysis)
[<img src="images/figs/example_education.png" alt="Histogram releases" height="100">](https://github.com/opendifferentialprivacy/whitenoise-samples/tree/master/analysis)
[<img src="images/figs/example_utility.png" alt="Utility simulations" height="100">](https://github.com/opendifferentialprivacy/whitenoise-samples/tree/master/analysis)
[<img src="images/figs/example_simulations.png" alt="Bias simulations" height="100">](https://github.com/opendifferentialprivacy/whitenoise-samples/tree/master/analysis)

## SQL Data Access SDK

[Notebooks on SQL Data Access:](https://github.com/opendifferentialprivacy/whitenoise-samples/tree/master/data) A set of notebooks showing how to use SQL to creat differentially private reports.

## Reference Execution Service

## Stochastic Evaluator

[Notebooks on Stochastic Evaluation:](https://github.com/opendifferentialprivacy/whitenoise-samples/tree/master/evaluator) Notebooks demonstrating the use of the stochastic evaluator.

## API Reference Documentation

[WhiteNoise Core Library Reference:](https://opendifferentialprivacy.github.io/whitenoise-core/) The Core Library implments the runtime validator and execution engine.

[WhiteNoise System SDK Reference:](https://opendifferentialprivacy.github.io/whitenoise-samples/docs/api/system/). The System SDK implements the SQL Data Access, Execution Service, and Stochastic Evaluator.
