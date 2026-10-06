"""
CONSENT-BASED VOICE SYNTHESIS DEMO

For the lab, use a voice_id that belongs to a voice you are authorized
to use (for example, your own authorized voice clone). This program does
not bypass verification or create a clone of an unwilling/unknown person.

Set ELEVENLABS_API_KEY and AUTHORIZED_VOICE_ID in .env.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

def generate_speech(text, output_file):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("AUTHORIZED_VOICE_ID")

    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is missing in .env")
    if not voice_id:
        raise RuntimeError("AUTHORIZED_VOICE_ID is missing in .env")

    client = ElevenLabs(api_key=api_key)

    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_v4",
        output_format="mp3_44100_128",
    )

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return output_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate speech with an authorized ElevenLabs voice.")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("--output", default="generated_audio/output.mp3")
    args = parser.parse_args()

    path = generate_speech(args.text, args.output)
    print(f"Generated audio: {path}")
