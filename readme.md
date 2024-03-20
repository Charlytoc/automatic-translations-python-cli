

# Automatic Translations Project - Comprehensive Guide

If you want to see a video about how to use this repo, check this [video](https://youtu.be/CA7i_kcks-Q?si=klrLJy5_YdZR0HLZ)

## Prerequisites
Ensure Python 3.x is installed:
```bash
python --version
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
1. Duplicate `.env.example` to `.env` and add credentials:
```bash
cp .env.example .env
```

## Using `main.py`
Place videos in `/videos` and run:
```bash
python main.py --language [TARGET_LANGUAGE] --action [ACTION]
```
- `--language` or `-l`: Specify the target language for translation (default is English).
- `--action` or `-a`: Define the last action to perform (options: extract, transcribe, translate, all).

Select a video and language, then start processing.

## Using `record.py`
Record, transcribe, and translate audio in real-time:
1. Choose the microphone ID for recording:
   First, the application will show you the available devices, just type the ID of the one you want to use.
2. Set the target language:
   Then, you will be prompted to write the language you want to translate to, it can be any language.
3. After that, just press `Enter` to start recording and you're all set!

## Output
- `main.py`: MP3 audio, transcription, translation, and translated audio in `/output`.
- `record.py`: WAV recordings, transcriptions, translations, and translated audio in `recording_sessions`.

## Additional Information
- `.gitignore` excludes `venv` and `output`.
- Scripts ignore `.gitkeep` in `/videos`.

Follow this guide for efficient use of the Automatic Translations Project.
