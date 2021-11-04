# Last tested May 12, 2020 -- May not be up to date
#
FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    curl \
    diffutils \
    gcc \
    git \
    openjdk-8-jdk \
    jupyter \
    jupyter-core \
    jupyter-client \
    libcurl4-openssl-dev \
    libssl-dev \
    libzmq3-dev \
    make \
    m4 \
    pkg-config \
    protobuf-compiler \
    python3 \
    python3-pip \
    sudo \
    vim

# Install R 3.6
RUN apt-get update && apt-get -y install --no-install-recommends --no-install-suggests \
        ca-certificates software-properties-common gnupg2 gnupg1 \
      && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 \
      && add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/' \
      && apt-get -y install r-base

COPY install.R .
RUN Rscript install.R && rm install.R

# Install SBT
RUN apt-get update && apt-get -y install --no-install-recommends --no-install-suggests \
    ca-certificates software-properties-common gnupg2 gnupg1 \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 2EE0EA64E40A89B84B2DF73499E82A75642AC823 \
    && add-apt-repository 'deb https://dl.bintray.com/sbt/debian /' \
    && apt-get -y install sbt

# Create privacy user and switch user
RUN useradd --create-home --shell /bin/bash privacy
RUN echo privacy:pass@word99 | chpasswd
RUN usermod -aG sudo privacy

USER privacy
WORKDIR /home/privacy

# Allow local install of R packages
RUN mkdir .rpackages
RUN echo "R_LIBS=/home/privacy/.rpackages" > .Renviron

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/home/privacy/.cargo/bin:${PATH}"

# Install Conda
RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b && rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH="/home/privacy/miniconda3/bin:${PATH}"
ARG PATH="/home/privacy/miniconda3/bin:${PATH}"

RUN conda init
RUN conda install -y -c conda sqlite pyspark jupyter
RUN conda run pip install z3-solver seaborn

# Jupyter password and port
COPY jupyter.txt .
RUN jupyter notebook --generate-config && cat jupyter.txt >> .jupyter/jupyter_notebook_config.py && rm jupyter.txt

# Clone the repositories
RUN git clone https://github.com/opendifferentialprivacy/smartnoise-samples.git
RUN git clone https://github.com/opendifferentialprivacy/dp-test-datasets.git

# Install Core, Python Bindings, and System
RUN conda run pip install opendp-smartnoise-core opendp-smartnoise

ENTRYPOINT ["jupyter", "notebook"]

EXPOSE 8989
