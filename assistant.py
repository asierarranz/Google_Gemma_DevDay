import whisper, requests, os, sounddevice as sd, numpy as np, tempfile, wave
import faiss
from sentence_transformers import SentenceTransformer
import torch

# Optimization: Use a more efficient embedding model for Jetson Orin Nano
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Optimization: Explicitly use CUDA if available, with fallback to CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
whisper_model = whisper.load_model("base").to(device)

# Configuration for local LLM server
llama_url = "http://127.0.0.1:8080/completion"

# Initial prompt to guide the LLaMA model's behavior
initial_prompt = ("You're a language tutor specialized in teaching Spanish to beginners and advanced learners." "Provide explanations of grammar, vocabulary, and common expressions." "Help with pronunciation and sentence construction, offering tips for practicing and improving fluency. Keep responses clear and easy to understand." "Do not use asterisks, do not ask new questions ""or act as the user. Keep replies short to speed up inference. If unsure, admit it and suggest looking into it further.")


# Current directory and path for beep sound files (used to indicate recording start and end)
current_dir = os.path.dirname(os.path.abspath(__file__))
bip_sound = os.path.join(current_dir, "assets/bip.wav")
bip2_sound = os.path.join(current_dir, "assets/bip2.wav")

# Documents to be used in Retrieval-Augmented Generation (RAG)
docs = ["In Spanish, verbs are conjugated based on tense, mood, and subject. For example, 'hablar' (to speak) becomes 'hablo' (I speak) in the present tense.",
"Common Spanish phrases for beginners include 'Hola' (Hello), '¿Cómo estás?' (How are you?), and 'Gracias' (Thank you).", "The Spanish language has gendered nouns, where words like 'libro' (book) are masculine, and 'mesa' (table) are feminine."
]


# Vector Database class to handle document embedding and search using FAISS
class VectorDatabase:
    def __init__(self, dim):
        # Create FAISS index with specified dimension (384 for SentenceTransformer embeddings)
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
db = VectorDatabase(dim=384)
db.add_documents(docs)

# Play sound (beep) to signal recording start/stop
def play_sound(sound_file):
    os.system(f"aplay {sound_file}")

# Record audio using sounddevice, save it as a .wav file
def record_audio(filename, duration=5, fs=16000):
    
    play_sound(bip_sound)  # Start beep
    print("5 seconds recording started...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording to complete
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())
    play_sound(bip2_sound)  # End beep
    print("recording completed")

# Transcribe recorded audio to text using Whisper
def transcribe_audio(filename):
    return whisper_model.transcribe(filename, language="en")['text']

# Send a query and context to LLaMA server for completion
def ask_llama(query, context):
    data = {
        "prompt": f"{initial_prompt}\nContext: {context}\nQuestion: {query}\nAnswer:",
        "max_tokens": 80,  # Limit response length to avoid delays
        "temperature": 0.7  # Adjust temperature for balanced responses
    }
    response = requests.post(llama_url, json=data, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return response.json().get('content', '').strip()
    else:
        return f"Error: {response.status_code}"

# Generate a response using Retrieval-Augmented Generation (RAG)
def rag_ask(query):
    context = " ".join(db.search(query))  # Search for related docs in the FAISS index
    return ask_llama(query, context)  # Ask LLaMA using the retrieved context

# Convert text to speech using Piper TTS model
def text_to_speech(text):
    os.system(f'echo "{text}" | /home/orin_nano/piper/build/piper --model /usr/local/share/piper/models/en_US-lessac-medium.onnx --output_file response.wav && aplay response.wav')

# Main loop for the assistant
def main():
    while True:
        # Create a temporary .wav file for the recording
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            record_audio(tmpfile.name)  # Record the audio input
            transcribed_text = transcribe_audio(tmpfile.name)  # Convert speech to text
            print(f"Agent heard: {transcribed_text}")
            response = rag_ask(transcribed_text)  # Generate response using RAG and LLaMA
            print(f"Agent response: {response}")
            if response:
                text_to_speech(response)  # Convert response to speech

# Entry point of the script
if __name__ == "__main__":
    main()
