[**Please note that we recently renaming this toolkit.**](https://projects.iq.harvard.edu/opendp/blog/building-inclusive-community)

<a href="https://www.linkedin.com/pulse/microsoft-harvards-institute-quantitative-social-science-john-kahan/"><img src="images/SmartNoise/SVG/LogoMark_color.svg" align="left" height="65" vspace="8" hspace="18"></a>
## SmartNoise Samples: Differential Privacy Examples, Notebooks and Documentation
See also the accompanying [SmartNoise System repository](https://github.com/opendifferentialprivacy/smartnoise-system) and [SmartNoise Core repository](https://github.com/opendifferentialprivacy/smartnoise-core) for this system.

##

Differential privacy is the gold standard definition of privacy protection.  The SmartNoise project, in collaboration with OpenDP, aims to connect theoretical solutions from the academic community with the practical lessons learned from real-world deployments, to make differential privacy broadly accessible to future deployments.  Specifically, we provide several basic building blocks that can be used by people involved with sensitive data, with implementations based on vetted and mature differential privacy research.  In this Samples repository we provide example code and notebooks to:
* demonstrate the use of the system platform, 
* teach the properties of differential privacy, 
* highlight some of the nuances of the system implementation.

## Runtime Library and Validator
[Notebooks on SmartNoise Library Usage:](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/analysis) A set of notebooks showing how to create differentially private releases using the SmartNoise Core library and private analysis validator.  The library and validator are both written in Rust, but the notebooks are Python and demonstrate the use of our Python bindings.

[<img src="images/figs/plugin_mean_comparison.png" alt="Relative error distributions" height="100">](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/analysis)
[<img src="images/figs/example_size.png" alt="Release box plots" height="100">](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/analysis)
[<img src="images/figs/example_education.png" alt="Histogram releases" height="100">](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/analysis)
[<img src="images/figs/example_utility.png" alt="Utility simulations" height="100">](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/analysis)
[<img src="images/figs/example_simulations.png" alt="Bias simulations" height="100">](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/analysis)

## SQL Data Access SDK

[Notebooks on SQL Data Access:](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/data) A set of notebooks showing how to use SQL to create differentially private reports.

## Reference Execution Service

## Stochastic Evaluator

[Notebooks on Stochastic Evaluation:](https://github.com/opendifferentialprivacy/smartnoise-samples/tree/master/evaluator) Notebooks demonstrating the use of the stochastic evaluator.

## API Reference Documentation

[Core Library Reference:](https://opendifferentialprivacy.github.io/smartnoise-core/) The Core Library implments the runtime validator and execution engine.

[System SDK Reference:](https://opendifferentialprivacy.github.io/smartnoise-samples/docs/api/system/). The System SDK implements the SQL Data Access, Execution Service, and Stochastic Evaluator.

## Communication

- Please use [GitHub issues](https://github.com/opendifferentialprivacy/smartnoise-samples/issues) for bug reports, feature requests, install issues, and notebook ideas.
- [Gitter](https://gitter.im/opendifferentialprivacy/WhiteNoise) is available for general chat and online discussions.
- For other requests, please contact us at [smartnoise@opendp.io](mailto:smartnoise@opendp.io).
  - _Note: We encourage you to use [GitHub issues](https://github.com/opendifferentialprivacy/smartnoise-samples/issues), especially for bugs._

## Releases and Contributing

Please let us know if you encounter a bug by [creating an issue](https://github.com/opendifferentialprivacy/smartnoise-samples/issues).

We appreciate all contributions. We welcome pull requests with bug-fixes without prior discussion.

If you plan to contribute new features, utility functions or extensions to the samples repository, please first open an issue and discuss the feature with us.
  - Sending a PR without discussion might end up resulting in a rejected PR, because we may be taking the examples in a different direction than you might be aware of.
