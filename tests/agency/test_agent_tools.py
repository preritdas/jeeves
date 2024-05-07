"""Test agent tools."""
import pytest

import requests

from jeeves.utils import CHROME_REQUEST_HEADERS
from jeeves.agency.retrieval import WebsiteAnswerer, YouTubeAnswerer
from jeeves.agency.news import manual_headline_news
from jeeves.agency.tool_auth import NO_AUTH_TOOLS
from jeeves.agency.send_texts import create_text_message_tool
from jeeves.agency.movies import MoviesTool


def test_website_answerer():
    answer = WebsiteAnswerer.answer_json_string(
        """{"source": "https://example.com/", "query": "What is the domain for?"}"""
    )

    assert answer
    assert "Unfortunately cannot answer" not in answer


def test_youtube_answerer():
    video_link = "https://www.youtube.com/watch?v=fLeJJPxua3E"
    question = "What is the difference between Oprah and someone who's broke?"

    answer = YouTubeAnswerer.answer_json_string(
        f"""{{"source": "{video_link}", "query": "{question}"}}"""
    )

    assert answer
    assert "Unfortunately cannot answer" not in answer


@pytest.mark.skip
def test_youtube_parsers():
    video_link = "https://www.youtube.com/watch?v=d1KT39pDiY0&ab_channel=MattWalsh"
    content = requests.get(video_link, headers=CHROME_REQUEST_HEADERS).text

    assert YouTubeAnswerer._parse_video_title(content) == (
        "Paper Straws Confirmed To Be Worse Than Plastic Straws"
    )

    assert YouTubeAnswerer._parse_video_channel(content) == "Matt Walsh"


def test_headlines():
    headlines = manual_headline_news("business")

    assert headlines
    assert "Error getting headline news" not in headlines


def test_wolfram_alpha():
    # Find the Wolfram tool
    query_res = [tool for tool in NO_AUTH_TOOLS if "Wolfram" in tool.name]

    if not query_res:
        raise ValueError("Wolfram Alpha tool not found.")

    if len(query_res) > 1:
        raise ValueError("Multiple Wolfram Alpha tools found.")

    wolfram_tool = query_res[0]
    res = wolfram_tool.run("3^3")

    assert res
    assert "27" in res


def test_text_tool(mocker, default_options):
    mocker.patch("jeeves.agency.send_texts.texts.CONFIG.General.sandbox_mode", True)

    TextToolClass = create_text_message_tool(default_options["inbound_phone"])
    tool = TextToolClass()

    res = tool.run("""{"recipient_phone": "12223334455", "content": "Hello world!"}""")

    assert res
    assert isinstance(res, str)
    assert "fail" not in res.lower()


@pytest.mark.skip()
def test_movie_tool():
    """Currently the movie tool is not given to the agent."""
    tool = MoviesTool()

    assert "Tom Cruise" in tool.run("top gun")
