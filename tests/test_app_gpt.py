"Test the GPT app."
from apps import gpt


def test_handler():
    """Test the GPT applet handler."""
    res = gpt.handler(
        content = "Give me three short rhyming words.",
        options = {"tokens": "20"}
    )

    assert res
    assert isinstance(res, str)
