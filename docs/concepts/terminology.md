# Terminology

These definitions serve as a reference to the terminology used in this documentation.

The ordering and presentation of this Terminology is evolving.

**Private Data**: This is data that we want to protect from re-identification. Examples of entities we wish to protect might be user, device, household, or company.

**Private Data Owner**:  The owner of the private data is known as the private data owner or data curator.

**Private Data Store**:  The physical implementation that houses the data is called a private data store. This data may reside in a SQL Server Database, Spark Cluster, Cloud Blob Storage, CSV file, etc. 

**Privacy Module**: This is a small, self-contained routine that processes private data and returns a privacy-preserving output that is safe against re-identification. Privacy Modules may be provided by independent researchers, and are sometimes called utilities or algorithms. 

Example modules include privacy-preserving logistic regression, k-mean, naïve bayes, neural network, and aggregates (sum, count, mean, median). 

The privacy module is short-running, and typically processes a single small set of private data at a time. We often call the privacy- preserving output a Report. 

Authors of privacy modules typically depend on two pieces of library code that are externally-provided: the Privacy Mechanism, and the Dataset API. 

**Privacy Mechanism**: The mechanism is a small routine that processes a single piece of private data to produce a privacy-preserving output. 
Mechanisms are relatively standardized across the industry and research community. 

Examples include Laplace, Gaussian, Geometric, and Vector. 

The mechanism may be used to privatize an aggregate such as sum or count, or may be used to privatize an objective such as a gradient. 

The mechanism depends on access to a good source of randomness.

**Dataset API**: This is a library, usually maintained by a third-party platform provider, which accesses a data store and returns results in a format that can be consumed by the privacy module. 

Examples could include a native MySQL client library, ADO.NET, a Python library that wraps calls to a remote Spark Cluster, or a statically linked wrapper for CSV file access. 

We assume the “Dataset API” provides a common interface to privacy modules, regardless of the proprietary data store being used. In practice, achieving this generality means the Dataset API will be a wrapper around multiple layers of proprietary data access code.

**Analyst** or **Researcher**: This user role, interchangeably referred to as the Analyst or Researcher, is the entity requesting a report.  
May be an individual or an organization.

> :bulb: For our initial release, the analyst is assumed to be trusted by the data owner.  In future releases, we will provider stronger support for threat models where the analyst is not trusted.


**Report**: The privacy-preserving response returned when an Analyst makes a query or request.  The report consists of two parts:

1. The actual data computed.  

    * i.e. An aggregate where the data is the number “7.8”)

2. A description of how the data was created. 

    * i.e. “7.8 was computed on this dataset using mechanism x and epsilon y at date/time, etc. etc.
    * The format/language for the context depends on the systems involved.  It may be a textual description (with i18n considerations), visualizations, both, etc.

**Query / Request**: Interchangeable terms for the action the user takes to request a privacy-preserving response.

**Epsilon**: The standard measure of privacy exposure is epsilon.  Used as a privacy budget parameter.

A smaller epsilon indicates smaller privacy exposure, and more noise. 

Very roughly, an epsilon below 1.0 might provide plausible deniability for every individual in the database, while epsilon above 1.0 might risk re-identification of some individuals. 

**Delta**: In addition to the epsilon parameter, we typically have a delta parameter, which is set very small (e.g. 10E-30) and indicates the probability of any result failing to provide full epsilon protection.

**Privacy Budget**: When multiple queries are permitted, multiple noisy responses can be combined to re-identify records. In online and adaptive settings, it is imperative to measure both (1) the individual privacy loss and (2) the total loss across all reports. 

The privacy budget is the total amount of privacy loss that can be incurred across all queries before the private data can no longer be accessed. 

A typical privacy budget might be epsilon between 1.0 and 3.0. 

**Privacy Odometer**:  Ongoing tally of privacy spend.  

**Privacy Filter**: Lesser used synonym for Privacy Budget

**Composition**: Composition describes how the privacy cost of multiple queries compose together. 

**Basic Composition**:  Simply adds exposure (e.g. 5 queries of epsilon 0.2 each, sums up to 1.0 epsilon).

**Advanced Composition**: Allows smaller total exposure under some conditions. 

**Homogeneous Composition**:  All queries have identical epsilon and delta.

**Heterogeneous Composition**:  Where different queries may have different epsilon and delta. 

**Optimal Composition**: Important for ensuring maximum utility from data. 
