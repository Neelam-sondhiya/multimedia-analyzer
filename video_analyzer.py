import json
import shutil
import subprocess
from pathlib import Path
from file_utils import validate_file, get_file_size, format_size

def _require_ffprobe():
    if shutil.which("ffprobe") is None:
        raise RuntimeError(
            "ffprobe was not found. Install FFmpeg and add its bin folder to PATH."
        )

def _run_ffprobe(path):
    _require_ffprobe()
    command = [
        "ffprobe", "-v", "error",
        "-show_entries",
        "format=format_name,duration,bit_rate:stream=index,codec_type,codec_name,width,height,"
        "r_frame_rate,bit_rate,channels,sample_rate",
        "-of", "json",
        str(path)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed.")
    return json.loads(result.stdout)

def _fps(value):
    if not value or value == "0/0":
        return "Not available"
    try:
        a, b = value.split("/")
        return f"{float(a) / float(b):.2f} fps" if float(b) else "Not available"
    except Exception:
        return value

def _seconds(value):
    if value is None:
        return "Not available"
    total = float(value)
    h = int(total // 3600)
    m = int((total % 3600) // 60)
    s = total % 60
    return f"{h:02d}:{m:02d}:{s:05.2f}"

def _bitrate(value):
    if not value:
        return "Not available"
    try:
        return f"{int(value) / 1000:.0f} kbps"
    except Exception:
        return str(value)

def analyze_video(path):
    path = validate_file(path)
    data = _run_ffprobe(path)
    streams = data.get("streams", [])
    fmt = data.get("format", {})

    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})

    return {
        "type": "video",
        "file_name": path.name,
        "file_size": format_size(get_file_size(path)),
        "file_size_bytes": get_file_size(path),
        "container": fmt.get("format_name", "Not available"),
        "duration_seconds": fmt.get("duration"),
        "video": {
            "resolution": (
                f"{video.get('width')} x {video.get('height')}"
                if video.get("width") and video.get("height") else "Not available"
            ),
            "frame_rate": _fps(video.get("r_frame_rate")),
            "bit_rate": _bitrate(video.get("bit_rate")),
            "codec": video.get("codec_name", "Not available"),
        },
        "audio": {
            "codec": audio.get("codec_name", "Not available"),
            "channels": audio.get("channels", "Not available"),
            "sampling_rate": (
                f"{audio.get('sample_rate')} Hz"
                if audio.get("sample_rate") else "Not available"
            ),
            "bit_rate": _bitrate(audio.get("bit_rate")),
        },
        "metadata": {
            "format_long_name": fmt.get("format_name", "Not available"),
            "stream_count": len(streams),
        },
    }

def print_report(report):
    print("=" * 32)
    print("VIDEO METADATA REPORT")
    print("=" * 32)
    print(f"\nFile Name       : {report['file_name']}")
    print(f"File Size       : {report['file_size']}")
    print(f"Container       : {report['container']}")
    print(f"Duration        : {_seconds(report['duration_seconds'])}")

    print("\nVIDEO")
    print("-" * 32)
    for k, v in report["video"].items():
        print(f"{k.replace('_', ' ').title():16}: {v}")

    print("\nAUDIO")
    print("-" * 32)
    for k, v in report["audio"].items():
        print(f"{k.replace('_', ' ').title():16}: {v}")

    print("\nMETADATA")
    print("-" * 32)
    for k, v in report["metadata"].items():
        print(f"{k.replace('_', ' ').title():16}: {v}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Analyze video metadata.")
    parser.add_argument("video", help="Path to video file")
    args = parser.parse_args()
    print_report(analyze_video(args.video))
