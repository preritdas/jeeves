"Test the GPT app."
from apps import gpt


def test_handler():
    """Test the GPT applet handler."""
    res = gpt.handler(
        content = "Write a short three-word tweet."
    )

    assert res
    assert isinstance(res, str)
