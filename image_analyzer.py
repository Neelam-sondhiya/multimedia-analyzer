from pathlib import Path
from PIL import Image, ExifTags
from file_utils import validate_file, get_file_size, format_size

def _exif_value(exif, tag_name):
    for tag_id, value in exif.items():
        if ExifTags.TAGS.get(tag_id) == tag_name:
            return value
    return "Not available"

def analyze_image(path):
    path = validate_file(path)

    with Image.open(path) as img:
        exif = img.getexif()
        dpi = img.info.get("dpi")

        if dpi:
            resolution = f"{dpi[0]:.0f} x {dpi[1]:.0f} DPI"
        else:
            resolution = "Not available"

        report = {
            "type": "image",
            "file_name": path.name,
            "file_size": format_size(get_file_size(path)),
            "file_size_bytes": get_file_size(path),
            "file_format": img.format or "Unknown",
            "width": img.width,
            "height": img.height,
            "resolution": resolution,
            "color_mode": img.mode,
            "exif": {
                "camera": (
                    _exif_value(exif, "Model")
                    if _exif_value(exif, "Model") != "Not available"
                    else _exif_value(exif, "Make")
                ),
                "date_taken": _exif_value(exif, "DateTimeOriginal"),
                "orientation": _exif_value(exif, "Orientation"),
                "software": _exif_value(exif, "Software"),
            },
        }
    return report

def print_report(report):
    print("=" * 32)
    print("IMAGE METADATA REPORT")
    print("=" * 32)
    print(f"\nFile Name       : {report['file_name']}")
    print(f"File Size       : {report['file_size']}")
    print(f"File Format     : {report['file_format']}")
    print(f"Width           : {report['width']}")
    print(f"Height          : {report['height']}")
    print(f"Resolution      : {report['resolution']}")
    print(f"Color Mode      : {report['color_mode']}")
    print("\nEXIF Metadata")
    print("-" * 31)
    for key, value in report["exif"].items():
        print(f"{key.replace('_', ' ').title():16}: {value}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Analyze image metadata.")
    parser.add_argument("image", help="Path to JPG/PNG/TIFF/WEBP/BMP image")
    args = parser.parse_args()
    print_report(analyze_image(args.image))
