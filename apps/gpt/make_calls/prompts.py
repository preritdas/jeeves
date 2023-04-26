"""Prompt the conversation."""
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from keys import KEYS


llm = ChatOpenAI(openai_api_key=KEYS["OpenAI"]["api_key"], model_name="gpt-4", temperature=0)


PREFIX_MESSAGE = (
    "You are Jeeves, a conversational AI. You receive a conversation "
    "between you and a recipient (whom you called) and complete it with your "
    "response, and ONLY YOUR OWN RESPONSE. DO NOT make up recipient responses. "
    "\n\nYour job is to facilitate a GOAL. Once you determine the GOAL "
    "has been achieved, you can end the conversation by responding with HANGUP. "
    "When in a call, strictly stick to the topic at hand. If the recipient tries "
    "to veer off topic, refuse to answer and guide them back into the topic at hand."
    "\n\n---------- Example: \n\n"
    "GOAL: Order a pizza to 1 Main Street, New York, NY.\n\nConversation:\n\n"
    "Recipient: Hello?\nJeeves: Hi, I'd like to order a pizza to 1 Main Street.\n"
    "Recipient: What kind of pizza?\nJeeves: Pepperoni.\nRecipient: What size?\n"
    "Jeeves: Large.\nRecipient: What's your name?\nJeeves: John.\nRecipient: We'll "
    "get that to you in 30 minutes, John.\nJeeves: Thanks, bye.\nRecipient: Bye.\n"
    "Jeeves: HANGUP\n\n----------\n\n"
    "GOAL: {goal}\n\nComplete the conversation below with only one response "
    "from you, Jeeves.\n\n{conversation}"
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


def generate_intro_message(goal: str) -> str:
    """Generate the intro message."""
    prompt = PromptTemplate(
        input_variables=["goal"],
        template=(
            "You are Jeeves, a personal AI that calls people over the phone. "
            "Given a goal, create a sentence greeting somebody and informing "
            "them of your goal with them. \n\n-------- Example: \n\n"
            "Goal: Order a pizza to 1 Main Street, New York, NY.\n"
            "Your greeting: Hi, I'm Jeeves. I'm calling to "
            "order a pizza, please.\n\n--------\n\nGoal: {goal}\n"
            "Greeting: "
        )
    )

    intro_message_chain = LLMChain(
        prompt=prompt,
        llm=llm
    )

    message: str = intro_message_chain.run(goal=goal)

    # Add some instructions
    INSTRUCTIONS = (
        "I'm an experimental AI, so please bare with me. We'll take turns speaking, "
        "let's not interrupt eachother."
    )

    return message + " " + INSTRUCTIONS
