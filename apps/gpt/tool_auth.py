"""Load tools depending on authorization."""
from langchain.agents import Tool
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.utilities.zapier import ZapierNLAWrapper
from langchain.agents.agent_toolkits import ZapierToolkit

from keys import KEYS

from apps.gpt import retrieval
from apps.gpt import news
from apps.gpt import send_texts
from apps.gpt import make_calls


class GoogleSerperAPIWrapperURL(GoogleSerperAPIWrapper):
    """Same as the GoogleSerperAPIWrapper but provides URLs to results."""
    def _parse_results(self, results: dict) -> str:
        snippets = []

        if results.get("answerBox"):
            answer_box = results.get("answerBox", {})
            if answer_box.get("answer"):
                return answer_box.get("answer")
            elif answer_box.get("snippet"):
                return answer_box.get("snippet").replace("\n", " ")
            elif answer_box.get("snippetHighlighted"):
                return ", ".join(answer_box.get("snippetHighlighted"))

        if results.get("knowledgeGraph"):
            kg = results.get("knowledgeGraph", {})
            title = kg.get("title")
            entity_type = kg.get("type")
            if entity_type:
                snippets.append(f"{title}: {entity_type}.")
            description = kg.get("description")
            if description:
                snippets.append(description)
            for attribute, value in kg.get("attributes", {}).items():
                snippets.append(f"{title} {attribute}: {value}.")

        for result in results["organic"][: self.k]:
            if "snippet" in result:
                snippets.append(f"{result['snippet']} ({result['link']})")
            for attribute, value in result.get("attributes", {}).items():
                snippets.append(f"{attribute}: {value}.")

        if len(snippets) == 0:
            return "No good Google Search Result was found"

        return " ".join(snippets)


ANSWERER_JSON_STRING_INPUT_INSTRUCTIONS = (
    "Input must be a JSON string with the keys \"source\" and \"query\"."
)

no_auth_tools = [
    Tool(
        name="Google Search",
        func=GoogleSerperAPIWrapperURL(serper_api_key=KEYS.GoogleSerper.api_key).run,
        description=(
            "Useful for when you need to search Google. Provides links to search results "
            "that you can use Website Answerer to answer for more information."
        )
    ),
    Tool(
        name="Website Answerer",
        func=retrieval.WebsiteAnswerer.answer_json_string,
        description=(
            "Useful for when you need to answer a question about the content on a website. "
            "You can use this to answer questions about links found in Google Search results. "
            f"{ANSWERER_JSON_STRING_INPUT_INSTRUCTIONS} \"source\" is the URL of the website. "
            "Do not make up websites to search - you can use Google Search to find relevant urls."
        )
    ),
    Tool(
        name="YouTube Answerer",
        func=retrieval.YouTubeAnswerer.answer_json_string,
        description=(
            "Useful for when you need to answer a question about the contents of a YouTube video. "
            f"{ANSWERER_JSON_STRING_INPUT_INSTRUCTIONS} \"source\" is the URL of the YouTube video. "
            "Do not make up YouTube videos - you can use Google Search to find relevant videos, or "
            "accept them directly from the user."
        )
    ),
    Tool(
        name="Headline News",
        func=news.manual_headline_news,
        description=(
            "Useful for when you need to get the top headlines from a specific category. "
            "Input must be a string with the category name. Category must be one of "
            f"{news.MANUAL_AVAILABLE_CATEGORIES}."
        )
    ),
    Tool(
        name="Wolfram Alpha",
        func=WolframAlphaAPIWrapper(wolfram_alpha_appid=KEYS.WolframAlpha.app_id).run,
        description=(
            "Useful for when you need to do math or anything quantitative/computational. "
            "Input should ideally be math expressions, ex. \"8^3\", but can also be "
            "natural language if a math expression is not possible."
        )
    ),
    make_calls.CallTool(),
]


def build_tools(inbound_phone: str) -> list[Tool]:
    """Build all authenticated tools given a phone number."""
    added_tools = []

    # Zapier
    if inbound_phone in KEYS.ZapierNLA:
        zapier_key = KEYS.ZapierNLA[inbound_phone]
        zapier_wrapper = ZapierNLAWrapper(zapier_nla_api_key=zapier_key)
        zapier_toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier_wrapper)
        added_tools.extend(zapier_toolkit.get_tools())

    # Text messages
    TextToolClass = send_texts.create_text_message_tool(inbound_phone)
    added_tools.append(TextToolClass())

    return no_auth_tools + added_tools
