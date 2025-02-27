import pygame
import os
import threading
import time

# Initialize pygame mixer
pygame.mixer.init()

# Flag to track if sound is currently playing
sound_playing = False

def play_alert():
    """
    Play an alert sound when a pothole is detected.
    Uses threading to avoid blocking the main application.
    """
    global sound_playing
    
    # Don't play if sound is already playing
    if sound_playing:
        return
    
    # Set flag
    sound_playing = True
    
    # Start thread to play sound
    sound_thread = threading.Thread(target=_play_sound)
    sound_thread.daemon = True
    sound_thread.start()

def _play_sound():
    """
    Internal function to play the alert sound.
    """
    global sound_playing
    
    try:
        # Check if custom alert sound exists, otherwise use default beep
        sound_file = "alert.mp3"
        if os.path.exists(sound_file):
            pygame.mixer.music.load(sound_file)
        else:
            # Create a simple beep using pygame
            pygame.mixer.music.load(generate_beep())
        
        # Play the sound
        pygame.mixer.music.play()
        
        # Wait for sound to finish
        time.sleep(1)
        
        # Reset flag
        sound_playing = False
        
    except Exception as e:
        print(f"Error playing alert sound: {e}")
        sound_playing = False

def generate_beep():
    """
    Generate a simple beep sound if no alert sound file is available.
    Returns a BytesIO object containing a WAV file.
    """
    from io import BytesIO
    import numpy as np
    import wave
    import struct
    
    # Parameters for the beep sound
    duration = 0.5  # seconds
    frequency = 440  # Hz (A4 note)
    sample_rate = 44100  # samples per second
    
    # Generate samples
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    samples = (np.sin(2 * np.pi * frequency * t) * 32767).astype(np.int16)
    
    # Create a BytesIO object
    buffer = BytesIO()
    
    # Write WAV file to the buffer
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack('h' * len(samples), *samples))
    
    # Reset buffer position
    buffer.seek(0)
    
    return buffer

