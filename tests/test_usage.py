"""Test the actual usage module, not the usage app."""
import datetime as dt
import string
import random

import usage

# Fixtures
from . import temp_usage_logs


def test_log_use():
    TEST_APP_RANDOM = "".join(random.sample(string.ascii_letters, 10))

    key = usage.log_use(
        phone_number = "12223334455",
        app_name = TEST_APP_RANDOM,
        content = "Apples",
        options = {"setup": "whole foods"},
        time = dt.datetime.now()
    )
    
    # Try to find this item
    db_res = usage.usage_db.fetch(
        {
            "Phone": "12223334455",
            "App": TEST_APP_RANDOM
        }
    )

    assert len(db_res.items) == 1

    # Clean up - delete the entry
    usage.usage_db.delete(key)


def test_phone_to_name():
    assert usage._phone_to_name("12223334455") == "Git Pytest"
    assert usage._phone_to_name("11234567890") == "11234567890"


# ---- Usage summary

def test_usage_summary_string_date():
    """Test the generation of a string usage summary based on various inputs."""
    assert usage.usage_summary(dt.datetime.today().strftime(usage.DT_FORMAT_DATE))


def test_usage_summary_fake_log(temp_usage_logs):
    assert type(temp_usage_logs) is list
    assert "29" in usage.usage_summary()
