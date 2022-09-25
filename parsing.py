"""
Parsing inbound messages for content.
"""

def is_concat(inbound: dict) -> bool:
    """Determines if an inbound sms is part of a concatenated series of messages."""
    assert isinstance(inbound, dict)
    return "concat" in inbound


def content_and_user(inbound: dict) -> tuple[str, str]:
    """Returns a tuple of the content and user."""
    return inbound["text"], inbound["msisdn"]
