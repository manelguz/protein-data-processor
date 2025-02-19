FROM ubuntu:20.04

# Copy application code
COPY src/esm_model.py src/handler.py tf/requiremnt_lambda.txt ./

# # Install pip
RUN apt update && apt install -y python3-pip && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools and requirements
RUN pip install --no-cache-dir pip setuptools --upgrade
RUN pip install --no-cache-dir -r requiremnt_lambda.txt 
RUN pip3 install awslambdaric boto3
# Download ESM model files to speed up the inizialization process
RUN apt update && apt install wget unzip -y
RUN mkdir -p /opt/ml/torch/hub/checkpoints/
RUN wget https://dl.fbaipublicfiles.com/fair-esm/models/esm2_t33_650M_UR50D.pt -O /opt/ml/torch/hub/checkpoints/esm2_t33_650M_UR50D.pt
RUN wget https://dl.fbaipublicfiles.com/fair-esm/regression/esm2_t33_650M_UR50D-contact-regression.pt -O /opt/ml/torch/hub/checkpoints/esm2_t33_650M_UR50D-contact-regression.pt
RUN wget https://github.com/facebookresearch/esm/zipball/main -O /opt/ml/torch/hub/main.zip && unzip /opt/ml/torch/hub/main.zip -d /opt/ml/torch/hub/ && mv /opt/ml/torch/hub/facebookresearch-esm-* /opt/ml/torch/hub/facebookresearch_esm_main

ENTRYPOINT [ "/usr/bin/python3.8", "-m", "awslambdaric" ]
CMD ["handler.lambda_handler"]