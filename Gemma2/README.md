# Voice Assistant with LLaMA.cpp + Gemma2

Original implementation using LLaMA.cpp and Google's Gemma2 models, optimized for the Jetson Orin Nano platform.

## Overview

This directory contains the original voice assistant implementation along with additional demonstration scripts showcasing different AI capabilities.

## Demos Included

### 1. Voice Assistant (`assistant.py`)
- Main voice assistant with RAG (Retrieval-Augmented Generation)
- Uses Whisper for speech-to-text
- FAISS for document search
- Gemma2 for response generation
- Piper TTS for text-to-speech

### 2. Multi-Agent NPC System (`npcservers.py`)
- Simulates a conversation between two AI agents
- Each agent has a different personality
- Demonstrates multi-agent communication
- Uses two instances of Gemma2 running simultaneously

### 3. Translation Assistant (`translate.py`)
- English to Japanese voice translation
- Real-time speech translation
- Uses Whisper for transcription
- Gemma2 for translation
- Coqui TTS for Japanese speech synthesis

## Quick Start

### Prerequisites
- LLaMA.cpp server running with Gemma2 model
- Piper TTS installed (for voice assistant)
- Coqui TTS installed (for translation demo)

### Installation
```bash
pip install -r requirements.txt
```

### Running the Demos

**Voice Assistant:**
```bash
python assistant.py
```

**Multi-Agent NPC System:**
```bash
python npcservers.py
```

**Translation Assistant:**
```bash
python translate.py
```

## Configuration

### LLaMA.cpp Server
Make sure your LLaMA.cpp server is running on port 8080 with a Gemma2 model loaded.

### Audio Devices
Update the `find_device()` function in each script to match your audio input device.

### TTS Paths
Update the Piper TTS path in the scripts to match your installation:
```python
piper_path = "/home/asier/piper/build/piper"
```

## Requirements

- Python 3.8+
- LLaMA.cpp server
- Gemma2 model files
- Piper TTS (optional)
- Coqui TTS (for translation demo)

## Platform Support

**Tested and optimized for:**
- Jetson Orin Nano (ARM64, Linux)

## Differences from Gemma3

This implementation uses LLaMA.cpp instead of Ollama, providing:
- Direct model control
- Custom server configuration
- Legacy compatibility
- Research and development capabilities

## License

This project is open source and available under the MIT License. 