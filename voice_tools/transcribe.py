"""
Transcribe a Twilio recording using OpenAI's Whisper API.
"""
import openai
import requests

import uuid
import os

from keys import KEYS


# Authenticate OpenAI
openai.api_key = KEYS["OpenAI"]["api_key"]


def retry_whisper(function):
    """
    Decorator that retries Whisper once if it fails.
    """
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            return function(*args, **kwargs)


@retry_whisper
def _whisper_transcribe(filepath: str) -> str:
    """Transcribes with Whisper. Doesn't touch the file."""
    with open(filepath, "rb") as f:
        res = openai.Audio.transcribe("whisper-1", f)

    return res["text"]


def transcribe_twilio_recording(recording_url: str) -> str:
    """
    Transcribe a Twilio recording using OpenAI's Whisper API.
    """
    filepath = f"{uuid.uuid1()}.mp3"

    with open(filepath, "wb") as f:
        f.write(requests.get(f"{recording_url}.mp3").content)

    transcription = _whisper_transcribe(filepath)

    # Remove the temporary file
    os.remove(filepath)

    return transcription
