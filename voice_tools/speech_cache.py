"""Cache spoken text audio urls."""
import deta

from keys import KEYS


deta_client = deta.Deta(KEYS["Deta"]["project_key"])
speech_db = deta_client.Base("voice_cache")


def cache_speech(text: str, url: str) -> None:
    """Cache the speech."""
    speech_db.put(
        {
            "Voice": KEYS["ElevenLabs"]["voice_id"],
            "Text": text,
            "URL": url
        }
    )


def get_speech(text: str) -> str:
    """Get the speech URL from the cache."""
    items = speech_db.fetch(
        query={
            "Text": text,
            "Voice": KEYS["ElevenLabs"]["voice_id"]
        }
    ).items

    if not items:
        return ""

    return items[0]["URL"]
