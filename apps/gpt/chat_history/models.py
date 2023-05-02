"""Models for chat history."""
from pydantic import BaseModel

import datetime as dt


class Message(BaseModel):
    """
    A Message is both the user input and the agent response.
    
    Attributes:
        datetime: The datetime of the message. 
        user_input: The user input.
        agent_response: The agent response.
    """
    datetime: dt.datetime
    user_input: str
    agent_response: str
