# Gemma3n and Gemma2 demo on Jetson Orin Nano



This repository shows you step-by-step how to use Google's latest AI models, Gemma3N, on your Jetson Orin Nano. We also cover Gemma2 briefly, using demos from my presentation at the Google Gemma Dev Day in Tokyo.


## YouTube Video
This video offers a detailed guide on setting up **Gemma 2** on the Jetson Orin Nano, covering installation, configuration, and execution of the demos. Watch it to get a better understanding of how to replicate the steps on your device:

[![Watch the video](https://img.youtube.com/vi/Kd7VJ-TKb8I/maxresdefault.jpg)](https://www.youtube.com/watch?v=Kd7VJ-TKb8I)



## Overview

- **Gemma3**: Modern implementation using Ollama with Gemma3n models.
- **Gemma2**: Older model with additional demos from the Tokyo event.

## Quick Start

### Gemma3n

```bash
cd Gemma3
./setup.sh
python assistant_ollama.py
```

### Gemma2 (Tokyo demo)

```bash
cd Gemma2
pip install -r requirements.txt
python assistant.py
```

## Project Structure

```
├── Gemma2/                 # Original LLaMA.cpp implementation
│   ├── assistant.py       # Voice assistant with RAG
│   ├── npcservers.py      # Multi-agent NPC conversation demo
│   ├── translate.py       # English to Japanese translation demo
│   ├── requirements.txt   # Python dependencies
│   └── assets/           # Audio files
│
├── Gemma3/                # Modern Ollama implementation
│   ├── assistant_ollama.py # Voice assistant
│   ├── demo_text.py       # Text-only demo
│   ├── test_ollama.py     # Connection test
│   ├── config.py          # Configuration file
│   ├── requirements.txt   # Python dependencies
│   ├── setup.sh          # Setup script
│   └── README.md         # Detailed documentation
│
└── README.md             # This file
```


## Use Cases


### Gemma3 (Ollama) 
- Production deployments on Jetson Orin Nano
- Easy setup and maintenance
- Modern Gemma3n models
- Text and voice interfaces

- 
### Gemma2 (LLaMA.cpp)
- Voice assistant with RAG
- Multi-agent NPC conversation simulation
- English to Japanese translation
- Research and development


## Requirements

### Gemma2
- LLaMA.cpp server running
- Gemma2 model files
- Piper TTS (optional)

### Gemma3
- Ollama installed
- Internet connection (for model download)

## Documentation

- **[Gemma2 Documentation](Gemma2/README.md)** - Original implementation details
- **[Gemma3 Documentation](Gemma3/README.md)** - Modern implementation details


## License

This project is open source and available under the MIT License.

## Acknowledgments

- Google for the Gemma models
- Ollama team for the excellent framework

---

## 🛠️ Installation – Ollama on NVIDIA Systems

To run Gemma 3 locally, you'll need to install **Ollama**.

### On Jetson or Linux

Run the following command in your terminal:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 🚀 Running Gemma 3 with Ollama

Pull and run the desired model size (4B recommended for Jetson):

```bash
ollama pull gemma3:4b
ollama run gemma3:4b
```

For larger variants on AGX Orin:

```bash
ollama pull gemma3:12b
ollama run gemma3:12b

ollama pull gemma3:27b-it-qat
ollama run gemma3:27b-it-qat
```

Run prompts directly:

```bash
ollama run gemma3:12b -p "Summarize a research paper in plain English."
```

For multimodal (image + text) tasks:

```bash
ollama run gemma3:4b "Describe this image" < ./image.png
```


---

## Directory Structure


The project is organized as follows:

```
GEMMALLAMA/
│
├── assets/
│   ├── bip.wav      # Sound file to indicate the start of a recording
│   └── bip2.wav     # Sound file to indicate the end of a recording
│
├── npcs/
│   └── conversation_log.html  # Directory where NPC conversations will be stored in HTML format
│
├── assistant.py     # Script for the Home Assistant demo, using Whisper, FAISS, and Piper
├── npcservers.py    # Script for the multi-agent system demo, where two Gemma instances interact
└── translate.py     # Script for the translation assistant demo, using Whisper and Coqui TTS
```

- **assets/**: Contains audio files (`bip.wav`, `bip2.wav`) used to indicate when recording starts and ends.
- **npcs/**: This folder stores conversation logs in HTML format. For example, when two NPCs (Gemma and Gemmo) converse, their dialogue is saved here.
- **assistant.py**: Implements a voice-activated assistant using Whisper for transcription, FAISS for retrieval, and Piper for text-to-speech.
- **npcservers.py**: Simulates conversations between two LLaMA-based agents (Gemma and Gemmo) with different personalities.
- **translate.py**: Translates speech from English to Japanese using Whisper and Coqui TTS for speech synthesis.

