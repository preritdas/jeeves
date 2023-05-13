"""Test chat history message filterers."""
import pytest

import datetime as dt
import pytz

from jeeves.config import CONFIG
from jeeves.apps.gpt.chat_history.filter import RecencyFilterer, DatetimeFilterer
from jeeves.apps.gpt.chat_history.models import Message


tz = pytz.timezone(CONFIG.General.default_timezone)

@pytest.fixture(scope="module")
def temporary_messages(default_inbound) -> list[Message]:
    """Return a list of temporary messages."""
    return [
        Message(
            datetime=dt.datetime(2021, 1, 1, 0, 0, 0, tzinfo=tz),
            inbound_phone=default_inbound["phone_number"],
            user_input="Hello",
            agent_response="Hi.",
        ),
        Message(
            datetime=dt.datetime(2021, 1, 2, 0, 0, 0, tzinfo=tz),
            inbound_phone=default_inbound["phone_number"],
            user_input="How are you?",
            agent_response="I'm good.",
        ),
        Message(
            datetime=dt.datetime(2021, 1, 3, 0, 0, 0, tzinfo=tz),
            inbound_phone=default_inbound["phone_number"],
            user_input="What's your name?",
            agent_response="My name is Bob.",
        ),
        Message(
            datetime=dt.datetime(2021, 1, 4, 0, 0, 0, tzinfo=tz),
            inbound_phone=default_inbound["phone_number"],
            user_input="What's your favorite color?",
            agent_response="My favorite color is blue.",
        ),
        Message(
            datetime=dt.datetime(2021, 1, 5, 0, 0, 0, tzinfo=tz),
            inbound_phone=default_inbound["phone_number"],
            user_input="What's your favorite food?",
            agent_response="My favorite food is pizza.",
        ),
        Message(
            datetime=dt.datetime(2021, 1, 6, 0, 0, 0, tzinfo=tz),
            inbound_phone=default_inbound["phone_number"],
            user_input="What's your favorite animal?",
            agent_response="My favorite animal is a dog.",
        )
    ]


# ---- Recency ----

def test_recency_filterer(temporary_messages):
    """
    Test the recency filterer. Make sure it returns the correct number of messages,
    and that the messages are sorted by datetime. Make sure the bookend messages are
    correct. Make sure the first message isn't in there.
    """
    filterer = RecencyFilterer(n_messages=5)
    filtered_messages = filterer.filter_messages(temporary_messages)

    # Make sure 5 sorted messages
    assert len(filtered_messages) == 5
    
    # Make sure the bookend messages are correct (last and 2nd for 5 messages)
    assert filtered_messages[-1].user_input == "What's your favorite animal?"
    assert filtered_messages[0].user_input == "How are you?"

    # The first message shouldn't be in there (6 messages)
    assert all(m.user_input != "Hello" for m in filtered_messages)

    # Make sure the messages are in chronological order
    assert filtered_messages == sorted(filtered_messages, key=lambda m: m.datetime)
    

# ---- Datetime ----

def test_datetime_filterer(temporary_messages):
    """
    Test the datetime filterer. Make sure it returns the correct messages that fall
    within the specified datetime range.
    """
    start_datetime = dt.datetime(2021, 1, 2, 0, 0, 0, tzinfo=tz)
    end_datetime = dt.datetime(2021, 1, 5, 0, 0, 0, tzinfo=tz)
    filterer = DatetimeFilterer(start=start_datetime, end=end_datetime)
    filtered_messages = filterer.filter_messages(temporary_messages)

    # Make sure 4 messages are within the specified range
    assert len(filtered_messages) == 4

    # Make sure the messages are in the specified range
    for message in filtered_messages:
        assert start_datetime <= message.datetime <= end_datetime

    # Make sure the bookend messages are correct (first and last in the range)
    assert filtered_messages[0].user_input == "How are you?"
    assert filtered_messages[-1].user_input == "What's your favorite food?"

    # Messages outside the specified range shouldn't be in the filtered messages
    assert all(m.user_input != "Hello" for m in filtered_messages)
    assert all(m.user_input != "What's your favorite animal?" for m in filtered_messages)


def test_datetime_filterer_empty_result(temporary_messages):
    """
    Test the datetime filterer when no messages fall within the specified datetime range.
    """
    start_datetime = dt.datetime(2021, 1, 10, 0, 0, 0, tzinfo=tz)
    end_datetime = dt.datetime(2021, 1, 12, 0, 0, 0, tzinfo=tz)
    filterer = DatetimeFilterer(start=start_datetime, end=end_datetime)
    filtered_messages = filterer.filter_messages(temporary_messages)

    # Make sure no messages are within the specified range
    assert len(filtered_messages) == 0
