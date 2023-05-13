"""Create message filterers."""
from abc import ABC, abstractmethod

import datetime as dt

from jeeves.agency.chat_history.models import Message


class BaseFilterer(ABC):
    """Base class for filterers."""

    @abstractmethod
    def filter_messages(self, messages: list[Message]) -> list[Message]:
        """
        Filter the messages. Input schema is the same as output schema. Order matters.
        """
        raise NotImplementedError


class DatetimeFilterer(BaseFilterer):
    """
    Filter messages by datetime.

    Takes a start and end datetime, and returns all messages that fall within
    that range.
    """

    def __init__(self, start: dt.datetime, end: dt.datetime) -> None:
        """Initialize the filterer."""
        # Valid parameters check
        assert isinstance(start, dt.datetime), "Start datetime must be a datetime."
        assert isinstance(end, dt.datetime), "End datetime must be a datetime."
        assert start <= end, "Start datetime must be before end datetime."

        self.start = start
        self.end = end

    def filter_messages(self, messages: list[Message]) -> list[Message]:
        """Filter messages by datetime."""
        return [
            message
            for message in messages
            if self.start <= message.datetime <= self.end
        ]


class RecencyFilterer(BaseFilterer):
    """
    Filter messages by recency.

    Takes `n_messages` and returns the `n_messages` most recent messages.
    """
    def __init__(self, n_messages: int) -> None:
        """Initialize the filterer."""
        self.n_messages = int(n_messages)

    def filter_messages(self, messages: list[Message]) -> list[Message]:
        """Filter messages by recency."""
        # Sort the messages by datetime, most recent last (formatting)
        messages = sorted(messages, key=lambda message: message.datetime)

        # If there are fewer messages than n_messages, return all messages
        if len(messages) < self.n_messages:
            return messages

        # Return the last n_messages
        return messages[-self.n_messages :]
