import os
import sys
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
from moviepy.video.fx.all import speedx
from src.openai_functions import transcribe_audio, translate_transcription
from src.eleven import generate_audio
from src.utils import print_colored

import argparse

actions = ["extract", "transcribe", "translate", "all"]

# Interactive action selection
print_colored("Available actions:", "green")
print(
    "The program will execute from the first to the last action selected. For example, if you choose '3', then the actions '1' and '2' will be executed first"
)
for index, action in enumerate(actions):
    print(f"{index + 1}: {action}")
action_input = input("Select the action to perform by entering the number: ")
selected_action_index = int(action_input) - 1
ACTION = actions[selected_action_index]

# Parse command line arguments for language
parser = argparse.ArgumentParser(description="Process video files.")
parser.add_argument(
    "--language", "-l", default="English", help="The target language for translation"
)
args = parser.parse_args()

TARGET_LANGUAGE = args.language

transcription_formats = ["vtt", "verbose_json"]


print_colored(f"Action to perform: {ACTION}", "blue")

# This section lists the video files that have not been processed yet
video_files = [f for f in os.listdir("./videos") if f != ".gitkeep"]

# Display the list of available videos for the user to choose from
print("📽️ Available videos:")
for index, file in enumerate(video_files):
    print(f"\033[92m{index + 1}\033[0m: {file}")

# Prompt the user to select videos to process
selected_indexes = input(
    "Enter the \033[92m numbers \033[0m of the videos you want to process, separated by commas: "
)

# Split the input string by commas and convert each index to an integer
try:
    selected_indexes = [int(index.strip()) - 1 for index in selected_indexes.split(",")]
    for selected_index in selected_indexes:
        if selected_index < 0 or selected_index >= len(video_files):
            raise ValueError
except ValueError:
    print("Invalid selection. Please enter valid numbers separated by commas.")
    sys.exit(1)

# Execute the code for each selected video
for selected_index in selected_indexes:
    video_path = f"./videos/{video_files[selected_index]}"
    video_name = video_files[selected_index].split(".")[0]
    output_dir = f"output/{video_name}"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video = VideoFileClip(video_path)
    transcription = None
    translation = None
    output_audio_path = f"{output_dir}/{video_name}.mp3"

    if ACTION in ["extract", "translate", "all", "transcribe"]:
        print_colored(f"Extracting audio from {video_name}...", "green")
        video.audio.write_audiofile(output_audio_path)

    if ACTION in ["transcribe", "translate", "all"]:
        OUTPUT_FORMAT = input(
            "Enter the output format for the transcription (e.g., 'vtt' or 'verbose_json'): "
        )
        while OUTPUT_FORMAT not in transcription_formats:
            print("Invalid format. Please enter a valid format.")
            OUTPUT_FORMAT = input(
                "Enter the output format for the transcription (e.g., 'vtt' or 'verbose_json'): "
            )

        transcription_file_path = f"{output_dir}/transcription.txt"
        if not os.path.exists(transcription_file_path):
            print_colored("Transcribing audio...", "green")
            transcription = transcribe_audio(
                output_audio_path, output_format=OUTPUT_FORMAT
            )
            with open(transcription_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(transcription)
            print_colored("Audio transcribed succesfully!", "green")
        else:
            with open(transcription_file_path, "r", encoding="utf-8") as text_file:
                transcription = text_file.read()

    if ACTION in ["translate", "all"]:
        print_colored(f"Target language: {TARGET_LANGUAGE}", "blue")
        translation_file_path = f"{output_dir}/translation.txt"
        if not os.path.exists(translation_file_path):
            print_colored("Translating transcription...", "green")
            translation = translate_transcription(transcription, TARGET_LANGUAGE)
            with open(translation_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(translation)
        else:
            with open(translation_file_path, "r", encoding="utf-8") as text_file:
                translation = text_file.read()

    if ACTION == "all":
        translated_audio_path = f"{output_dir}/generated_audio.mp3"
        if not os.path.exists(translated_audio_path):
            print_colored(f"🎤 Generating audio for {video_name}...", "green")
            generate_audio(
                text=translation, output_path=translated_audio_path, play_audio=False
            )

        translated_audio = AudioFileClip(translated_audio_path)
        video_duration = video.duration
        audio_duration = translated_audio.duration
        speed_factor = audio_duration / video_duration

        print_colored(f"🎬 Speed factor: {speed_factor}", "blue")
        final_video = speedx(video, final_duration=audio_duration + 0.5)
        final_video = final_video.set_audio(translated_audio)
        final_video_path = f"{output_dir}/{video_name}_translated.mp4"

        print_colored("🎬 Writing new video...", "blue")
        final_video.write_videofile(final_video_path)

        print("🎉 New video version created!")
