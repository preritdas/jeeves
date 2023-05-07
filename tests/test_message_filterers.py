"""Test chat history message filterers."""
from apps.gpt.chat_history.filter import RecencyFilterer
from apps.gpt.chat_history.models import Message


def test_recency_filterer():
    filterer = RecencyFilterer(n_messages=5)
