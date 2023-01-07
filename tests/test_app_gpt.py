"Test the GPT app."
from apps import gpt


def test_handler():
    """Test the GPT applet handler."""
    res = gpt.handler(
        content = "Give me three rhyming words.",
        options = {"tokens": "15"}
    )

    assert res
    assert isinstance(res, str)
