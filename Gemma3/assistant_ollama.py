import whisper, requests, os, sounddevice as sd, numpy as np, tempfile, wave
import faiss
from sentence_transformers import SentenceTransformer
from config import *

# Load sentence transformer model for document embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Using a smaller, more accessible model

# Load Whisper model for speech-to-text
whisper_model = whisper.load_model(WHISPER_CONFIG["model"])

# Current directory and path for beep sound files
current_dir = os.path.dirname(os.path.abspath(__file__))
bip_sound = os.path.join(current_dir, "../Gemma2/assets/bip.wav")
bip2_sound = os.path.join(current_dir, "../Gemma2/assets/bip2.wav")

# Vector Database class to handle document embedding and search using FAISS
class VectorDatabase:
    def __init__(self, dim):
        # Create FAISS index with specified dimension (384 for all-MiniLM-L6-v2 embeddings)
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []
    
    # Add documents and their embeddings to the FAISS index
    def add_documents(self, docs):
        embeddings = embedding_model.encode(docs)  # Get embeddings for the docs
        self.index.add(np.array(embeddings, dtype=np.float32))  # Add them to the FAISS index
        self.documents.extend(docs)
    
    # Search for the top K most relevant documents based on query embedding
    def search(self, query, top_k=3):
        query_embedding = embedding_model.encode([query])[0].astype(np.float32)
        distances, indices = self.index.search(np.array([query_embedding]), top_k)
        return [self.documents[i] for i in indices[0]]

# Create a VectorDatabase and add documents to it
db = VectorDatabase(dim=FAISS_CONFIG["dimension"])
db.add_documents(KNOWLEDGE_DOCS)

# Find the device for audio recording by matching part of the device name
def find_device(device_name_substring):
    try:
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device['max_inputs'] > 0 and device_name_substring.lower() in device['name'].lower():
                return i
        # If specific device not found, use first available input device
        for i, device in enumerate(devices):
            if device['max_inputs'] > 0:
                return i
        # Fallback to default
        return sd.default.device[0]
    except:
        return None

# Play sound (beep) to signal recording start/stop
def play_sound(sound_file):
    if os.path.exists(sound_file):
        # Cross-platform sound playback
        if os.name == 'posix':  # Linux/macOS
            if os.path.exists('/usr/bin/aplay'):  # Linux
                os.system(f"aplay {sound_file}")
            else:  # macOS
                os.system(f"afplay {sound_file}")
        else:  # Windows
            os.system(f"start {sound_file}")
    else:
        print("Beep!")  # Fallback if sound file doesn't exist

# Record audio using sounddevice, save it as a .wav file
def record_audio(filename, duration=AUDIO_CONFIG["duration"], fs=AUDIO_CONFIG["sample_rate"]):
    try:
        device_id = find_device("920")  # Try to find Logitech 920
        if device_id is not None:
            sd.default.device = device_id
    except:
        pass  # Use default device if not found
    
    play_sound(bip_sound)  # Start beep
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording to complete
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())
    play_sound(bip2_sound)  # End beep

# Transcribe recorded audio to text using Whisper
def transcribe_audio(filename):
    return whisper_model.transcribe(filename, language="en")['text']

# Send a query and context to Ollama server for completion
def ask_ollama(query, context):
    data = {
        "model": MODEL_NAME,
        "prompt": f"{INITIAL_PROMPT}\nContext: {context}\nQuestion: {query}\nAnswer:",
        "stream": False,
        "options": GENERATION_OPTIONS
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=data, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return response.json().get('response', '').strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama server. Make sure Ollama is running with 'ollama serve'"
    except Exception as e:
        return f"Error: {str(e)}"

# Generate a response using Retrieval-Augmented Generation (RAG)
def rag_ask(query):
    context = " ".join(db.search(query))  # Search for related docs in the FAISS index
    return ask_ollama(query, context)  # Ask Ollama using the retrieved context

# Convert text to speech using system TTS
def text_to_speech(text):
    # Cross-platform TTS
    if os.name == 'posix':  # Linux/macOS
        if os.path.exists('/usr/bin/espeak'):  # Linux with espeak
            os.system(f'espeak "{text}"')
        elif os.path.exists('/usr/bin/say'):  # macOS
            os.system(f'say "{text}"')
        else:  # Try piper if available (Jetson)
            piper_path = "/home/asier/piper/build/piper"
            if os.path.exists(piper_path):
                os.system(f'echo "{text}" | {piper_path} --model /usr/local/share/piper/models/en-us-lessac-medium.onnx --output_file response.wav && aplay response.wav')
            else:
                print(f"🤖 Assistant: {text}")  # Fallback to text output
    else:  # Windows
        os.system(f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"')

# Main loop for the assistant
def main():
    print("Voice Assistant with Ollama + Gemma3n")
    print("Optimized for Jetson Orin Nano")
    print("Press Ctrl+C to exit")
    print("-" * 50)
    
    while True:
        try:
            # Create a temporary .wav file for the recording
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                record_audio(tmpfile.name)  # Record the audio input
                transcribed_text = transcribe_audio(tmpfile.name)  # Convert speech to text
                print(f"You said: {transcribed_text}")
                
                if transcribed_text.strip():  # Only process if there's actual text
                    response = rag_ask(transcribed_text)  # Generate response using RAG and Ollama
                    print(f"Assistant: {response}")
                    if response and not response.startswith("Error"):
                        text_to_speech(response)  # Convert response to speech
                else:
                    print("Assistant: I didn't hear anything. Please try again.")
                
                # Clean up temporary file
                os.unlink(tmpfile.name)
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

# Entry point of the script
if __name__ == "__main__":
    main() 