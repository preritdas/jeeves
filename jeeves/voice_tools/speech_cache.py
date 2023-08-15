"""Cache spoken text audio urls."""
from pymongo import MongoClient

from jeeves.keys import KEYS


SPEECH_COLL = MongoClient(KEYS.MongoDB.connect_str)["Jeeves"]["voice_cache"]


def cache_speech(text: str, filetype: str, url: str) -> None:
    """Cache the speech."""
    SPEECH_COLL.insert_one(
        {
            "Voice": KEYS.ElevenLabs.voice_id,
            "Filetype": filetype,
            "Text": text,
            "URL": url
        }
    )


def get_speech(text: str, filetype: str) -> str:
    """Get the speech URL from the cache."""
    item = SPEECH_COLL.find_one(
        {"Text": text, "Filetype": filetype, "Voice": KEYS.ElevenLabs.voice_id}
    )

    if not item:
        return ""

    return item["URL"]
