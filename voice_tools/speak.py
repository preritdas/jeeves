"""Use ElevenLabs to speak."""
import elevenlabs
import requests
from pydub import AudioSegment

import io
import uuid

from keys import KEYS
from voice_tools import speech_cache


JEEVES_VOICE_ID = KEYS.ElevenLabs.voice_id

CODECS = {
    "ogg": "libopus"
}


def _upload_result(bytecode: bytes, filetype: str, mime: str) -> str:
    """Upload the result to the server and return the URL."""
    url = f"https://api.upload.io/v2/accounts/{KEYS.UploadIO.account}/uploads/binary"
    headers = {
        "Authorization": f"Bearer {KEYS.UploadIO.api_key}",
        "Content-Type": mime
    }

    # Create a filename
    filename = str(uuid.uuid1()) + f".{filetype}"

    response = requests.post(
        url, 
        headers=headers, 
        data=bytecode, 
        params={"fileName": filename}
    )

    return response.json()["fileUrl"]


def _speak_jeeves(text: str) -> bytes:
    """Speak the text using the Jeeves voice. Returns MP3 bytecode."""
    return elevenlabs.generate(text, KEYS.ElevenLabs.api_key, JEEVES_VOICE_ID)


def speak_jeeves(
    text: str, 
    output_format: str = "mp3", 
    output_mime: str = "audio/mpeg"
) -> str:
    """
    Speak the text using the Jeeves voice. Returns a public URL path.
    If changing the output format or mime type, be sure to change *both* 
    arguments so they match. Otherwise, weird things may happen.
    """
    # Check if the speech is cached
    if (cached_url := speech_cache.get_speech(text, output_format)):
        return cached_url

    # Generate MP3 bytecode
    byte_code = _speak_jeeves(text)

    # Convert if necessary
    if output_format != "mp3":
        segment = AudioSegment.from_mp3(io.BytesIO(byte_code))
        result_stream = io.BytesIO()

        exporter_kwargs = {"format": output_format}
        if output_format.lower() in CODECS:
            exporter_kwargs["codec"] = CODECS[output_format.lower()]

        segment.export(result_stream, **exporter_kwargs)

        result_stream.seek(0)
        byte_code = result_stream.getvalue()

    # Upload for public link with UploadIO
    public_url = _upload_result(byte_code, output_format, output_mime)

    # Cache the speech
    speech_cache.cache_speech(text, output_format)

    return public_url
