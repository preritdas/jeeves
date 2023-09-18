"""Retrieval mechanisms."""
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.question_answering import load_qa_chain

import requests
from pymongo import MongoClient

from bs4 import BeautifulSoup
import requests
import json
from abc import ABC, abstractmethod

from jeeves import utils
from keys import KEYS


llm = ChatOpenAI(model_name="gpt-4", openai_api_key=KEYS.OpenAI.api_key, temperature=0)
embeddings = OpenAIEmbeddings(openai_api_key=KEYS.OpenAI.api_key)
N_DOCS = 10  # 10 for gpt-4, 5 for 3.5
splitter = TokenTextSplitter(
    encoding_name="cl100k_base", chunk_size=300, chunk_overlap=50
)


# Deta Base for caching conversions
CONVERSIONS_COLL = MongoClient(KEYS.MongoDB.connect_str)["Jeeves"]["conversions_cache"]


class ConversionError(Exception):
    """Raised when a conversion fails."""
    def __init__(self, answerer_name: str, source: str, error: str) -> None:
        super().__init__(
            f"Could not convert {answerer_name} source {source}. Error {error}."
        )


class BaseAnswerer(ABC):
    """Abstract base class for answerers."""

    def __init__(self, source: str):
        self.source = source

    @abstractmethod
    def convert(self) -> str:
        """
        Converts `self.source` into a string. If the input is text already, return input.
        If it's a website, scrape the website and return the text. Etc. The input should
        be providable in string form so a GPT agent can use it.

        Ex. text can be passed as a string, website can be passed as a URL, etc.
        """

    def answer(self, query: str, n_docs: int = N_DOCS) -> str:
        """
        First converts the initial source, then queries it. The query must be a string,
        and the answer will be a string. This does not work with the string-in-string-out
        nature of an LLM agent, so it is not exposed to the user.
        """
        text = self.convert()
        docs = splitter.create_documents([text])
        vectorstore = FAISS.from_documents(docs, embeddings)

        _find_similar = lambda k: vectorstore.similarity_search(query, k=k)
        similar_docs = _find_similar(n_docs)

        # Adjust the instructions based on the source
        PREFIX = (
            f"You are a {type(self).__name__}. Your context is snippets from the "
            f"transcription of your source as a {type(self).__name__}. "
        )
        qa_chain = load_qa_chain(llm)
        qa_chain.llm_chain.prompt.messages[0].prompt.template = (
            PREFIX + qa_chain.llm_chain.prompt.messages[0].prompt.template
        )

        return qa_chain.run(input_documents=similar_docs, question=query)

    @classmethod
    def answer_json_string(cls, agent_input: str) -> str:
        """
        Parses the agent input and returns the answer. This is the function that the
        agent will call. The agent input must be a string, and the answer will be a string.
        Parses with JSON. Agent must provide a JSON string with two keys: "source" and "query".

        Eventually, add some JSON parsing to allow for slightly-off inputs.
        """
        dic = json.loads(agent_input)

        # Return the answer or an error
        try:
            return cls(dic["source"]).answer(dic["query"])
        except Exception:
            return "Unfortunately cannot answer questions using that particular source."


class TextAnswerer(BaseAnswerer):
    """Answerer for text."""

    def convert(self) -> str:
        return self.source


class WebsiteAnswerer(BaseAnswerer):
    """Answerer for websites."""

    def convert(self) -> str:
        """Convert website to text."""
        response = requests.get(self.source, headers=utils.REQUEST_HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        for script in soup(["script", "style"]):
            script.decompose()

        return " ".join(string for string in soup.stripped_strings)


class YouTubeAnswerer(BaseAnswerer):
    """Answerer for YouTube videos."""

    @staticmethod
    def _video_source_to_url(video_source: str) -> str:
        """Convert a YouTube video ID to a URL."""
        if "youtube" in video_source:
            return video_source.split("?v=")[1]
        elif "youtu.be" in video_source:
            return video_source.split("/")[-1]
        elif len(video_source) == 11:  # Assume it's just the video ID
            return video_source

        raise ValueError(f"Could not parse YouTube video source {video_source}.")

    @staticmethod
    def _video_title(video_url: str) -> str:
        """
        Get the title of a YouTube video.

        Args:
            video_url: URL of the YouTube video.

        Returns:
            (str) The title of the video.
        """

    @staticmethod
    def _parse_video_title(html_content: str) -> str:
        """
        Parse the title of a YouTube video from the HTML.
        Returns an empty string if the title cannot be found.
        """
        title_start = html_content.find("only screen and (max")

        if title_start == -1:
            return ""

        title_start += 92  # link and other stuff, advance to title
        title_end = html_content[title_start:].find("</title")
        title = html_content[title_start : title_start + title_end]

        # Remove the " - YouTube" suffix
        if title.endswith(" - YouTube"):
            title = title[:-10]

        return title

    @staticmethod
    def _parse_video_channel(html_content: str) -> str:
        """
        Parse the channel of a YouTube video from the HTML.
        Returns an empty string if the channel cannot be found.
        """
        search_str = 'link itemprop="name" content="'
        channel_start = html_content.find(search_str)
        channel_start += len(search_str)

        if channel_start == -1:
            return ""

        return html_content[channel_start:].split('"')[0]

    def convert(self) -> str:
        """Convert YouTube video to text."""
        # First parse the video ID
        video_id = self._video_source_to_url(self.source)

        # Check if the video has already been converted
        cache_res = CONVERSIONS_COLL.find_one(
            {"answerer": "YouTubeAnswerer", "video_id": video_id}
        )
        if cache_res:
            return cache_res["transcription"]

        # Then get the transcript
        response = requests.post(
            f"{KEYS.Transcription.api_url}/youtube", json={"video_id": video_id}
        )

        if not response.ok:
            raise ConversionError(
                "YouTube",
                video_id,
                f"YouTube transcription failed: {response.content.decode()}"
            )

        # Get the transcription
        transcription = response.json()["transcription"]

        # Insert title and source into the transcription
        html_content = requests.get(self.source, headers=utils.CHROME_REQUEST_HEADERS).text
        title = self._parse_video_title(html_content)
        channel = self._parse_video_channel(html_content)
        
        if title:
            transcription = f"Title: {title}\n\n" + transcription
        if channel:
            transcription = f"Channel: {channel}\n\n" + transcription

        # Cache the transcription
        CONVERSIONS_COLL.insert_one(
            {
                "answerer": "YouTubeAnswerer",
                "video_id": video_id,
                "transcription": transcription
            }
        )

        return transcription
