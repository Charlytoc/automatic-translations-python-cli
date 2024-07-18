# Automatic Translations Project - Complete Guide

## Prerequisites
Ensure that Python 3.x is installed:
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

## Output
- `main.py`: MP3 audio, transcription, translation, and translated audio in `/output`, additionally the translated video if you selected all.
- `record.py`: WAV recordings, transcriptions, translations, and translated audio in `recording_sessions`.

## Additional Information
- `.gitignore` excludes `venv` and `output`.
- The scripts ignore `.gitkeep` in `/videos`.