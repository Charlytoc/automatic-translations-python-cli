
import os
import sys
from moviepy.editor import VideoFileClip
from src.openai_functions import transcribe_audio, translate_transcription
from src.eleven import generate_audio

# This should list the files in the ./videos directory
video_files = [f for f in os.listdir('./videos') if not f.endswith('_done')]

# List the available videos and prompt the user to select one
print("📽️ Available videos:")
for index, file in enumerate(video_files):
    print(f"{index + 1}: {file}")

selected_index = input("Enter the number of the video you want to process: ")

TARGET_LANGUAGE = (
    input("Enter the target language or skip to use the default one: ") or "English"
)

try:
    selected_index = int(selected_index) - 1
    if selected_index < 0 or selected_index >= len(video_files):
        raise ValueError
except ValueError:
    print("Invalid selection. Please enter a valid number.")
    sys.exit(1)

video_path = f"./videos/{video_files[selected_index]}"
video_name = video_files[selected_index].split(".")[0]

# Create a directory for the video inside the output directory
output_dir = f"output/{video_name}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_audio_path = f"{output_dir}/{video_name}.mp3"

print(f"Processing {output_audio_path}...")

video = VideoFileClip(video_path)
audio = video.audio
audio.write_audiofile(output_audio_path)

transcription = transcribe_audio(output_audio_path)
translation = translate_transcription(transcription, TARGET_LANGUAGE)

with open(f'{output_dir}/transcription.txt', 'w', encoding='utf-8') as text_file:
    text_file.write(transcription)

with open(f"{output_dir}/translation.txt", "w", encoding='utf-8') as text_file:
    text_file.write(translation)


generate_audio(
    text=translation,
    output_path=f"{output_dir}/generated.mp3"
)
