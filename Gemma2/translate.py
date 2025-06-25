import whisper, requests, os, sounddevice as sd, tempfile, wave, time
from TTS.api import TTS  # Coqui TTS for Japanese text-to-speech

# Load Whisper model for English speech-to-text
whisper_model = whisper.load_model("tiny")

# URL for the LLaMA server running for translation purposes
llama_url = "http://127.0.0.1:8080/completion"

# Initial prompt to guide LLaMA's behavior as a translation assistant
initial_prompt = (
    "You are a translation assistant. Translate all input text from English to Japanese. "
    "Provide a natural and accurate translation without using phrases like 'Translation:', "
    "just return the translated text directly in Japanese. Very short responses. "
    "Don't create new phrases or conversations. Just reply with the translation. Nothing else."
)

# Define sound file paths (to signal recording start/stop)
current_dir = os.path.dirname(os.path.abspath(__file__))
bip_sound = os.path.join(current_dir, "assets/bip.wav")
bip2_sound = os.path.join(current_dir, "assets/bip2.wav")

# Load Coqui TTS model for Japanese text-to-speech synthesis
tts = TTS("tts_models/ja/kokoro/tacotron2-DDC")

# Find the correct audio input device by name (substring match)
def find_device(device_name_substring):
    devices = sd.query_devices()  # Get list of all available audio devices
    for i, device in enumerate(devices):
        if device_name_substring.lower() in device['name'].lower():
            print(f"Found device: {device['name']} at index {i}")
            return i
    raise ValueError(f"Device with name containing '{device_name_substring}' not found")

# Play a sound file to indicate start/stop of recording
def play_sound(sound_file):
    os.system(f"aplay {sound_file}")

# Record audio and save it as a .wav file
def record_audio(filename, duration=5, fs=16000):
    input_device = find_device("920")  # Adjust device name substring (I have a Logitech 920, that's why, modify as needed)
    with sd.InputStream(device=input_device, samplerate=fs, channels=1, dtype='int16') as stream:
        play_sound(bip_sound)  # Beep to indicate start of recording
        audio = stream.read(int(duration * fs))[0]
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(audio.tobytes())
        play_sound(bip2_sound)  # Beep to indicate end of recording

# Transcribe recorded audio into English text using Whisper
def transcribe_audio(filename):
    result = whisper_model.transcribe(filename, language="en")
    return result['text'].strip()

# Send the transcribed text to LLaMA for translation into Japanese
def ask_llama(query):
    data = {
        "prompt": f"{initial_prompt}\nQuestion: {query}\nAnswer:",  # Pass the transcribed query
        "max_tokens": 30,  # Limit response length to ensure concise replies
        "temperature": 0.7  # Adjust temperature for balanced responses
    }
    response = requests.post(llama_url, json=data, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return response.json().get('content', '').strip()  # Return the translation
    return f"Error: {response.status_code}"

# Convert translated text to speech using Coqui TTS
def text_to_speech(text):
    if not text:
        text = "I could not hear anything, please try again."  # Handle case where input is unclear
    print(f"Llama response (translated to Japanese): {text}")  # Log the translation
    tts.tts_to_file(text=text, file_path="response.wav")  # Save speech as a .wav file
    os.system("aplay response.wav")  # Play the generated audio

# Main loop for the translation assistant
def main():
    while True:
        # Create a temporary .wav file for the recording
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            record_audio(tmpfile.name)  # Record the user's speech
            transcribed_text = transcribe_audio(tmpfile.name)  # Convert speech to text
            print(f"Transcribed text: {transcribed_text}")  # Log the transcribed text
            response = ask_llama(transcribed_text)  # Get the translated text from LLaMA
            if response:
                text_to_speech(response)  # Convert the translation to speech and play it

# Entry point of the script
if __name__ == "__main__":
    main()
