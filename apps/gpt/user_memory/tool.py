"""Create tools accessible to Jeeves."""
from langchain.tools import Tool

from apps.gpt.user_memory.database import UserMemory


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
            description=(
                "Store a piece of information in longterm memory. Do this even when "
                "not specifically instructed by me. Store anything I say that "
                "could be asked about later, for example, favorite colors, car model, "
                "parking location on a certain date, family relationships, etc. "
                "Store facts, opinions, preferences, etc. Store more than you think "
                "necessary - it is better to store too much than too little. "
                "Tool input is a string with the content you're storing, in "
                "first-person from my perspective, not yours. Ex. 'My favorite color "
                "is blue.' or 'I parked in the parking lot on May 5 2023.' "
                "This tool pairs with the 'Question User Memory' tool, which you can "
                "use to query the user memory."
            )
        ),
        Tool(
            name="Question User Memory",
            func=user_memory.answer_question,
            description=(
                "This tool is used to query the memory from the 'Store in User "
                "Longterm Memory' tool. Ask natural language questions to this tool "
                "and it will return the answer, if found in the longterm memory. "
                "Ex. 'What is my favorite color?' or 'Where did I park on May 5 2023?' "
                "Input is a string with the question, in first-person from my "
                "perspective, not yours."
            )
        )
    ]
