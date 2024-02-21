
import os
import sys
from moviepy.editor import VideoFileClip, AudioFileClip
from src.openai_functions import transcribe_audio, translate_transcription
from src.eleven import generate_audio
from src.utils import print_colored
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
from moviepy.video.fx.all import speedx
from src.utils import print_colored

import argparse

def split_text(text, separator):
    return text.split(separator)

actions = ['extract','transcribe', 'translate', 'all']
# Parse command line arguments
parser = argparse.ArgumentParser(description='Process video files.')
parser.add_argument('--language', '-l', default='English', help='The target language for translation')
parser.add_argument('--action', '-a', choices=actions, default='all', help='The last action to perform')
args = parser.parse_args()

TARGET_LANGUAGE = args.language
ACTION = args.action

selected_action_index = actions.index(ACTION)
actions[-1] = "generate translated audio"

print_colored(f"Target language: {TARGET_LANGUAGE}", "blue")
print_colored(f"Actions to perform: {actions[:selected_action_index+1]}", "blue")

# This section lists the video files that have not been processed yet
video_files = [f for f in os.listdir('./videos') if f != '.gitkeep']

# Display the list of available videos for the user to choose from
print("📽️ Available videos:")
for index, file in enumerate(video_files):
    print(f"\033[92m{index + 1}\033[0m: {file}")

# Prompt the user to select a video to process
selected_index = input("Enter the \033[92m number \033[0m of the video you want to process: ")

# Validate the user's selection and exit if it's invalid
try:
    selected_index = int(selected_index) - 1
    if selected_index < 0 or selected_index >= len(video_files):
        raise ValueError
except ValueError:
    print("Invalid selection. Please enter a valid number.")
    sys.exit(1)

# Define the path for the selected video
video_path = f"./videos/{video_files[selected_index]}"
video_name = video_files[selected_index].split(".")[0]

# Create an output directory for the processed video
output_dir = f"output/{video_name}"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define the path for the output audio file
output_audio_path = f"{output_dir}/{video_name}.mp3"

# Process the video and extract the audio
print_colored(f"Extracting audio from {video_name}...", "green")
video = VideoFileClip(video_path)
audio = video.audio
audio.write_audiofile(output_audio_path)

# Check if transcription or translation already exists
transcription_file_path = f'{output_dir}/transcription.txt'
translation_file_path = f"{output_dir}/translation.txt"

if ACTION in ['transcribe','translate', 'all']:
    if os.path.exists(transcription_file_path):
        print_colored("Transcription already exists", "blue")
        with open(transcription_file_path, 'r', encoding='utf-8') as text_file:
            transcription = text_file.read()
    else:
        print_colored("Transcribing audio...", "green")
        transcription = transcribe_audio(output_audio_path)

        with open(transcription_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(transcription)

if ACTION in ['translate', 'all']:
    if os.path.exists(translation_file_path):
        print_colored("Translation already exists", "blue")
        with open(translation_file_path, 'r', encoding='utf-8') as text_file:
            translation = text_file.read()
    else:
        if 'transcription' not in locals():
            with open(transcription_file_path, 'r', encoding='utf-8') as text_file:
                transcription = text_file.read()
        print_colored("Translating transcription...", "green")
        translation = translate_transcription(transcription, TARGET_LANGUAGE)
        with open(translation_file_path, "w", encoding='utf-8') as text_file:
            text_file.write(translation)


if ACTION in ['all']:
    print_colored("🎤 Generating translated audio...", "green")
    translated_audio_path = f"{output_dir}/generated_audio.mp3"
    generate_audio(
        text=translation,
        output_path=translated_audio_path,
        play_audio=False
    )

    # Load the translated audio
    translated_audio = AudioFileClip(translated_audio_path)

    # Calculate the factor by which to speed up or slow down the video
    video_duration = video.duration
    audio_duration = translated_audio.duration
    speed_factor = audio_duration / video_duration

    # Apply the speed change to the video

    final_video = speedx(video, final_duration=audio_duration +0.5)
    # Set the audio of the new video to the translated audio
    final_video = final_video.set_audio(translated_audio)

    # Define the path for the final video
    final_video_path = f"{output_dir}/{video_name}_translated.mp4"

    # Write the final video to a file
    final_video.write_videofile(final_video_path)

    print("🎉 New video version created!")

