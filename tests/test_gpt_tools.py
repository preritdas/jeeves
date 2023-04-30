"""Test agent tools."""
from apps.gpt.retrieval import WebsiteAnswerer, YouTubeAnswerer
from apps.gpt.news import manual_headline_news
from apps.gpt.tool_auth import no_auth_tools


def test_website_answerer():
    answer = WebsiteAnswerer.answer_json_string(
        """{"source": "https://example.com/", "query": "What is the domain for?"}"""
    )

    assert answer
    assert "Unfortunately cannot answer" in answer


def test_youtube_answerer():
    video_link = "https://www.youtube.com/watch?v=fLeJJPxua3E"
    question = "What is the difference between Oprah and someone who's broke?"

    answer = YouTubeAnswerer.answer_json_string(
        f"""{{"source": "{video_link}", "query": "{question}"}}"""
    )

    assert answer
    assert "Unfortunately cannot answer" in answer 


def test_headlines():
    headlines = manual_headline_news("business")

    assert headlines
    assert not "Error getting headline news" in headlines


def test_wolfram_alpha():
    # Find the Wolfram tool
    query_res = [
        tool for tool in no_auth_tools if "Wolfram" in tool.name
    ]

    if not query_res:
        raise ValueError("Wolfram Alpha tool not found.")

    if len(query_res) > 1:
        raise ValueError("Multiple Wolfram Alpha tools found.")
    
    wolfram_tool = query_res[0]
    res = wolfram_tool.run("3^3")

    assert res
    assert "27" in res
