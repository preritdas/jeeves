"""Test user memory."""
from apps.gpt.user_memory import UserMemory, create_user_memory_tools


def test_adding_to_memory(temporary_user_memory):
    """Test adding to memory."""
    user_memory = UserMemory.from_user_phone(temporary_user_memory)
    user_memory.add_entry("My great grandfather's name is Bobbert.")
    assert any("Bobbert" in entry.content for entry in user_memory.entries)


def test_retrieving_from_memory(temporary_user_memory):
    """
    Test retrieving from memory. 
    Temporary user memory adds an entry saying I parked on level 2.
    """
    user_memory = UserMemory.from_user_phone(temporary_user_memory)
    assert "2" in user_memory.answer_question("Where did I park?")
