# Use Python 3.8 with CUDA 11.3 base image
FROM nvidia/cuda:11.3.1-runtime-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# # Install pip
 RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN pip install --no-cache-dir pip setuptools --upgrade

COPY requirements.txt /app/requirements.txt

# Install Python packages
RUN cd /app && pip install --no-cache-dir -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cu113

# Download ESM model files to speed up the inizialization process
RUN apt update && apt install wget unzip -y
RUN mkdir -p /root/.cache/torch/hub/checkpoints/
RUN wget https://dl.fbaipublicfiles.com/fair-esm/models/esm2_t33_650M_UR50D.pt -O /root/.cache/torch/hub/checkpoints/esm2_t33_650M_UR50D.pt
RUN wget https://dl.fbaipublicfiles.com/fair-esm/regression/esm2_t33_650M_UR50D-contact-regression.pt -O /root/.cache/torch/hub/checkpoints/esm2_t33_650M_UR50D-contact-regression.pt
RUN wget https://github.com/facebookresearch/esm/zipball/main -O /root/.cache/torch/hub/main.zip && unzip /root/.cache/torch/hub/main.zip -d /root/.cache/torch/hub/ && mv /root/.cache/torch/hub/facebookresearch-esm-* /root/.cache/torch/hub/facebookresearch_esm_main

# Copy application code
COPY src /app/src

# Set working directory
WORKDIR /app/src

# Expose port
EXPOSE 5000
# Run the application with gunicorn, server production ready instaed of flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "pdb_api:app"]