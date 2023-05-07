"""Test chat history message filterers."""
import pytest

import datetime as dt
import pytz

from config import CONFIG
from apps.gpt.chat_history.filter import RecencyFilterer
from apps.gpt.chat_history.models import Message


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


def test_recency_filterer(temporary_messages):
    filterer = RecencyFilterer(n_messages=5)
    filtered_messages = filterer.filter_messages(temporary_messages)

    assert len(filtered_messages) == 5
    assert filtered_messages[0].user_input == "What's your favorite animal?"