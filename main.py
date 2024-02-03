import os
import sys
from moviepy.editor import VideoFileClip
from src.openai_functions import transcribe_audio, translate_transcription
from src.eleven import generate_audio

# This section lists the video files that have not been processed yet

video_files = [f for f in os.listdir('./videos') if f != '.gitkeep']

# Display the list of available videos for the user to choose from
print("📽️ Available videos:")
for index, file in enumerate(video_files):
    print(f"{index + 1}: {file}")

# Prompt the user to select a video to process
selected_index = input("Enter the number of the video you want to process: ")

# Allow the user to specify a target language or use the default
TARGET_LANGUAGE = (
    input("Enter the target language or skip to use the default one: ") or "English"
)

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
print(f"Processing {output_audio_path}...")
video = VideoFileClip(video_path)
audio = video.audio
audio.write_audiofile(output_audio_path)

# Transcribe the audio and translate the transcription
transcription = transcribe_audio(output_audio_path)
translation = translate_transcription(transcription, TARGET_LANGUAGE)

# Save the transcription and translation to text files
with open(f'{output_dir}/transcription.txt', 'w', encoding='utf-8') as text_file:
    text_file.write(transcription)

with open(f"{output_dir}/translation.txt", "w", encoding='utf-8') as text_file:
    text_file.write(translation)

# Generate an audio file from the translated text
generate_audio(
    text=translation,
    output_path=f"{output_dir}/generated.mp3"
)
