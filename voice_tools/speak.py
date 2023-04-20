"""Use ElevenLabs to speak."""
import elevenlabs

from keys import KEYS


JEEVES_VOICE_ID = "O1lUlMPuT6IOj4I43c6s"


def speak_jeeves(text: str) -> bytes:
    """Speak the text using the Jeeves voice."""
    return elevenlabs.generate(text, KEYS["ElevenLabs"]["api_key"], JEEVES_VOICE_ID)
    