"""Test voice tools."""
import pytest

import string
import random

import voice_tools as vt


@pytest.mark.xfail(reason="Out of ElevenLabs credits.")
def test_speak():
    """Test ElevenLabs Jeeves speaking, both generation and caching."""
    random_words = ' '.join(
        ''.join(
            random.choice(string.ascii_lowercase) for _ in range(5)
        ) for _ in range(3)
    )

    # Test speaking with generation
    link = vt.speak.speak_jeeves(random_words)
    assert "upcdn" in link  # upload.io link, starts with upcdn.io/

    # Test caching
    new_link = vt.speak.speak_jeeves(random_words)
    assert link == new_link  # same link, cached


def test_transcribe(who_are_you_twilio_recording):
    """Test transcribing a Twilio recording."""
    speech = vt.transcribe.transcribe_twilio_recording(
        recording_url=who_are_you_twilio_recording
    )

    assert "who are you" in speech.lower()
