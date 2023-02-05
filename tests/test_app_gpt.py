"Test the GPT app."
# import pytest

from apps import gpt


# @pytest.mark.xfail
def test_handler():
    """Test the GPT applet handler."""
    res = gpt.handler(
        content = "Give me three short rhyming words.",
        options = {"tokens": "20"}
    )

    assert res
    assert isinstance(res, str)
