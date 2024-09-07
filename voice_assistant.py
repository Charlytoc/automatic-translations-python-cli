import os
import time
import sounddevice as sd
import numpy as np
import wavio
import asyncio
from pydub import AudioSegment

from src.utils import print_colored, extract_python_code, execute_python_code
from src.prompts import system_prompts, get_system_prompt
from src.openai_functions import (
    transcribe_audio,
    generate_speech_stream,
    create_completion_openai,
)

def list_audio_devices():
    print("\033[92mAvailable audio devices:\033[0m")  # Green color start
    device_info = sd.query_devices()
    working_devices = []

    for i, device in enumerate(device_info):
        try:
            # Try to open an input stream with the device to check if it works
            with sd.InputStream(device=i):
                working_devices.append((i, device["name"]))
        except Exception as e:
            # If the device doesn't work, skip it
            continue

    for i, (device_id, device_name) in enumerate(working_devices):
        print(f"ID: \033[92m{device_id}\033[0m, Name: {device_name}")  # Green color end

    return working_devices

def select_device(working_devices):
    mic_id = int(input("\033[92mEnter the microphone ID: \033[0m"))
    return mic_id

def list_voices():
    print("\033[92mAvailable voices:\033[0m")
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    for i, voice in enumerate(voices):
        print(f"ID: \033[92m{i}\033[0m, Name: {voice}")
    return voices

def select_voice(voices):
    voice_id = int(input("\033[92mEnter the voice ID: \033[0m"))
    return voices[voice_id]

def list_system_prompts():
    print("\033[92mAvailable system prompts:\033[0m")
    for i, prompt in enumerate(system_prompts.keys()):
        print(f"ID: \033[92m{i}\033[0m, Name: {prompt}")

def select_system_prompt():
    prompt_id = int(input("\033[92mEnter the system prompt ID: \033[0m"))
    return list(system_prompts.keys())[prompt_id]

def create_session_directory():
    session_dir = f"notes/{int(time.time() * 1000)}"
    os.makedirs(session_dir, exist_ok=True)
    return session_dir

def save_text_to_file(session_dir, text):
    with open(f"{session_dir}/note.md", "a", encoding="utf-8") as trans_file:
        trans_file.write(f"\n{text}\n\n")

def read_file_content(session_dir):
    with open(f"{session_dir}/note.md", "r", encoding="utf-8") as trans_file:
        return trans_file.read()

def log_times(session_dir, recording_counter, transcription_time, response_time, speech_time):
    with open(f"{session_dir}/logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"Recording {recording_counter}:\n")
        log_file.write(f"Transcription time: {transcription_time:.2f} seconds\n")
        log_file.write(f"Response generation time: {response_time:.2f} seconds\n")
        log_file.write(f"Speech generation time: {speech_time:.2f} seconds\n\n")

def concatenate_audio_files(session_dir, recording_counter):
    conversation = AudioSegment.empty()
    for i in range(recording_counter):
        user_audio = AudioSegment.from_wav(f"{session_dir}/user_{i:02d}.wav")
        ai_audio = AudioSegment.from_mp3(f"{session_dir}/ai_{i:02d}.mp3")
        conversation += user_audio + ai_audio
    conversation.export(f"{session_dir}/conversation.mp3", format="mp3")

async def main():
    working_devices = list_audio_devices()
    mic_id = select_device(working_devices)
    voices = list_voices()
    selected_voice = select_voice(voices)
    list_system_prompts()
    selected_prompt = select_system_prompt()

    fs = 44100
    channels = 1 
    session_dir = create_session_directory()
    recording_counter = 0

    while True:
        try:
            recording_chunks = []

            def callback(indata, frames, time, status):
                if status:
                    print(status)
                recording_chunks.append(indata.copy())

            try:
                text = input("\033[92mPress Enter to start recording or type your note and press Enter:\033[0m")
            except EOFError:
                print("\nNo input available. Concatenating notes and audio files...")
                concatenate_audio_files(session_dir, recording_counter)
                break

            if text:
                print("The user submitted text, appending to the note")
                save_text_to_file(session_dir, text)

            print("\033[91m👂🏻 Listening...\033[0m")
            stream = sd.InputStream(samplerate=fs, channels=channels, callback=callback, device=mic_id)
            with stream:
                input("Press Enter to stop recording")
                stream.stop()

            myrecording = np.concatenate(recording_chunks, axis=0)
            RECORDING_OUTPUT = f"{session_dir}/user_{recording_counter:02d}.wav"
            TRANSLATION_OUTPUT = f"{session_dir}/ai_{recording_counter:02d}.mp3"
            wavio.write(RECORDING_OUTPUT, myrecording, fs, sampwidth=2)

            start_time = time.time()
            transcription = transcribe_audio(RECORDING_OUTPUT)
            transcription_time = time.time() - start_time
            print(transcription)
            save_text_to_file(session_dir, transcription)

            current_note_content = read_file_content(session_dir)

            start_time = time.time()

            print(selected_prompt, "SELECTED PROMPT")
            response_text = create_completion_openai(get_system_prompt(selected_prompt, current_note_content), transcription)

            executable, cleaned_response = extract_python_code(response_text)
            execute_python_code(executable)

            # Check if cleaned_response has at least one word
            if not cleaned_response.strip():
                cleaned_response = "Ready."

            response_time = time.time() - start_time
            print_colored(cleaned_response, color="magenta")
            save_text_to_file(session_dir, response_text)

            start_time = time.time()
            await generate_speech_stream(cleaned_response, TRANSLATION_OUTPUT, output_format="mp3", voice=selected_voice)
            speech_time = time.time() - start_time

            log_times(session_dir, recording_counter, transcription_time, response_time, speech_time)
            recording_counter += 1

        except KeyboardInterrupt:
            print("\nRecording loop terminated by user.")
            concatenate_audio_files(session_dir, recording_counter)
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        print("¡Espero verte pronto!")
