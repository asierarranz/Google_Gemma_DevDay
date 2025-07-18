#!/bin/bash

echo "🚀 Setting up Voice Assistant with Ollama + Gemma3n"
echo "Tested on: Jetson Nano, Jetson Orin Nano, macOS, Linux, Windows"
echo "=================================================="

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install it first:"
    echo "   macOS: brew install ollama"
    echo "   Linux/Jetson: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "   Windows: Download from https://ollama.ai"
    exit 1
fi

echo "✅ Ollama is installed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check if Ollama server is running
echo "🔍 Checking if Ollama server is running..."
if curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
    echo "✅ Ollama server is running"
else
    echo "⚠️  Ollama server is not running. Starting it..."
    echo "   Please run 'ollama serve' in a separate terminal"
    echo "   Then run 'ollama pull gemma3n:e2b' to download the model"
fi

echo ""
echo "🎯 Setup complete! To run the assistant:"
echo "   1. Make sure Ollama server is running: ollama serve"
echo "   2. Download a model: ollama pull gemma3n:e2b"
echo "   3. Run the assistant: python assistant_ollama.py"
echo ""
echo "📝 Available models you can use:"
echo "   - gemma3n:e2b (recommended - efficient, ~2GB VRAM)"
echo "   - gemma3n:e4b (multimodal - image/audio/video, ~3GB VRAM)"
echo "   - gemma3:27b (large, very accurate, ~17GB RAM)"
echo "   - gemma2:2b (small, fast, ~2GB RAM)"
echo ""
echo "   Change the model_name variable in assistant_ollama.py to use a different model"
echo ""
echo "🧪 Test your setup:"
echo "   python test_ollama.py"
echo ""
echo "📖 For text-only demo:"
echo "   python demo_text.py" 