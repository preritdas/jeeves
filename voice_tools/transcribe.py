"""
Transcribe a Twilio recording using OpenAI's Whisper API.
"""
import openai
import requests
from pydub import AudioSegment

import uuid
import os

from keys import KEYS


# Authenticate OpenAI
openai.api_key = KEYS["OpenAI"]["api_key"]


def _standardize_mp3(filepath: str) -> None:
    """Resets the bitrate, framerate, and channels."""
    segment: AudioSegment = AudioSegment.from_file(filepath, format="mp3")
    segment.set_frame_rate(44100).set_channels(1)
    segment.export(filepath, format="mp3", bitrate="64k")


def retry_whisper(function):
    """
    Decorator that retries Whisper once if it fails.
    """
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            return function(*args, **kwargs)

    return wrapper


@retry_whisper
def _whisper_transcribe(filepath: str) -> str:
    """Transcribes with Whisper. Doesn't touch the file."""
    with open(filepath, "rb") as f:
        res = openai.Audio.transcribe("whisper-1", f)

    return res["text"]


def transcribe_twilio_recording(recording_url: str) -> str:
    """
    Transcribe a Twilio recording using OpenAI's Whisper API.

    Args:
        recording_url (str): The URL of the Twilio recording. This should be the raw
            url from Twilio, without appending .mp3.
    """
    if not recording_url.endswith(".mp3"):
        recording_url += ".mp3"

    filepath = f"{uuid.uuid1()}.mp3"

    with open(filepath, "wb") as f:
        f.write(requests.get(recording_url).content)

    _standardize_mp3(filepath)
    transcription = _whisper_transcribe(filepath)

    # Remove the temporary file
    os.remove(filepath)

    return transcription
