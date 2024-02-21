import os
from dotenv import load_dotenv
from elevenlabs import generate, save, Voice, play

load_dotenv(dotenv_path="../.env")
VOICE_ID = os.environ.get("ELEVEN_VOICE_ID")

def generate_audio(
    text: str,
    voice: Voice = Voice(voice_id=VOICE_ID),
    model: str = "eleven_multilingual_v2",
    output_path: str = None,
    play_audio: bool = True
):
    audio = generate(text=text, voice=voice, model=model)
    if output_path:
        save(audio, output_path)
    if play_audio:
        play(audio=audio)
        
    return audio

if __name__ == "__main__":
    with open("src/example.txt", "r") as transcription_file:
        transcription = transcription_file.read() 
    audio_file_path = "src/example.mp3"

    print(f"Generating audio using voice {VOICE_ID}...")
    generate_audio(transcription, output_path=audio_file_path, play_audio=False)