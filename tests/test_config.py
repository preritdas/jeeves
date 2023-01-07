"""Test config."""
import pytest

import config


def test_invalid_bool():
    with pytest.raises(config.ConfigurationError):
        config.read_bool_option("asdfaskdlf")
