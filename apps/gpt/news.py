"""Get the news by API."""
import requests
from pydantic import BaseModel, Field

from keys import KEYS


NEWS_ENDPOINT = "https://newsapi.org/v2"
AVAILABLE_CATEGORIES = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology",
]


class Articles(BaseModel):
    """Articles model."""

    articles: list[tuple[str, str, str | None]] = Field(..., title="Articles by URL, title, and content.")


def _headline_news(category: str) -> Articles:
    """Query directly and return URLs, titles, and contents."""
    res = requests.get(
        f"{NEWS_ENDPOINT}/top-headlines",
        params={"apiKey": KEYS["NewsAPI"]["api_key"], "country": "us", "category": category},
    )

    articles = res.json()["articles"]
    return Articles(
        articles=[(article["url"], article["title"], article["content"]) for article in articles[:7]]
    )


def get_headline_news(category: str) -> str:
    """Get the headline news."""
    category = category.strip().lower()
    
    if category not in AVAILABLE_CATEGORIES:
        return f"Invalid category. Category must be one of {AVAILABLE_CATEGORIES}."

    articles = _headline_news(category).articles
    article_strs = [f"{article[1]} - {article[2]} ({article[0]})\n" for article in articles] 
    return "\n".join(article_strs)
