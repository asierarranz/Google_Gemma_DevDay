#!/bin/bash

echo "Jetson Orin Nano Setup for Ollama + Gemma3n"
echo "============================================"

# Check if running on Jetson
if [[ $(uname -m) != "aarch64" ]]; then
    echo "Warning: This script is designed for ARM64 architecture (Jetson)"
    echo "Current architecture: $(uname -m)"
fi

# Check CUDA availability
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits
else
    echo "Warning: NVIDIA GPU not detected"
fi

# Install system dependencies for Jetson
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    portaudio19-dev \
    python3-dev \
    python3-pip \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    espeak \
    espeak-data

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
else
    echo "Ollama is already installed"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Install PyAudio with Jetson-specific flags
echo "Installing PyAudio for Jetson..."
pip3 install pyaudio

# Check audio devices
echo "Available audio devices:"
python3 -c "
import sounddevice as sd
devices = sd.query_devices()
print('Input devices:')
for i, dev in enumerate(devices):
    if dev['max_inputs'] > 0:
        print(f'  {i}: {dev[\"name\"]}')
print('Output devices:')
for i, dev in enumerate(devices):
    if dev['max_outputs'] > 0:
        print(f'  {i}: {dev[\"name\"]}')
"

# Test Ollama connection
echo "Testing Ollama installation..."
if curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
    echo "Ollama server is running"
else
    echo "Ollama server is not running"
    echo "Start it with: ollama serve"
fi

echo ""
echo "Setup complete for Jetson Orin Nano!"
echo ""
echo "Next steps:"
echo "1. Start Ollama: ollama serve"
echo "2. Download model: ollama pull gemma3n:e2b"
echo "3. Test audio: python3 test_audio.py"
echo "4. Run assistant: python3 assistant_ollama.py" 