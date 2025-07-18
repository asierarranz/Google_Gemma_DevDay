#!/usr/bin/env python3
"""
Text-based demo of the Ollama assistant without audio requirements
Optimized for Jetson Orin Nano
"""

import requests
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load sentence transformer model for document embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Ollama server URL for completion
ollama_url = "http://127.0.0.1:11434/api/generate"

# Model name to use with Ollama
model_name = "gemma3n:e2b"  # Modern Gemma3n model optimized for efficiency

# Initial prompt to guide the model's behavior
initial_prompt = ("You're an AI assistant specialized in AI development, embedded systems like the Jetson Nano, and Google technologies. "
                  "Answer questions clearly and concisely in a friendly, professional tone. Do not use asterisks, do not ask new questions "
                  "or act as the user. Keep replies short to speed up inference. If unsure, admit it and suggest looking into it further.")

# Documents to be used in Retrieval-Augmented Generation (RAG)
docs = [
    "The Jetson Nano is a compact, powerful computer designed by NVIDIA for AI applications at the edge.",
    "Developers can create AI assistants in under 100 lines of Python code using open-source libraries.",
    "Retrieval Augmented Generation enhances AI responses by combining language models with external knowledge bases.",
    "Ollama is a framework for running large language models locally, making it easy to deploy and manage LLMs.",
    "Gemma3n is Google's latest efficient model family, designed to be accessible for developers on edge devices.",
    "The Jetson Orin Nano provides enhanced performance for AI workloads compared to the original Jetson Nano.",
    "Edge AI deployment enables real-time processing without requiring cloud connectivity.",
]

# Vector Database class to handle document embedding and search using FAISS
class VectorDatabase:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []
    
    def add_documents(self, docs):
        embeddings = embedding_model.encode(docs)
        self.index.add(np.array(embeddings, dtype=np.float32))
        self.documents.extend(docs)
    
    def search(self, query, top_k=3):
        query_embedding = embedding_model.encode([query])[0].astype(np.float32)
        distances, indices = self.index.search(np.array([query_embedding]), top_k)
        return [self.documents[i] for i in indices[0]]

# Create a VectorDatabase and add documents to it
db = VectorDatabase(dim=384)
db.add_documents(docs)

def ask_ollama(query, context):
    """Send a query and context to Ollama server for completion"""
    data = {
        "model": model_name,
        "prompt": f"{initial_prompt}\nContext: {context}\nQuestion: {query}\nAnswer:",
        "stream": False,
        "options": {
            "num_predict": 80,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(ollama_url, json=data, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return response.json().get('response', '').strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama server. Make sure Ollama is running with 'ollama serve'"
    except Exception as e:
        return f"Error: {str(e)}"

def rag_ask(query):
    """Generate a response using Retrieval-Augmented Generation (RAG)"""
    context = " ".join(db.search(query))
    return ask_ollama(query, context)

def main():
    print("Ollama + Gemma3n Assistant Demo")
    print("Optimized for Jetson Orin Nano")
    print("=" * 50)
    print("This is a text-based demo. Type your questions and press Enter.")
    print("Type 'quit' to exit.")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\n🎤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                print("Assistant: Please say something!")
                continue
            
            # Get context from RAG
            context_docs = db.search(user_input)
            print(f"Context found: {len(context_docs)} relevant documents")
            
            # Generate response
            print("Thinking...")
            response = rag_ask(user_input)
            
            print(f"Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main() 