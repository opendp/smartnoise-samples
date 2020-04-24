FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    curl \
    diffutils \
    gcc \
    git \
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

RUN useradd --create-home --shell /bin/bash privacy
RUN usermod -aG sudo privacy

USER privacy
WORKDIR /home/privacy

RUN git clone https://github.com/opendifferentialprivacy/whitenoise-core.git
RUN git clone https://github.com/opendifferentialprivacy/whitenoise-system.git
RUN git clone https://github.com/opendifferentialprivacy/whitenoise-samples.git
RUN git clone https://github.com/opendifferentialprivacy/dp-test-datasets.git

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/home/privacy/.cargo/bin:${PATH}"
RUN cargo

COPY profile.txt .
RUN cat profile.txt >> .bashrc && rm profile.txt

COPY jupyter.txt .
RUN jupyter notebook --generate-config && cat jupyter.txt >> .jupyter/jupyter_notebook_config.py && rm jupyter.txt

RUN pip3 install pyspark

RUN cd whitenoise-core && \
    pip3 install -e bindings-python/ && \
    cd ..

RUN cd whitenoise-system && \
    pip3 install -r service/requirements.txt && \
    rm -rf ~/.local && \
    pip3 install -r tests/requirements.txt && \
    pip3 install -e sdk/ && \
    cd ..

EXPOSE 8989