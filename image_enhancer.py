from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

def enhance_image(input_path, output_path, scale=1.0):
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as img:
        # Preserve transparency for formats that support it.
        enhanced = ImageOps.exif_transpose(img)

        if scale != 1.0:
            new_size = (
                max(1, int(enhanced.width * scale)),
                max(1, int(enhanced.height * scale)),
            )
            enhanced = enhanced.resize(new_size, Image.Resampling.LANCZOS)

        enhanced = ImageEnhance.Contrast(enhanced).enhance(1.10)
        enhanced = ImageEnhance.Sharpness(enhanced).enhance(1.25)
        enhanced = enhanced.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=3))

        # JPEG cannot save RGBA directly.
        if output_path.suffix.lower() in {".jpg", ".jpeg"} and enhanced.mode in {"RGBA", "LA"}:
            enhanced = enhanced.convert("RGB")

        enhanced.save(output_path, quality=95 if output_path.suffix.lower() in {".jpg", ".jpeg", ".webp"} else None)

    return output_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Basic image enhancement.")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--scale", type=float, default=1.0, help="Resize factor, e.g. 2.0")
    args = parser.parse_args()

    result = enhance_image(args.input, args.output, args.scale)
    print(f"Enhanced image saved to: {result}")
