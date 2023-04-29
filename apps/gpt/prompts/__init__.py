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
            return '{' + str(key) + '}'


class Prompt:
    """A prompt for the agent. Allows for variable insertion."""
    def __init__(self, template: str, input_variables: dict[str, str] = None):
        self.template = template
        self.input_variables = input_variables

    def build_prompt(self) -> str:
        """Build the prompt using self.input_variables."""
        if self.input_variables is None:
            return self.template

        return PartialFormatter().format(self.template, **self.input_variables)


# ---- Build the prompts ----

current_dir = os.path.dirname(os.path.realpath(__file__))
prompt_path = lambda name: os.path.join(current_dir, f"{name}.txt")

# Variables for the prompts
current_datetime = lambda: dt.datetime.now(pytz.timezone("US/Eastern")).strftime(
    "%-I:%M%p on %A, %B %d, %Y"
)

PROMPT_INPUTS: dict[str, dict[str, Callable]] = {
    "prefix": {
        "current_datetime": current_datetime
    },
    "format_instructions": {},
    "suffix": {}
}


def _build_prompt(name: str) -> Prompt:
    """Build the prompt with the given name."""
    if name not in PROMPT_INPUTS:
        raise ValueError(f"Prompt name {name} not found.")

    if not os.path.exists(prompt_path(name)):
        raise FileNotFoundError(f"Prompt file {name}.txt not found.")

    with open(prompt_path(name), "r", encoding="utf-8") as f:
        template = f.read()

    input_dict: dict[str, Callable] = PROMPT_INPUTS[name]

    return Prompt(
        template=template,
        input_variables={var: input_dict[var]() for var in input_dict}
    )


def build_prompts() -> AgentPrompts:
    """Build the prompts inserting any variables necessary."""
    return AgentPrompts(
        prefix=_build_prompt("prefix").build_prompt(),
        format_instructions=_build_prompt("format_instructions").build_prompt(),
        suffix=_build_prompt("suffix").build_prompt()
    )
