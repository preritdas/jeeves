"""Use ElevenLabs to speak."""
import elevenlabs
import requests

import os
import uuid

from keys import KEYS
from voice_tools import speech_cache


JEEVES_VOICE_ID = KEYS.ElevenLabs.voice_id


def _upload_result(filepath: str) -> str:
    """Upload the result to the server and return the URL."""
    url = f"https://api.upload.io/v2/accounts/{KEYS.UploadIO.account}/uploads/binary"
    headers = {
        "Authorization": f"Bearer {KEYS.UploadIO.api_key}",
        "Content-Type": "audio/mpeg"
    }

    with open(filepath, "rb") as f:
        data = f.read()
        response = requests.post(url, headers=headers, data=data)

    return response.json()["fileUrl"]


def speak_jeeves(text: str) -> str:
    """Speak the text using the Jeeves voice. Returns a public URL path."""
    # Check if the speech is cached
    if (cached_url := speech_cache.get_speech(text)):
        return cached_url

    byte_code = elevenlabs.generate(text, KEYS.ElevenLabs.api_key, JEEVES_VOICE_ID)
    filepath = f"{uuid.uuid1()}.mp3"

    with open(filepath, "wb") as f:
        f.write(byte_code)

    public_url = _upload_result(filepath)
    os.remove(filepath)

    # Cache the speech
    speech_cache.cache_speech(text, public_url)

    return public_url
