# Installation Guide

This guide will walk you through the complete installation steps for the Automatic Translations Project, including the installation of Python, `ffmpeg`, and other dependencies.

## Prerequisites

### Python
Ensure that Python 3.x is installed on your system. You can check the version by running:
```bash
python --version
```
If Python is not installed, you can download it from the [official Python website](https://www.python.org/downloads/).

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

1. Duplicate `.env.example` to `.env` and add the necessary credentials:
   ```bash
   cp .env.example .env
   ```

2. Obtain an OpenAI API key:
   - Go to the [OpenAI website](https://beta.openai.com/signup/).
   - Sign up for an account or log in if you already have one.
   - Navigate to the API section and generate a new API key.
   - Copy the API key and add it to your `.env` file.

## Common Errors and Troubleshooting

### Python Not Found
If you encounter an error indicating that Python is not found, ensure that Python is installed and added to your system's PATH.

### FFmpeg Not Found
If you encounter an error indicating that FFmpeg is not found, ensure that FFmpeg is installed and the `bin` directory is added to your system's PATH.

### Virtual Environment Activation
If you have trouble activating the virtual environment, ensure that you are using the correct command for your operating system:
- Windows: `source venv/Scripts/activate`
- Unix/MacOS: `source venv/bin/activate`

### Dependency Installation Issues
If you encounter issues while installing dependencies, ensure that you have an active internet connection and that you are using the correct version of Python.

## Additional Information

- `.gitignore` excludes `venv` and `output`.
- Scripts ignore `.gitkeep` in `/videos`.

Follow this guide for a smooth installation process and efficient use of the Automatic Translations Project.
