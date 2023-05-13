"""Read in tool prompts."""
import os


current_dir = os.path.realpath(os.path.dirname(__file__))
prompt_path = lambda x: os.path.join(current_dir, f"{x}.txt")


# ---- Read in prompts ----

def _storer_prompt() -> str:
    """Read in the storer prompt."""
    with open(prompt_path("store"), "r", encoding="utf-8") as f:
        return f.read()


def _answerer_prompt() -> str:
    """Read in the answerer prompt."""
    with open(prompt_path("answer"), "r", encoding="utf-8") as f:
        return f.read()


STORER_PROMPT: str = _storer_prompt()
ANSWERER_PROMPT: str = _answerer_prompt()
