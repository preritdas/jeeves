"""Get the news by API."""
import requests
from pydantic import BaseModel, Field

from keys import KEYS
from apps.gpt import retrieval


NEWS_ENDPOINT = "https://newsapi.org/v2"
API_AVAILABLE_CATEGORIES = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology",
]
MANUAL_AVAILABLE_CATEGORIES = [
    "general",
    "business",
    "technology",
    "markets",
    "world",
    "politics"
]


class Articles(BaseModel):
    """Articles model."""

    articles: list[tuple[str, str, str | None]] = Field(..., title="Articles by URL, title, and content.")


def _headline_news(category: str) -> Articles:
    """Query directly and return URLs, titles, and contents."""
    res = requests.get(
        f"{NEWS_ENDPOINT}/top-headlines",
        params={"apiKey": KEYS.NewsAPI.api_key, "country": "us", "category": category},
    )

    articles = res.json()["articles"]
    return Articles(
        articles=[(article["url"], article["title"], article["content"]) for article in articles[:7]]
    )


def get_headline_news(category: str) -> str:
    """Get the headline news."""
    category = category.strip().lower()
    
    if category not in API_AVAILABLE_CATEGORIES:
        return f"Invalid category. Category must be one of {API_AVAILABLE_CATEGORIES}."

    articles = _headline_news(category).articles
    article_strs = [f"{article[1]} - {article[2]} ({article[0]})\n" for article in articles] 
    return "\n".join(article_strs)


## ---- Manual ----

def _manual_headline_news(category: str) -> str:
    """Manually get headline news by using a WebsiteAnswerer."""
    category = category.strip().lower()

    if category not in MANUAL_AVAILABLE_CATEGORIES:
        return (
            f"Invalid category. Category must be one of {MANUAL_AVAILABLE_CATEGORIES}."
        )

    suffix = "" if category == "general" else "news/" + category
    answerer = retrieval.WebsiteAnswerer(f"https://wsj.com/{suffix}")
    
    return answerer.answer(
        query=(
            f"The context is snippets from the WSJ {category} page. "
            "Extract a human-readable list of news stories."
        ),
        n_docs=20
    )


def manual_headline_news(category: str) -> str:
    """Manually get headline news, catch errors and return a string."""
    try:
        return _manual_headline_news(category)
    except Exception as e:
        return f"Error getting headline news: {e}"
