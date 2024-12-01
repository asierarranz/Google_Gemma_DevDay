#!/bin/bash

# Update and upgrade system packages
sudo apt update && sudo apt upgrade -y

# Install required dependencies
sudo apt install -y cmake git libasound2-dev python3 python3-pip python3-venv ffmpeg portaudio19-dev

# Install ONNX Runtime for Python
pip3 install --upgrade pip
pip3 install onnxruntime
