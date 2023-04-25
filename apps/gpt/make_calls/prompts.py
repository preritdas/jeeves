"""Prompt the conversation."""
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from keys import KEYS


llm = ChatOpenAI(openai_api_key=KEYS["OpenAI"]["api_key"], model_name="gpt-4")


PREFIX_MESSAGE = (
    "You are a conversational AI. You receive a conversation "
    "between you and a recipient (whom you called) and complete it with your "
    "response, and ONLY YOUR OWN RESPONSE. DO NOT make up recipient responses. "
    "\n\nYour job is to facilitate a GOAL. Once you determine the GOAL "
    "has been achieved, you can end the conversation by responding with HANGUP. "
    "\n\n---------- Example: \n\n"
    "GOAL: Order a pizza to 1 Main Street, New York, NY.\n\nConversation:\n\n"
    "Recipient: Hello?\nAI: Hi, I'd like to order a pizza to 1 Main Street.\n"
    "Recipient: What kind of pizza?\nAI: Pepperoni.\nRecipient: What size?\n"
    "AI: Large.\nRecipient: What's your name?\nAI: John.\nRecipient: We'll "
    "get that to you in 30 minutes, John.\nAI: Thanks, bye.\nRecipient: Bye.\n"
    "AI: HANGUP\n\n----------\n\n"
    "GOAL: {goal}\n\nComplete the conversation below with only one response "
    "from you, the AI.\n\n{conversation}"
)

prompt_template = PromptTemplate(
    input_variables=["goal", "conversation"],
    template=PREFIX_MESSAGE,
)

conversation_chain = LLMChain(
    prompt=prompt_template,
    llm=llm
)


def generate_response(goal: str, convo: str) -> str:
    """Generate a response given the conversation history and the goal."""
    return conversation_chain.run(goal=goal, conversation=convo)
