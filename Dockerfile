# Use Python 3.8 with CUDA 11.3 base image
FROM nvidia/cuda:11.3.1-runtime-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and Python 3.8
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    python3.8-dev \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic links for python and pip
RUN ln -sf /usr/bin/python3.8 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# Upgrade pip and setuptools
RUN pip install --no-cache-dir pip==22.0.4 setuptools==59.5.0

# Install Python packages
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cu113 \
    torch==1.12.1+cu113 \
    numpy==1.21.2 \
    requests==2.26.0 \
    scipy==1.7.1 \
    tqdm==4.62.2 \
    'fair-esm[esmfold]' \
    mkl==2024.0

# Set working directory
WORKDIR /app

# Default command
CMD ["/bin/bash"]