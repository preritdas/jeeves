"""
Transcribe a Twilio recording using OpenAI's Whisper API.
"""
import requests

from functools import wraps

from keys import KEYS


# Authenticate OpenAI
WHISPER_ENDPOINT = "https://api.openai.com/v1/audio/transcriptions"


def retry_whisper(function):
    """
    Decorator that retries Whisper once if it fails.
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            return function(*args, **kwargs)

    return wrapper


@retry_whisper
def _whisper_transcribe_url(url: str) -> str:
    """Transcribes with Whisper. Doesn't touch the file."""
    # Stream the remote file content
    remote_file = requests.get(url, stream=True)
    remote_file.raise_for_status()

    # OpenAI information
    headers = {"Authorization": f"Bearer {KEYS.OpenAI.api_key}"}
    data = {"model": "whisper-1"}
    files = {"file": ("audio.mp3", remote_file.raw, "multipart/form-data")}

    response = requests.post(WHISPER_ENDPOINT, headers=headers, data=data, files=files)
    response.raise_for_status()

    return response.json()["text"]


def transcribe_twilio_recording(recording_url: str) -> str:
    """
    Transcribe a Twilio recording using OpenAI's Whisper API.

    Args:
        recording_url (str): The URL of the Twilio recording. This should be the raw
            url from Twilio, without appending .mp3.
    """
    if not recording_url.endswith(".mp3"):
        recording_url += ".mp3"

    return _whisper_transcribe_url(recording_url)
