import argparse
from file_utils import identify_file_type, validate_file
from image_analyzer import analyze_image, print_report as print_image_report
from audio_analyzer import analyze_audio, print_report as print_audio_report
from video_analyzer import analyze_video, print_report as print_video_report
from report_generator import save_json_report

def analyze(path):
    path = validate_file(path)
    file_type = identify_file_type(path)

    if file_type == "image":
        report = analyze_image(path)
        print_image_report(report)
    elif file_type == "audio":
        report = analyze_audio(path)
        print_audio_report(report)
    elif file_type == "video":
        report = analyze_video(path)
        print_video_report(report)
    else:
        raise ValueError(
            "Unsupported file type. Supported image: JPG/JPEG/PNG/TIFF/WEBP/BMP; "
            "audio: MP3/WAV/FLAC/M4A/OGG/AAC; video: MP4/MKV/AVI/MOV/WEBM/FLV/WMV."
        )

    report_path = save_json_report(report)
    print(f"\nJSON report saved to: {report_path}")
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Consolidated Multimedia Analyzer - Image, Audio and Video"
    )
    parser.add_argument("file", help="Path to image, audio or video")
    args = parser.parse_args()
    analyze(args.file)
