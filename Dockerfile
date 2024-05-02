
# Use the official Ubuntu LTS base image
FROM ubuntu:latest

# Set environment variables to reduce interaction needs
ENV DEBIAN_FRONTEND=noninteractive

# Update Ubuntu Software repository
RUN apt-get update && apt-get install -y wget && apt-get clean

# Download the Miniconda installation script
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /miniconda.sh

# Install Miniconda
RUN bash /miniconda.sh -b -p /opt/miniconda

# Remove the installer script
RUN rm /miniconda.sh

# Set path to conda
ENV PATH=/opt/miniconda/bin:$PATH

# Initialize conda for all shell types
RUN conda init --all

# Optionally, update Conda
RUN conda update -y conda

# Cleanup
RUN conda clean -afy

# Specify the command to run on container startup
CMD [ "/bin/bash" ]
