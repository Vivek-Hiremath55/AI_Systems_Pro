# Use Ubuntu 20.04 as the base image for Python 3.9 support
FROM ubuntu:20.04

# Set the working directory
WORKDIR /app

# Install Python 3.9 and other dependencies
RUN apt-get update && \
    apt-get install -y python3.9 python3.9-dev python3.9-distutils curl && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9

# Use Python 3.9 as the default Python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

# Install necessary Python packages, including torch, torchvision, and scikit-learn 1.5.2
RUN python3.9 -m pip install pandas numpy joblib h5py pillow gradio scikit-learn==1.5.2 prometheus_client torch torchvision

# Copy all local files into the container
COPY . /app

# Expose the port that Gradio will run on
EXPOSE 7860

# Set environment variables for model and data directories
ENV MODEL_DIR="/app/models"
ENV DATA_DIR="/app/data"

# Command to run the UI file that launches the Gradio interface
CMD ["python", "ui_notebook.py"]
