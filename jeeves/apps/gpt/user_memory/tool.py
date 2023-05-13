"""Create storer and answerer tools accessible in tool auth."""
from langchain.tools import Tool

from apps.gpt.user_memory.database import UserMemory
from apps.gpt.user_memory.prompts import STORER_PROMPT, ANSWERER_PROMPT


def create_user_memory_tools(user_phone: str) -> list[Tool]:
    """
    Create tools for the user memory.

    Args:
        user_phone (str): User phone number.

    Returns:
        list[Tool]: List of two tools, one for storing and one for retrieving.
    """
    user_memory = UserMemory.from_user_phone(user_phone)

    return [
        Tool(
            name="Store in User Longterm Memory",
            func=user_memory.add_entry,
            description=STORER_PROMPT
        ),
        Tool(
            name="Question User Memory",
            func=user_memory.answer_question,
            description=ANSWERER_PROMPT
        )
    ]
