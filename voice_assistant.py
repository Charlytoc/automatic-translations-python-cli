import os
import time
import sounddevice as sd
import numpy as np
import wavio
import asyncio
import openai
from src.openai_functions import transcribe_audio, generate_speech_stream, create_completion_openai
from src.local_ais import create_completion_ollama
from src.utils import print_colored
import simpleaudio as sa
from pydub import AudioSegment
from pydub.playback import play

def get_system_prompt(memory):
    speak_system = f"""
Act as an interactive voice agent.
You will receive the transcription of the latest 4 messages between you and the user.

Current conversation messages:
---
{memory}
---

You must just continue the conversation naturally. Never give long answer if they are not necessary.
"""
    return speak_system

print("\033[92mAvailable audio devices:\033[0m")  # Green color start
device_info = sd.query_devices()
for i, device in enumerate(device_info):
    print(f"ID: \033[92m{i}\033[0m, Name: {device['name']}")  # Green color end

mic_id = int(input("\033[92mEnter the microphone ID: \033[0m"))  # User inputs the correct device ID

# Add this after the microphone ID input
print("\033[92mAvailable voices:\033[0m")
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
for i, voice in enumerate(voices):
    print(f"ID: \033[92m{i}\033[0m, Name: {voice}")

voice_id = int(input("\033[92mEnter the voice ID: \033[0m"))
selected_voice = voices[voice_id]

fs = 44100  # Sample rate
channels = 1  # Number of channels

# Create a directory inside recording_sessions with the date in milliseconds as name
session_dir = f"notes/{int(time.time() * 1000)}"
os.makedirs(session_dir, exist_ok=True)

recording_counter = 0

async def main():
    global recording_counter  # Declare recording_counter as global to access it inside the function
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
            input("\033[92mPress Enter to start recording\033[0m")

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
            TRANSLATION_OUTPUT = f"{session_dir}/recording_{recording_counter}_translated.mp3"
            # Save the recording to a file
            wavio.write(RECORDING_OUTPUT, myrecording, fs, sampwidth=2)

            # Measure transcription time
            start_time = time.time()
            transcription = transcribe_audio(RECORDING_OUTPUT)
            transcription_time = time.time() - start_time
            print(transcription)

            # Save transcription to text file
            with open(f"{session_dir}/note.md", "a", encoding="utf-8") as trans_file:
                trans_file.write(f"\n{transcription}\n\n")

            # Read the current note content
            with open(f"{session_dir}/note.md", "r", encoding="utf-8") as trans_file:
                current_note_content = trans_file.read()

            # Measure response generation time
            start_time = time.time()
            response_text = create_completion_openai(get_system_prompt(current_note_content), transcription)
            response_time = time.time() - start_time
            print_colored(response_text)

            # Save AI response to text file
            with open(f"{session_dir}/note.md", "a", encoding="utf-8") as trans_file:
                trans_file.write(f"\n{response_text}\n\n")

            # Measure speech generation time
            start_time = time.time()
            await generate_speech_stream(
                response_text, TRANSLATION_OUTPUT, output_format="mp3", voice=selected_voice
            )
            speech_time = time.time() - start_time

            # Log times to logs.txt
            with open(f"{session_dir}/logs.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"Recording {recording_counter}:\n")
                log_file.write(f"Transcription time: {transcription_time:.2f} seconds\n")
                log_file.write(f"Response generation time: {response_time:.2f} seconds\n")
                log_file.write(f"Speech generation time: {speech_time:.2f} seconds\n\n")

            recording_counter += 1

        except KeyboardInterrupt:
            print("\nRecording loop terminated by user.")
            break

if __name__ == "__main__":
    asyncio.run(main())
