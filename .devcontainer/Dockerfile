# Simple devcontainer - Python 3.11
FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.11

# Install graphviz system package
RUN apt-get update && apt-get install -y graphviz && rm -rf /var/lib/apt/lists/*

# Install pip dependencies in container's dev environment
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create app directory
WORKDIR /workspace
