# Voice Assistant with Ollama + Gemma3n

A modern voice assistant implementation using Ollama and Google's Gemma3n models, specifically optimized for the Jetson Orin Nano platform.

## Quick Setup

### 1. Install Ollama

**Jetson Orin Nano:**
```bash
# Use the Jetson-specific setup script
./jetson_setup.sh

# Or install manually
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Start Ollama Server

In a terminal, run:
```bash
ollama serve
```

### 3. Download a Model

In another terminal, download the model you want to use:
```bash
# Modern efficient model (recommended)
ollama pull gemma3n:e2b

# Multimodal model (image, audio, video)
ollama pull gemma3n:e4b

# Alternative models
ollama pull gemma3:27b  # Large, very accurate
ollama pull gemma2:2b   # Small, fast
```

### 4. Install Python Dependencies

```bash
cd Gemma3
pip install -r requirements.txt
```

### 5. Run the Assistant

```bash
python assistant_ollama.py
```

## Configuration

### Change the Model

Edit the `model_name` variable in `assistant_ollama.py`:

```python
model_name = "gemma3n:e2b"  # Modern efficient model
# model_name = "gemma3n:e4b"  # Multimodal model
# model_name = "gemma3:27b"   # Large model
```

### Adjust Parameters

You can modify the generation parameters in the `ask_ollama` function:

```python
"options": {
    "num_predict": 80,    # Maximum response length
    "temperature": 0.7,   # Creativity (0.0-1.0)
    "top_p": 0.9         # Response diversity
}
```

## How to Use

1. **Run the script**: `python assistant_ollama.py`
2. **Speak when you hear the beep**: The assistant will record for 5 seconds
3. **Listen to the response**: The assistant will process your question and respond by voice
4. **Repeat**: The process continues until you press Ctrl+C

## Differences from Original Version

### Key Changes:

1. **Ollama API**: Uses Ollama's REST API instead of LLaMA.cpp
2. **Embedding Model**: Changed to `all-MiniLM-L6-v2` (more accessible)
3. **TTS**: Uses cross-platform TTS (espeak, say, piper, or Windows TTS)
4. **Error Handling**: Improved to detect connection issues
5. **Compatibility**: Adapted for Jetson Orin Nano

### Advantages of Ollama:

- Easy installation and model management
- Standard REST API
- Support for multiple models
- Better memory management
- Automatic updates

## Troubleshooting

### Error: "Cannot connect to Ollama server"
- Make sure `ollama serve` is running
- Verify that port 11434 is available

### Error: "Model not found"
- Download the model: `ollama pull gemma3n:e2b`
- Check the model name in the code

### Audio Issues
- Verify your microphone is working
- Change the audio device in `find_device()`

### Model Too Slow
- Use a smaller model (e2b or 2b)
- Reduce `num_predict` in the options

## Available Models

### Gemma3n (recommended - most modern):
- `gemma3n:e2b` - Efficient, ~2B parameters, ~2GB VRAM
- `gemma3n:e4b` - Multimodal, ~4B parameters, ~3GB VRAM

### Gemma3 (alternative):
- `gemma3:27b` - Large, very accurate, ~17GB RAM
- `gemma3:9b` - Medium, balanced
- `gemma3:2b` - Small, fast

### Gemma2 (legacy):
- `gemma2:27b` - Previous version
- `gemma2:9b` - Medium
- `gemma2:2b` - Small

## Customization

### Add More Context

Edit the `docs` list in the code to add more information to the RAG:

```python
docs = [
    "Your information here...",
    "More context...",
    # Add more documents as needed
]
```

### Change the Prompt

Modify `initial_prompt` to change the assistant's behavior:

```python
initial_prompt = "You are an assistant specialized in..."
```

## Performance

### Gemma3n (recommended):
- **gemma3n:e2b**: ~2GB VRAM, very efficient, fast responses
- **gemma3n:e4b**: ~3GB VRAM, multimodal (image/audio/video)

### Gemma3:
- **gemma3:27b**: ~17GB RAM, very accurate responses
- **gemma3:9b**: ~9GB RAM, good balance
- **gemma3:2b**: ~2GB RAM, fast responses

### Gemma2:
- **gemma2:2b**: ~2GB RAM, fast responses

**Recommendation**: Use `gemma3n:e2b` for the best speed/efficiency ratio.

## Testing

Run the test script to verify your setup:

```bash
python test_ollama.py
```

Test audio functionality on Jetson Orin Nano:

```bash
python test_audio.py
```

For a text-only demo without audio requirements:

```bash
python demo_text.py
```

## Jetson Orin Nano Compatibility

### System Requirements
- Jetson Orin Nano (ARM64 architecture)
- Ubuntu 20.04 or later
- 8GB+ RAM recommended
- 2GB+ VRAM for gemma3n:e2b model

### Jetson-Specific Setup
The project includes a dedicated setup script for Jetson Orin Nano:

```bash
./jetson_setup.sh
```

This script will:
- Install system dependencies (portaudio, espeak, etc.)
- Install Ollama
- Install Python dependencies
- Test audio devices
- Verify CUDA availability

### Audio Configuration
Jetson Orin Nano supports multiple audio configurations:
- **Built-in audio**: HDMI audio, USB audio
- **External microphones**: USB, 3.5mm jack
- **TTS options**: espeak (built-in), Piper TTS (optional)

### Webcam Configuration
The demo was tested with a Logitech C920 webcam. The code specifically looks for "920" in the device name to automatically select this webcam. Feel free to modify the `find_device()` function in the code to use your preferred webcam or audio device:

```python
def find_device():
    # Change "920" to match your device name
    # or modify the logic to select your preferred device
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if "920" in device['name']:  # Change this to your device
            return i
    return None
```

### Performance Optimization
- Uses CUDA acceleration when available
- Optimized for ARM64 architecture
- Memory-efficient model loading
- Real-time audio processing

### Troubleshooting Jetson Issues

**Audio not working:**
```bash
# Test audio system
python test_audio.py

# Install missing dependencies
sudo apt-get install portaudio19-dev libasound2-dev
```

**Ollama not starting:**
```bash
# Check GPU availability
nvidia-smi

# Restart Ollama service
sudo systemctl restart ollama
```

**Memory issues:**
```bash
# Check available memory
free -h

# Use smaller model if needed
ollama pull gemma2:2b
```

## Project Structure

```
Gemma3/
├── assistant_ollama.py    # Main voice assistant
├── demo_text.py          # Text-only demo
├── test_ollama.py        # Connection test
├── test_audio.py         # Audio test for Jetson
├── jetson_setup.sh       # Jetson-specific setup
├── config.py             # Configuration file
├── requirements.txt      # Python dependencies
├── setup.sh             # General setup script
└── README.md            # This file
```

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is open source and available under the MIT License. 