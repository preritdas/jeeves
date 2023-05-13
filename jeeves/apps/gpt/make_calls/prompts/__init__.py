"""Prompt the conversation."""
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import os
import datetime as dt
import pytz

from keys import KEYS


llm = ChatOpenAI(
    openai_api_key=KEYS.OpenAI.api_key, model_name="gpt-3.5-turbo", temperature=0
)


# ---- Read and build prompts ----

current_dir = os.path.dirname(os.path.realpath(__file__))
prompt_path = lambda name: os.path.join(current_dir, f"{name}.txt")

get_current_datetime = lambda: dt.datetime.now(pytz.timezone("US/Eastern")).strftime(
    "%-I:%M%p on %A, %B %d, %Y"
)

with open(prompt_path("prefix"), "r", encoding="utf-8") as f:
    PREFIX_MESSAGE = f.read()

with open(prompt_path("greeting"), "r", encoding="utf-8") as f:
    GREETING_MESSAGE = f.read()

prompt_template = PromptTemplate(
    input_variables=["goal", "recipient_desc", "conversation", "current_datetime"],
    template=PREFIX_MESSAGE,
)

conversation_chain = LLMChain(prompt=prompt_template, llm=llm)


# ---- Generate responses ----

def generate_response(goal: str, recipient_desc: str, convo: str) -> str:
    """
    Generate a response given the conversation history and the goal. Format the
    current date and time into the prompt.
    """
    return conversation_chain.run(
        goal=goal,
        recipient_desc=recipient_desc,
        conversation=convo,
        current_datetime=get_current_datetime()
    )


def generate_intro_message(goal: str, recipient_desc: str) -> str:
    """Generate the intro message."""
    prompt = PromptTemplate(
        input_variables=["goal", "recipient_desc"], template=GREETING_MESSAGE
    )

    intro_message_chain = LLMChain(prompt=prompt, llm=llm)

    message: str = intro_message_chain.run(goal=goal, recipient_desc=recipient_desc)
    return message
