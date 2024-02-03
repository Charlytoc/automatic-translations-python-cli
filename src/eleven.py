import os
from dotenv import load_dotenv
from elevenlabs import generate, save, Voice, play

load_dotenv()


def generate_audio(
    text: str,
    voice: Voice = Voice(voice_id=os.environ.get("ELEVEN_VOICE_ID")),
    model: str = "eleven_multilingual_v2",
    output_path: str = None,
):
    audio = generate(text=text, voice=voice, model=model)
    if output_path:
        save(audio, output_path)
    play(audio=audio)
    return audio
