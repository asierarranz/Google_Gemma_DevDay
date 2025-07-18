#!/usr/bin/env python3
"""
Audio test script for Jetson Orin Nano
Tests microphone, speakers, and audio libraries
"""

import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
import sys

def test_audio_devices():
    """Test and list available audio devices"""
    print("Testing Audio Devices on Jetson Orin Nano")
    print("=" * 50)
    
    try:
        devices = sd.query_devices()
        print(f"Found {len(devices)} audio devices")
        
        print("\nInput devices:")
        input_devices = []
        for i, device in enumerate(devices):
            if device['max_inputs'] > 0:
                print(f"  {i}: {device['name']} (channels: {device['max_inputs']})")
                input_devices.append(i)
        
        print("\nOutput devices:")
        output_devices = []
        for i, device in enumerate(devices):
            if device['max_outputs'] > 0:
                print(f"  {i}: {device['name']} (channels: {device['max_outputs']})")
                output_devices.append(i)
        
        return input_devices, output_devices
        
    except Exception as e:
        print(f"Error querying audio devices: {e}")
        return [], []

def test_microphone(duration=3, sample_rate=16000):
    """Test microphone recording"""
    print(f"\nTesting microphone recording ({duration}s)...")
    
    try:
        # Record audio
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        print("Recording... Speak now!")
        sd.wait()
        
        # Check if audio was recorded
        audio_data = audio.flatten()
        max_amplitude = np.max(np.abs(audio_data))
        
        if max_amplitude > 0:
            print(f"Microphone test PASSED - Max amplitude: {max_amplitude}")
            return True
        else:
            print("Microphone test FAILED - No audio detected")
            return False
            
    except Exception as e:
        print(f"Microphone test FAILED - Error: {e}")
        return False

def test_speakers(duration=2, sample_rate=44100):
    """Test speaker output"""
    print(f"\nTesting speakers ({duration}s)...")
    
    try:
        # Generate a test tone
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(2 * np.pi * 440 * t) * 0.3  # 440 Hz sine wave
        
        # Play the tone
        sd.play(tone, sample_rate)
        print("Playing test tone...")
        sd.wait()
        
        print("Speaker test PASSED")
        return True
        
    except Exception as e:
        print(f"Speaker test FAILED - Error: {e}")
        return False

def test_audio_libraries():
    """Test audio library imports"""
    print("\nTesting Audio Libraries")
    print("=" * 30)
    
    libraries = {
        'sounddevice': 'Audio recording/playback',
        'numpy': 'Numerical operations',
        'wave': 'WAV file handling',
        'tempfile': 'Temporary file creation'
    }
    
    all_passed = True
    for lib, description in libraries.items():
        try:
            __import__(lib)
            print(f"✓ {lib}: {description}")
        except ImportError as e:
            print(f"✗ {lib}: {description} - {e}")
            all_passed = False
    
    return all_passed

def test_whisper():
    """Test Whisper installation"""
    print("\nTesting Whisper")
    print("=" * 20)
    
    try:
        import whisper
        print("✓ Whisper imported successfully")
        
        # Test model loading (tiny model)
        print("Loading Whisper tiny model...")
        model = whisper.load_model("tiny")
        print("✓ Whisper model loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Whisper test failed: {e}")
        return False

def main():
    """Main test function"""
    print("Jetson Orin Nano Audio Test Suite")
    print("=" * 40)
    
    # Test audio libraries
    libs_ok = test_audio_libraries()
    
    # Test audio devices
    input_devices, output_devices = test_audio_devices()
    
    # Test microphone if available
    mic_ok = False
    if input_devices:
        mic_ok = test_microphone()
    else:
        print("\nNo input devices found - skipping microphone test")
    
    # Test speakers if available
    speakers_ok = False
    if output_devices:
        speakers_ok = test_speakers()
    else:
        print("\nNo output devices found - skipping speaker test")
    
    # Test Whisper
    whisper_ok = test_whisper()
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    print(f"Audio Libraries: {'PASS' if libs_ok else 'FAIL'}")
    print(f"Input Devices: {len(input_devices)} found")
    print(f"Output Devices: {len(output_devices)} found")
    print(f"Microphone: {'PASS' if mic_ok else 'FAIL'}")
    print(f"Speakers: {'PASS' if speakers_ok else 'FAIL'}")
    print(f"Whisper: {'PASS' if whisper_ok else 'FAIL'}")
    
    if all([libs_ok, mic_ok, speakers_ok, whisper_ok]):
        print("\n🎉 All tests PASSED! Audio system is ready.")
        print("You can now run: python3 assistant_ollama.py")
    else:
        print("\n⚠️  Some tests FAILED. Check the errors above.")
        print("Common solutions:")
        print("- Install missing dependencies: sudo apt-get install portaudio19-dev")
        print("- Check microphone permissions")
        print("- Verify audio device connections")

if __name__ == "__main__":
    main() 