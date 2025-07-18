"""
Configuration file for the Ollama Voice Assistant
Easy to modify settings without changing the main code
"""

# Ollama Configuration
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# Model Configuration
MODEL_NAME = "gemma3n:e2b"  # Change this to use different models

# Available Models (uncomment the one you want to use):
# MODEL_NAME = "gemma3n:e2b"    # Efficient, ~2B parameters, ~2GB VRAM
# MODEL_NAME = "gemma3n:e4b"    # Multimodal, ~4B parameters, ~3GB VRAM
# MODEL_NAME = "gemma3:27b"     # Large, very accurate, ~17GB RAM
# MODEL_NAME = "gemma3:9b"      # Medium, balanced
# MODEL_NAME = "gemma3:2b"      # Small, fast
# MODEL_NAME = "gemma2:2b"      # Legacy, small, fast

# Generation Parameters
GENERATION_OPTIONS = {
    "num_predict": 80,    # Maximum response length
    "temperature": 0.7,   # Creativity (0.0-1.0)
    "top_p": 0.9         # Response diversity
}

# Assistant Configuration
INITIAL_PROMPT = (
    "You're an AI assistant specialized in AI development, embedded systems like the Jetson Nano, and Google technologies. "
    "Answer questions clearly and concisely in a friendly, professional tone. Do not use asterisks, do not ask new questions "
    "or act as the user. Keep replies short to speed up inference. If unsure, admit it and suggest looking into it further."
)

# Knowledge Base Documents (RAG)
KNOWLEDGE_DOCS = [
    "The Jetson Nano is a compact, powerful computer designed by NVIDIA for AI applications at the edge.",
    "Developers can create AI assistants in under 100 lines of Python code using open-source libraries.",
    "Retrieval Augmented Generation enhances AI responses by combining language models with external knowledge bases.",
    "Ollama is a framework for running large language models locally, making it easy to deploy and manage LLMs.",
    "Gemma3n is Google's latest efficient model family, designed to be accessible for developers on edge devices.",
    "The Jetson Orin Nano provides enhanced performance for AI workloads compared to the original Jetson Nano.",
    "Edge AI deployment enables real-time processing without requiring cloud connectivity.",
    "Local AI models provide privacy and reduce latency compared to cloud-based solutions.",
]

# Audio Configuration
AUDIO_CONFIG = {
    "duration": 5,        # Recording duration in seconds
    "sample_rate": 16000, # Audio sample rate
    "channels": 1,        # Mono audio
    "dtype": "int16"      # Audio data type
}

# Platform-specific TTS Configuration
TTS_CONFIG = {
    "jetson": {
        "piper_path": "/home/asier/piper/build/piper",
        "model_path": "/usr/local/share/piper/models/en-us-lessac-medium.onnx"
    },
    "linux": {
        "espeak": True,
        "aplay": True
    },
    "macos": {
        "say": True
    },
    "windows": {
        "powershell_tts": True
    }
}

# FAISS Configuration
FAISS_CONFIG = {
    "dimension": 384,     # Embedding dimension for all-MiniLM-L6-v2
    "top_k": 3           # Number of relevant documents to retrieve
}

# Whisper Configuration
WHISPER_CONFIG = {
    "model": "tiny",      # Model size: tiny, base, small, medium, large
    "language": "en"      # Language for transcription
} 