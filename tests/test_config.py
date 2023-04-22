"""Test config."""
import pytest

import config


@pytest.mark.skip  # skip as moved to yaml format
def test_invalid_bool():
    with pytest.raises(config.ConfigurationError):
        config.read_bool_option("asdfaskdlf")
