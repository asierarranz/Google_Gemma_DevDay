#!/usr/bin/env python3
"""
Test script to verify Ollama connection and model functionality
Optimized for Jetson Orin Nano
"""

import requests
import json

def test_ollama_connection():
    """Test if Ollama server is running"""
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("Ollama server is running")
            print(f"Available models: {[m['name'] for m in models]}")
            return True
        else:
            print(f"Ollama server error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Cannot connect to Ollama server")
        print("   Make sure to run: ollama serve")
        return False

def test_model_generation(model_name="gemma3n:e2b"):
    """Test if the model can generate responses"""
    try:
        data = {
            "model": model_name,
            "prompt": "Hello! Can you say 'Hello from Ollama'?",
            "stream": False,
            "options": {
                "num_predict": 20,
                "temperature": 0.7
            }
        }
        
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Model {model_name} is working")
            print(f"Response: {result.get('response', 'No response')}")
            return True
        else:
            print(f"Model generation error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing model: {e}")
        return False

def main():
    print("Testing Ollama Setup")
    print("Optimized for Jetson Orin Nano")
    print("=" * 50)
    
    # Test connection
    if not test_ollama_connection():
        return
    
    print()
    
    # Test model generation
    if not test_model_generation():
        return
    
    print()
    print("All tests passed! Your Ollama setup is ready.")
    print("   You can now run: python assistant_ollama.py")
    print("   Or try the text demo: python demo_text.py")

if __name__ == "__main__":
    main() 