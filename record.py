import os
import time
import sounddevice as sd
import numpy as np
import wavio
from src.eleven import generate_audio
from src.openai_functions import transcribe_audio, translate_transcription

# Print available devices and their IDs

print("\033[92mAvailable audio devices:\033[0m")  # Green color start
device_info = sd.query_devices()
for i, device in enumerate(device_info):
    print(f"ID: \033[92m{i}\033[0m, Name: {device['name']}")  # Green color end


mic_id = int(input("\033[92mEnter the microphone ID: \033[0m"))  # User inputs the correct device ID


TARGET_LANGUAGE = (
    input("\033[94m Write the target language\033[0m or skip to use the default one: ") or "English"
)

print(TARGET_LANGUAGE)
# Define the desired microphone ID
fs = 44100  # Sample rate
channels = 1  # Number of channels

# Create a directory inside recording_sessions with the date in milliseconds as name
session_dir = f"recording_sessions/{int(time.time() * 1000)}_{TARGET_LANGUAGE}"
os.makedirs(session_dir, exist_ok=True)

recording_counter = 0

while True:
    try:
        # Create a list to store the recording chunks
        recording_chunks = []

        # Define the callback function to store data
        def callback(indata, frames, time, status):
            if status:
                print(status)
            recording_chunks.append(indata.copy())

        # Ask the user to press Enter to start recording
        input("Press Enter to start recording")
        print("\033[91m👂🏻 Listening...\033[0m")
        # Start recording with the selected microphone
        stream = sd.InputStream(
            samplerate=fs, channels=channels, callback=callback, device=mic_id
        )
        with stream:
            input("Press Enter to stop recording")
            stream.stop()

        # Concatenate all the recording chunks
        myrecording = np.concatenate(recording_chunks, axis=0)

        RECORDING_OUTPUT = f"{session_dir}/recording_{recording_counter}.wav"
        TRANSLATION_OUTPUT = (
            f"{session_dir}/recording_{recording_counter}_translated.mp3"
        )
        # Save the recording to a file
        wavio.write(RECORDING_OUTPUT, myrecording, fs, sampwidth=2)

        transcription = transcribe_audio(RECORDING_OUTPUT)
        translation = translate_transcription(transcription, TARGET_LANGUAGE)

        # Save transcription and translation to text files
        with open(
            f"{session_dir}/transcription.txt", "a", encoding="utf-8"
        ) as trans_file:
            trans_file.write(f"Recording {recording_counter}:\n{transcription}\n\n")
        with open(
            f"{session_dir}/translation.txt", "a", encoding="utf-8"
        ) as translat_file:
            translat_file.write(f"Recording {recording_counter}:\n{translation}\n\n")

        print("👀 Generating translated audio...")
        # Generate audio and play it automatically
        generate_audio(text=translation, output_path=TRANSLATION_OUTPUT)
        # Increment the counter for the next recording
        recording_counter += 1

    except KeyboardInterrupt:
        print("\nRecording loop terminated by user.")
        break
