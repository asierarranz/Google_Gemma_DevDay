# Gemma 3 on NVIDIA RTX & Jetson – Powered by Ollama

Google’s latest open model family, **Gemma 3**, is now available on **Ollama**, with optimized performance for **NVIDIA RTX GPUs** and **Jetson edge devices**.

With model sizes ranging from **1B** to **27B parameters**, Gemma 3 brings:

- **Multimodal capabilities** (image + text) in 4B, 12B, and 27B variants
- **Up to 128K context length** for long documents and reasoning tasks
- **Quantization-aware models** that make even 27B run on a single RTX 3090 (~14 GB VRAM)
- **Multi-language support** across 140+ languages
- **Function calling** and structured tool-use capabilities

Gemma 3 is ideal for local prototyping, on-device inference, and edge deployment,  whether you're running on a high-end RTX workstation or a Jetson Orin Nano in the field.

---

## 🛠️ Installation – Ollama on NVIDIA Systems

To run Gemma 3 locally, you'll need to install **Ollama**.

### On Jetson or Linux

Run the following command in your terminal:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```


### On Windows

Download the installer directly from the official Ollama site:

[https://ollama.com/download](https://ollama.com/download)

Once installed, you can run models via the terminal (`ollama run ...`) or through the local API (`localhost:11434`).

---

## 🚀 Running Gemma 3 with Ollama

Pull and run the desired model size (4B recommended for Jetson):

```bash
ollama pull gemma3:4b
ollama run gemma3:4b
```

For larger variants on RTX-class GPUs:

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

## 🧪 Gemma 2 on Jetson Orin Nano – Google Dev Day Tokyo Demos

If you're working with a Jetson Orin Nano and want to explore the power of **Gemma 2**, this repository provides three easy-to-follow demos showcasing how to run a Small Language Model (SLM) with 2 billion parameters on this device. In my talk at the **Google Gemma 2 Dev Day in Tokyo**, I covered everything step-by-step, from setting up the device to running these demos efficiently.

## YouTube Video
This video offers a detailed guide on setting up **Gemma 2** on the Jetson Orin Nano, covering installation, configuration, and execution of the demos. Watch it to get a better understanding of how to replicate the steps on your device:

[![Watch the video](https://img.youtube.com/vi/Kd7VJ-TKb8I/maxresdefault.jpg)](https://www.youtube.com/watch?v=Kd7VJ-TKb8I)

## Demos

1. **Home Assistant Demo**  
   Uses Whisper, FAISS, Gemma 2 and Piper to build a local voice assistant.

2. **Translation Assistant Demo**  
   Translates English to Japanese speech using Whisper, Gemma 2, and Coqui TTS.

3. **Multi-Agent System Demo**  
   Simulates a dialogue between two different personalities using two instances of Gemma 2.

## Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run scripts:

- `home_assistant.py`: Voice assistant with Gemma 2 + RAG
- `translate.py`: English to Japanese voice translation
- `multi_agent.py`: Dual-agent personality simulation

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

