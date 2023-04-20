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


def transcribe_twilio_recording(recording_url: str) -> str:
    """
    Transcribe a Twilio recording using OpenAI's Whisper API.
    """
    filepath = f"{uuid.uuid1()}.mp3"

    with open(filepath, "wb") as f:
        f.write(requests.get(f"{recording_url}.mp3").content)

    with open(filepath, "rb") as f:
        res = openai.Audio.transcribe("whisper-1", f)

    # Remove the temporary file
    os.remove(filepath)

    return res["text"]
