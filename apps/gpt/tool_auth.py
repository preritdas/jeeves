"""Load tools depending on authorization."""
from langchain.agents import Tool
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.utilities.zapier import ZapierNLAWrapper
from langchain.agents.agent_toolkits import ZapierToolkit

from keys import KEYS

from . import retrieval


JSON_STRING_INPUT_INSTRUCTIONS = "Input must be a JSON string with the keys \"source\" and \"query\"."

no_auth_tools = [
    Tool(
        name="Google Search",
        func=GoogleSerperAPIWrapper(serper_api_key=KEYS["GoogleSerper"]["api_key"]).run,
        description="Useful for when you need to search Google."
    ),
    Tool(
        name="Website Answerer",
        func=retrieval.WebsiteAnswerer.answer_json_string,
        description=(
            "Useful for when you need to answer a question about the content on a website. "
            f"{JSON_STRING_INPUT_INSTRUCTIONS} \"source\" is the URL of the website."
        )
    )
]


def build_tools(inbound_phone: str) -> list[Tool]:
    """Build all authenticated tools given a phone number."""
    added_tools = []

    # Zapier
    if inbound_phone in KEYS["ZapierNLA"]:
        zapier_key = KEYS["ZapierNLA"][inbound_phone]
        zapier_wrapper = ZapierNLAWrapper(zapier_nla_api_key=zapier_key)
        zapier_toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier_wrapper)
        added_tools.extend(zapier_toolkit.get_tools())

    return no_auth_tools + added_tools
