import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
    return transcription.text


def translate_transcription(transcription:str, target_language="en"):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are translator and video editor. You will receive a transcription of a video. Your task is to provide the {target_language} version with the same meaning.",
            },
            {"role": "user", "content": transcription},
        ],
    )
    return completion.choices[0].message.content


