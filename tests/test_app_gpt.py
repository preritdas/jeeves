"Test the GPT app."
# import pytest

from apps import gpt


# @pytest.mark.xfail
def test_handler(default_options):
    """Test the GPT applet handler."""
    # Use vanilla GPT
    default_options["agency"] = "no"

    res = gpt.handler(
        content = "Give me three short rhyming words.",
        options = default_options
    )

    assert res
    assert isinstance(res, str)
