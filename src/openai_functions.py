import os
from openai import OpenAI
from dotenv import load_dotenv
from .utils import print_colored
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class TranscriptionResult:
    def __init__(self, text, segments, timestamps):
        self.text = text
        self.segments = segments
        self.timestamps = timestamps

def transcribe_audio(audio_file_path, output_format="verbose_json") -> str:
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            response_format=output_format,
            model="whisper-1", 
            file=audio_file
        )

    if output_format == "vtt":
        return transcription
    return transcription.text

def translate_transcription(transcription:str, target_language="English"):
    completion = client.chat.completions.create(
        model="gpt-4-vision-preview",
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": f"You are translator and video editor. You will receive a transcription of a video. Your task is to provide the {target_language} version with the same meaning. The resulting script should be coherent and consistent. Make sure of correcting inconsistencies, keep in mind that the video is a tutorial of an coding exercise of Learnpack, a tool to learn coding skills",
            },
            {"role": "user", "content": transcription},
        ],
    )
    return completion.choices[0].message.content

def translate_transcription_segments(transcription_segments: list[str], target_language="English"):
    # Verify each segment is a string and join them with '$\n'
    transcription_segments_str = "_step_".join(str(segment) for segment in transcription_segments)
    completion = client.chat.completions.create(
        model="gpt-4-vision-preview",
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": f""" 
                Give me the {target_language} version.
                Add the same number of _step_ like the original version in the same places.
                The english version should be coherent and consistent.
                Make sure that the translation is accurate and that the meaning is preserved, keep in mind that this is for a video tutorial of a LearnPack exercise made by 4Geeks Academy.
                """,
            },
            {"role": "user", "content": transcription_segments_str}
        ],
    )
    return completion.choices[0].message.content

