# Multimedia Analyzer

A Python-based multimedia analysis project developed as an academic project. The project focuses on analyzing image, video, and audio files, performing image enhancement, and exploring voice cloning/synthesis.

## Assignment Tasks

### Task 1 — Image Metadata Analyzer

The Image Metadata Analyzer extracts important information from image files, including:

- File name and file size
- Image format
- Width and height
- Resolution / DPI
- Color mode
- EXIF metadata
- Camera information when available
- Date taken when available
- Orientation
- Software information

**Technology:** Python, Pillow

---

### Task 2 — Video Metadata Analyzer

The Video Metadata Analyzer extracts technical information from video files, including:

- File name and file size
- Container format
- Duration
- Video resolution
- Frame rate
- Video bit rate
- Video codec
- Audio codec
- Audio channels
- Audio sampling rate
- Audio bit rate
- Video metadata

**Technology:** Python, FFmpeg / FFprobe

---

### Task 3 — Audio Metadata Analyzer

The Audio Metadata Analyzer extracts information from audio files, including:

- File name and file size
- Audio format
- Duration
- Bit rate
- Number of channels
- Sampling rate
- Embedded metadata

**Technology:** Python, Mutagen

---

### Task 4 — Voice Cloning

Voice cloning is included as a separate task of the assignment.

The project contains a voice synthesis demonstration designed to work with an authorized voice.

The implementation is kept separate from the multimedia metadata analysis modules.

**Technology:** Python and voice synthesis/cloning technology

> Voice cloning should only be performed with appropriate authorization and consent.

---

### Task 5 — Image Enhancement

The Image Enhancement module performs basic image processing operations such as:

- EXIF orientation correction
- Image resizing
- Contrast enhancement
- Sharpness enhancement
- Unsharp masking
- Saving the enhanced image as a new file

**Technology:** Python, Pillow

---

# Final Integration — Automatic Multimedia Analyzer

After completing the image, audio, and video metadata analyzers, they are integrated into a single automatic multimedia analyzer.

The system automatically identifies the type of input file and selects the appropriate analyzer.

```text
                    Input File
                        |
                        v
                File Type Detection
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
        Image         Audio         Video
          |             |             |
          v             v             v
       Pillow        Mutagen       FFprobe
          |             |             |
          +-------------+-------------+
                        |
                        v
                 Metadata Report
                        |
                        v
                   JSON Report