# Voice Assistant with Ollama + Gemma3n

A modern voice assistant implementation using Ollama and Google's Gemma3n models. This project demonstrates how to create an AI assistant that can run locally on edge devices like the Jetson Nano, Jetson Orin Nano, or any desktop computer.

## 🚀 Quick Setup

### 1. Install Ollama

**macOS:**
```bash
brew install ollama
```

**Linux (including Jetson):**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [ollama.ai](https://ollama.ai)

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

## 🔧 Configuration

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

## 🎤 How to Use

1. **Run the script**: `python assistant_ollama.py`
2. **Speak when you hear the beep**: The assistant will record for 5 seconds
3. **Listen to the response**: The assistant will process your question and respond by voice
4. **Repeat**: The process continues until you press Ctrl+C

## 🔍 Differences from Original Version

### Key Changes:

1. **Ollama API**: Uses Ollama's REST API instead of LLaMA.cpp
2. **Embedding Model**: Changed to `all-MiniLM-L6-v2` (more accessible)
3. **TTS**: Uses cross-platform TTS (espeak, say, piper, or Windows TTS)
4. **Error Handling**: Improved to detect connection issues
5. **Compatibility**: Adapted for Jetson Nano, Jetson Orin Nano, macOS, Linux, and Windows

### Advantages of Ollama:

- ✅ Easy installation and model management
- ✅ Standard REST API
- ✅ Support for multiple models
- ✅ Better memory management
- ✅ Automatic updates

## 🛠️ Troubleshooting

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

## 📝 Available Models

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

## 🎯 Customization

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

## 📊 Performance

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

## 🧪 Testing

Run the test script to verify your setup:

```bash
python test_ollama.py
```

For a text-only demo without audio requirements:

```bash
python demo_text.py
```

## 🖥️ Platform Compatibility

### Tested Platforms:
- ✅ **Jetson Nano** (ARM64, Linux)
- ✅ **Jetson Orin Nano** (ARM64, Linux)
- ✅ **macOS** (Intel/Apple Silicon)
- ✅ **Linux** (x86_64, ARM64)
- ✅ **Windows** (x86_64)

### Platform-Specific Features:
- **Jetson**: Optimized for edge deployment, supports Piper TTS
- **macOS**: Uses built-in `say` command for TTS
- **Linux**: Uses `espeak` or `aplay` for audio
- **Windows**: Uses PowerShell speech synthesis

## 📁 Project Structure

```
Gemma3/
├── assistant_ollama.py    # Main voice assistant
├── demo_text.py          # Text-only demo
├── test_ollama.py        # Connection test
├── requirements.txt      # Python dependencies
├── setup.sh             # Setup script
└── README.md            # This file
```

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License. 