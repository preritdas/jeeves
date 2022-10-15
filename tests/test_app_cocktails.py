"""Test the cocktails app."""
import app_cocktails


def test_handler():
    res = app_cocktails.handler("", {"inbound_phone": "12223334455"})

    # Assert the process succeeded
    assert "behold" in res.lower() and "enjoy" in res.lower()


def test_help():
    help_text = app_cocktails.handler(
        "", 
        {
            "inbound_phone": "12223334455",
            "help": "yes"
        }
    )

    assert "cocktail" in help_text.lower() and "drink" in help_text.lower()
