"""
Transcribe a Twilio (or Telegram) recording using OpenAI's Whisper API.
"""
import requests
from pydub import AudioSegment

from functools import wraps
import time
import io

from jeeves.keys import KEYS


# Authenticate OpenAI
WHISPER_ENDPOINT = "https://api.openai.com/v1/audio/transcriptions"


def retry_transcribe(function):
    """
    Decorator that retries Whisper once if it fails. If there's an error,
    it waits a second and tries again. If it fails again, it raises the error.
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            time.sleep(1)
            return function(*args, **kwargs)

    return wrapper


@retry_transcribe
def _whisper_transcribe_url(url: str = "", bytecode: bytes = b"") -> str:
    """Transcribes with Whisper. Doesn't touch the file."""
    if not url and not bytecode:
        raise ValueError("Must provide either a URL or bytecode.")

    if url and bytecode:
        raise ValueError("Must provide either a URL or bytecode, not both.")

    # Stream the remote file content
    if url:
        remote_file = requests.get(url, stream=True)
        remote_file.raise_for_status()
        raw_bytes = remote_file.raw

    if bytecode:
        raw_bytes = bytecode

    # OpenAI information
    headers = {"Authorization": f"Bearer {KEYS.OpenAI.api_key}"}
    data = {"model": "whisper-1"}
    files = {"file": ("audio.mp3", raw_bytes, "multipart/form-data")}

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


def transcribe_telegram_file_id(file_id: str) -> str:
    """Transcribe a File ID."""
    # Get the file from Telegram
    url = f"https://api.telegram.org/bot{KEYS.Telegram.bot_token}/getFile"
    res = requests.get(url, params={"file_id": file_id})
    res.raise_for_status()

    # Get the file path
    file_path = res.json()["result"]["file_path"]

    # Convert to mp3
    result_stream = io.BytesIO()

    file_path = (
        f"https://api.telegram.org/file/bot{KEYS.Telegram.bot_token}/{file_path}"
    )
    input_stream = io.BytesIO(requests.get(file_path).content)
    segment = AudioSegment.from_file(input_stream, format="ogg")

    segment.export(result_stream, format="mp3")
    result_stream.seek(0)

    # Get the file
    return _whisper_transcribe_url(bytecode=result_stream.getvalue())
