# Multimedia Analyzer

A Python multimedia lab project containing:

1. Image metadata analyzer
2. Audio metadata analyzer
3. Video metadata analyzer
4. Consent-based ElevenLabs voice synthesis using an authorized voice ID
5. Basic image enhancement
6. Consolidated automatic file-type detection
7. JSON report generation

## Project structure

```text
multimedia_analyzer/
├── main.py
├── file_utils.py
├── image_analyzer.py
├── audio_analyzer.py
├── video_analyzer.py
├── image_enhancer.py
├── voice_clone_demo.py
├── report_generator.py
├── requirements.txt
├── .gitignore
├── samples/
├── enhanced/
├── generated_audio/
└── reports/
```

## 1. Create virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install packages:

```powershell
pip install -r requirements.txt
```

## 2. Image analyzer

```powershell
python image_analyzer.py samples\image.jpg
```

Supported:
JPG/JPEG, PNG, TIFF, WEBP, BMP

## 3. Audio analyzer

```powershell
python audio_analyzer.py samples\song.mp3
```

## 4. Video analyzer

The video analyzer uses FFmpeg's `ffprobe`.

Check installation:

```powershell
ffprobe -version
```

Then:

```powershell
python video_analyzer.py samples\video.mp4
```

If Windows says `ffprobe is not recognized`, install FFmpeg and add its `bin` folder to PATH.

## 5. Image enhancement

Example:

```powershell
python image_enhancer.py samples\image.jpg enhanced\image_enhanced.jpg --scale 1.5
```

This performs EXIF orientation correction, optional resizing, contrast adjustment and sharpening.

## 6. Authorized ElevenLabs voice demo

Create `.env`:

```text
ELEVENLABS_API_KEY=your_api_key_here
AUTHORIZED_VOICE_ID=your_authorized_voice_id
```

Do not commit `.env` to Git.

Run:

```powershell
python voice_clone_demo.py "Hello, this is my multimedia analyzer project."
```

The voice ID should belong to a voice you are authorized to use. ElevenLabs provides official Python SDK support for text-to-speech and voice cloning.

## 7. Consolidated analyzer

This is the main application:

```powershell
python main.py samples\image.jpg
python main.py samples\song.mp3
python main.py samples\video.mp4
```

`main.py` calls `file_utils.py` to identify the extension and then routes the file to the correct analyzer.

Every successful analysis is also written to:

```text
reports/report.json
```

## Git commands

From the project root:

```powershell
git init
git add .
git commit -m "Initial multimedia analyzer project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/multimedia-analyzer.git
git push -u origin main
```

Before pushing, check:

```powershell
git status
```

The `.gitignore` prevents `.env`, generated audio, enhanced images and JSON reports from being committed accidentally.
