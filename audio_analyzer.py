from pathlib import Path
from mutagen import File as MutagenFile
from file_utils import validate_file, get_file_size, format_size

def analyze_audio(path):
    path = validate_file(path)
    audio = MutagenFile(path, easy=False)

    if audio is None:
        raise ValueError("Unsupported or unreadable audio file.")

    info = audio.info
    report = {
        "type": "audio",
        "file_name": path.name,
        "file_size": format_size(get_file_size(path)),
        "file_size_bytes": get_file_size(path),
        "format": audio.__class__.__name__,
        "duration_seconds": getattr(info, "length", None),
        "bitrate": getattr(info, "bitrate", None),
        "channels": getattr(info, "channels", None),
        "sample_rate": getattr(info, "sample_rate", None),
        "metadata": {},
    }

    # Convert common metadata values to JSON-friendly strings.
    for key, value in audio.items():
        report["metadata"][str(key)] = [str(v) for v in value]

    return report

def _seconds(value):
    if value is None:
        return "Not available"
    total = int(value)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def print_report(report):
    print("=" * 32)
    print("AUDIO METADATA REPORT")
    print("=" * 32)
    print(f"\nFile Name       : {report['file_name']}")
    print(f"File Size       : {report['file_size']}")
    print(f"Format          : {report['format']}")
    print(f"Duration        : {_seconds(report['duration_seconds'])}")
    print(f"Bit Rate        : {report['bitrate']} bps" if report["bitrate"] else "Bit Rate        : Not available")
    print(f"Channels        : {report['channels'] or 'Not available'}")
    print(f"Sampling Rate   : {report['sample_rate']} Hz" if report["sample_rate"] else "Sampling Rate   : Not available")
    print("\nMETADATA")
    print("-" * 31)
    if report["metadata"]:
        for key, value in report["metadata"].items():
            print(f"{key:16}: {', '.join(value)}")
    else:
        print("No embedded metadata found.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Analyze audio metadata.")
    parser.add_argument("audio", help="Path to audio file")
    args = parser.parse_args()
    print_report(analyze_audio(args.audio))
