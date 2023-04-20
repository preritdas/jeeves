"""Use ElevenLabs to speak."""
import elevenlabs

import os
import uuid

from keys import KEYS


# Voice cache folder
if not os.path.exists("voice_cache"):
    os.mkdir("voice_cache")


JEEVES_VOICE_ID = "O1lUlMPuT6IOj4I43c6s"


def speak_jeeves(text: str) -> str:
    """Speak the text using the Jeeves voice. Returns a path to the audio file."""
    byte_code = elevenlabs.generate(text, KEYS["ElevenLabs"]["api_key"], JEEVES_VOICE_ID)
    filepath = f"{uuid.uuid1()}.mp3"

    with open(f"voice_cache/{filepath}", "wb") as f:
        f.write(byte_code)

    return filepath
    