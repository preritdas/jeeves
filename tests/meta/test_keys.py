"""Test keys models."""

def test_keys_models():
    """Test that the keys models are valid."""
    # This will raise an exception if the models are invalid.
    from keys import KEYS
    assert KEYS
