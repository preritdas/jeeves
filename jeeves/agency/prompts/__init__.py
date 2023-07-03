"""
Build and serve the agent prompts.

This is in a module because the prompts are long, comprehensive, and may contain
variable information, such as the current date and time. This module will read the
prompts and format in the variables. 

Note that these variables are 'indicated' in the prompt files just as agent variables
are, with curly braces. Nonetheless, those variables that need to be formatted in 
according to this module are done so here, before the strings, with remaining variables
(for the agent) are sent to the agent.
"""
from pydantic import BaseModel

from typing import Callable
import string
import os

import datetime as dt
import pytz

from jeeves.permissions import User
from jeeves.agency.chat_history import ChatHistory
from jeeves.agency.chat_history import TokenCountFilterer


# ---- Model for prompting ----

class AgentPrompts(BaseModel):
    """The various prompt components for the agent."""
    prefix: str
    format_instructions: str
    suffix: str


class PartialFormatter(string.Formatter):
    """
    A custom string formatter that allows partial substitution of variables in a string template.
    If a variable is not provided, it leaves the placeholder unchanged.

    Example:
        template = "Hello, {something} and {else}."
        formatter = PartialFormatter()
        formatted = formatter.format(template, something="world")
        print(formatted)  # Output: "Hello, world and {else}."
    """

    def get_value(self, key: str | int, args: tuple, kwargs: dict[str, str]) -> str:
        """
        Get the value of a variable from the given args or kwargs.
        If the variable is not found, return the key enclosed in curly braces.

        Args:
            key (str | int): The variable key, either a string or an index.
            args (tuple[Any]): Positional arguments passed to the `format` method.
            kwargs (dict[str, Any]): Keyword arguments passed to the `format` method.

        Returns:
            str: The value of the variable, or the unchanged placeholder if the variable is not found.
        """
        try:
            return super(PartialFormatter, self).get_value(key, args, kwargs)
        except KeyError:
            return "{" + str(key) + "}"


class Prompt:
    """A prompt for the agent. Allows for variable insertion."""
    def __init__(self, template: str, input_variables: dict[str, str] = None):
        self.template = template
        self.input_variables = input_variables

    def build_prompt(self, **kwargs) -> str:
        """Build the prompt using self.input_variables."""
        if self.input_variables is None:
            return self.template

        # Update the input variables with the given kwargs
        input_variables = self.input_variables.copy()
        input_variables.update(kwargs)

        return PartialFormatter().format(self.template, **input_variables)


# ---- Build the prompts ----

current_dir = os.path.dirname(os.path.realpath(__file__))
prompt_path = lambda name: os.path.join(current_dir, f"{name}.txt")

# The reason these are stored in this Callable fashion is so the values are only
# evaluated when the prompt is built. This is because the values may change over time,
# ex. the date and time.


def get_current_datetime(tz_str: str):
    timezone = pytz.timezone(tz_str)
    format_str = "%-I:%M%p on %A, %B %d, %Y"
    return dt.datetime.now(timezone).strftime(format_str)


def build_prompt_inputs(user: User) -> dict[str, dict[str, Callable]]:
    """Build the prompt inputs dictionary."""
    assert user

    return {
        "prefix": {
            "current_datetime": lambda: get_current_datetime(user.timezone),
            "timezone": lambda: user.timezone,
            "my_name": lambda: user.name,
            "address_me": lambda: "sir" if user.gender_male else "ma'am"
        },
        "format_instructions": {},
        "suffix": {}
    }


def _build_prompt(name: str, prompt_inputs: dict[str, dict[str, Callable]], **kwargs) -> Prompt:
    """Build the prompt with the given name. Pass in any inputs as kwargs."""
    if name not in prompt_inputs:
        raise ValueError(f"Prompt name {name} not found.")

    if not os.path.exists(prompt_path(name)):
        raise FileNotFoundError(f"Prompt file {name}.txt not found.")

    with open(prompt_path(name), "r", encoding="utf-8") as f:
        template = f.read()

    # Input dictionary will evaluate the functions in PROMPT_INPUTS[name]
    input_dict: dict[str, str] = {
        var: prompt_inputs[name][var]() for var in prompt_inputs[name]
    }

    # Add any kwargs to the input dictionary
    input_dict.update(kwargs)

    return Prompt(template=template, input_variables=input_dict)


def build_prompts(user: User) -> AgentPrompts:
    """Build the prompts inserting any variables necessary."""
    chat_history = ChatHistory.from_inbound_phone(user.phone).format_messages(
        filterer=TokenCountFilterer()
    )
    prompt_inputs = build_prompt_inputs(user)

    return AgentPrompts(
        prefix=_build_prompt("prefix", prompt_inputs).build_prompt(),
        format_instructions=_build_prompt("format_instructions", prompt_inputs).build_prompt(),
        suffix=_build_prompt("suffix", prompt_inputs).build_prompt(chat_history=chat_history)
    )


def build_base_agent_prompts() -> AgentPrompts:
    """
    Build prompts for an agent that has no User.
    """
    BASE_AGENT_INPUTS = {
        "prefix": {
            "my_name": lambda: "a generic user",
            "address_me": lambda: "sir",
            "timezone": lambda: "EST",
            "current_datetime": lambda: get_current_datetime("EST")
        },
        "format_instructions": {},
        "suffix": {}
    }

    SUFFIX: str = "Begin!\n\nInput: {input}\n{agent_scratchpad}"

    return AgentPrompts(
        prefix=_build_prompt("prefix", BASE_AGENT_INPUTS).build_prompt(),
        format_instructions=_build_prompt("format_instructions", BASE_AGENT_INPUTS).build_prompt(),
        suffix=SUFFIX
    )
