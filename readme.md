# Automatic Translations Project - Complete Guide

If you want to see a video about how to use this repo, check this [video](https://youtu.be/CA7i_kcks-Q?si=klrLJy5_YdZR0HLZ)

## Prerequisites
Ensure that Python 3.x is installed:
```bash
python --version
```

### FFmpeg
FFmpeg is required for audio and video processing. Follow the steps below to install it:

#### Windows
1. Download the FFmpeg executable from the [official FFmpeg website](https://ffmpeg.org/download.html).
2. Extract the downloaded zip file to a folder (e.g., `C:\ffmpeg`).
3. Add the `bin` directory to your system's PATH:
   - Open the Start Menu, search for "Environment Variables", and select "Edit the system environment variables".
   - Click on "Environment Variables".
   - Under "System variables", find the `Path` variable and click "Edit".
   - Click "New" and add the path to the `bin` directory (e.g., `C:\ffmpeg\bin`).
   - Click "OK" to save the changes.

#### Unix/MacOS
1. Install FFmpeg using a package manager:
   ```bash
   # For Ubuntu/Debian
   sudo apt update
   sudo apt install ffmpeg

   # For MacOS using Homebrew
   brew install ffmpeg
   ```

## Environment Setup
1. Create and activate a virtual environment:
```bash
py -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Unix/MacOS
```
2. Install the dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
1. Duplicate `.env.example` to `.env` and add the credentials:
```bash
cp .env.example .env
```

## Using `main.py`
Place the videos in `/videos` and run:
```bash
python main.py --language [TARGET_LANGUAGE] --action [ACTION]
```
- `--language` or `-l`: Specifies the target language for the translation (default is English).
- `--action` or `-a`: Defines the last action to perform (options: extract, transcribe, translate, all).

### Explanation of Actions
- Extract: Extracts the audio from the source video
- Transcribe: Transcribes the source video into vtt or json format
- Translate: Translates the transcription into the target language
- All: Performs all the above actions and generates a new version of the video in the target language using ElevenLabs (you must have the API KEY)

## Using `record.py`
Record, transcribe, and translate audio in real-time:
1. Choose the microphone ID to record:
   First, the application will show you the available devices, just type the ID of the one you want to use.
2. Set the target language:
   Then, you will be asked to type the language you want to translate to, it can be any language.
3. After that, just press `Enter` to start recording and you're done!

## Using `voice_assistant.py`
This script acts as a voice assistant that records audio, transcribes it, generates responses using OpenAI, and converts the responses into speech. It allows users to select audio devices, voices, and system prompts. The script also logs the times for transcription, response generation, and speech generation, and concatenates audio files into a single conversation file.

## Using `notetaker.py`
This script records audio from a selected microphone and transcribes it. The transcription is then reformatted into a more readable format using markdown syntax. The script saves the formatted transcription to a markdown file.

## Output
- `main.py`: MP3 audio, transcription, translation, and translated audio in `/output`, additionally the translated video if you selected all.
- `record.py`: WAV recordings, transcriptions, translations, and translated audio in `recording_sessions`.
- `voice_assistant.py`: WAV recordings, transcriptions, responses, and concatenated audio files in `notes`.
- `notetaker.py`: WAV recordings and formatted transcriptions in `notes`.

## Additional Information
- `.gitignore` excludes `venv` and `output`.
- Scripts ignore `.gitkeep` in `/videos`.

Follow this guide for efficient use of the Automatic Translations Project.

