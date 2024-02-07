import os
import sys
from moviepy.editor import VideoFileClip
from src.openai_functions import transcribe_audio, translate_transcription
from src.eleven import generate_audio
import argparse

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
print(f"Target language: {TARGET_LANGUAGE}")
print(f"Actions to perform: {actions[:selected_action_index+1]}")

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
print(f"Extracting audio from {video_name}...")
video = VideoFileClip(video_path)
audio = video.audio
audio.write_audiofile(output_audio_path)


# Transcribe the audio and translate the transcription
if ACTION in ['transcribe','translate','all']:
    transcription = transcribe_audio(output_audio_path)
    with open(f'{output_dir}/transcription.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(transcription)

if ACTION in ['translate', 'all']:
    translation = translate_transcription(transcription, TARGET_LANGUAGE)
    # Save the transcription and translation to text files
    with open(f"{output_dir}/translation.txt", "w", encoding='utf-8') as text_file:
        text_file.write(translation)

# Generate an audio file from the translated text
if ACTION in ['all']:
    generate_audio(
        text=translation,
        output_path=f"{output_dir}/generated.mp3"
    )
