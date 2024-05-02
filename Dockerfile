# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set the maintainer label
LABEL maintainer="tanay.nayak@gmail.com"

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Update and install system-level dependencies
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    git \
    curl \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Download and install Miniconda for ARM64
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

# Add Conda to PATH
ENV PATH="/opt/conda/bin:${PATH}"

# Assuming the Dockerfile is at the same level as the dpok folder

# Copy the environment file from the dpok folder
COPY dpok/environment.yaml /tmp/environment.yml

# Create the environment
RUN conda env create -f /tmp/environment.yml

# Activate the environment
ENV PATH /opt/conda/envs/dpok/bin:$PATH
ENV CONDA_DEFAULT_ENV dpok

# Set the working directory
WORKDIR /usr/src/app

# Copy the local code to the container
COPY . .

# Expose ports (if necessary)
# EXPOSE 5000

# Command to run when starting the container
CMD ["python", "start_container"]
