FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    curl \
    diffutils \
    gcc \
    git \
    openjdk-11-jdk \
    jupyter \
    libssl-dev \
    make \
    m4 \
    pkg-config \
    protobuf-compiler \
    python3 \
    python3-pip \
    sudo \
    vim

RUN echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list
RUN curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add
RUN apt-get update && apt-get install sbt

RUN useradd --create-home --shell /bin/bash privacy
RUN echo privacy:pass@word99 | chpasswd
RUN usermod -aG sudo privacy

USER privacy
WORKDIR /home/privacy

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/home/privacy/.cargo/bin:${PATH}"
RUN cargo

COPY profile.txt .
RUN cat profile.txt >> .bashrc && rm profile.txt

COPY jupyter.txt .
RUN jupyter notebook --generate-config && cat jupyter.txt >> .jupyter/jupyter_notebook_config.py && rm jupyter.txt

RUN pip3 install pyspark

#RUN git clone https://github.com/opendifferentialprivacy/whitenoise-core.git
RUN git clone https://github.com/opendifferentialprivacy/whitenoise-core-python.git --recurse-submodules
RUN git clone https://github.com/opendifferentialprivacy/whitenoise-system.git
RUN git clone https://github.com/opendifferentialprivacy/whitenoise-samples.git
RUN git clone https://github.com/opendifferentialprivacy/dp-test-datasets.git


RUN cd whitenoise-core-python && \
    pip3 install -U setuptools && \
    pip3 install -e ".[test,plotting]" && \
    cd ..

RUN cd whitenoise-system && \
    pip3 install -r service/requirements.txt && \
    rm -rf ~/.local && \
    pip3 install -r tests/requirements.txt && \
    pip3 install -e sdk/ && \
    cd ..

RUN sbt exit
RUN pip3 install pyspark

EXPOSE 8989