import os
import tempfile
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
from .utils import print_colored
from pydub import AudioSegment
from pydub.playback import play

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


def create_completion_openai(system_prompt:str,user_message: str):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=200,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": user_message},
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


async def generate_speech_stream(text: str, output_path: str, model: str = "tts-1", voice: str = "alloy", output_format: str = "mp3"):
    try:
        with open(output_path, "wb") as output_file:
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )
        
            response.stream_to_file(output_file.name)

            # Play the audio file
            audio = AudioSegment.from_file(output_file.name, format=output_format)
            play(audio)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


import requests

def generate_speech_api(text: str, model: str = "tts-1-1106", voice: str = "onyx") -> bytes:
    try:
        response = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            },
            json={
                "model": model,
                "input": text,
                "voice": voice,
            },
        )

        response.raise_for_status()  # Raise an error for bad status codes

        audio = b""
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            audio += chunk

        return audio

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return b""
