"""Retrieval mechanisms."""
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.question_answering import load_qa_chain

import requests
import deta

from bs4 import BeautifulSoup
import requests
import json
from abc import ABC, abstractmethod

import utils
from keys import KEYS


llm = ChatOpenAI(model_name="gpt-4", openai_api_key=KEYS.OpenAI.api_key, temperature=0)
embeddings = OpenAIEmbeddings(openai_api_key=KEYS.OpenAI.api_key)
N_DOCS = 5  # 10 for gpt-4, 5 for 3.5
splitter = TokenTextSplitter(
    encoding_name="cl100k_base", 
    chunk_size=300, 
    chunk_overlap=50
)


# Deta Base for caching conversions
deta_client = deta.Deta(KEYS.Deta.project_key)
conversions_db = deta_client.Base("conversions_cache")


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
            return "Unfortunately cannot answer questions on that particular website."


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

    def convert(self) -> str:
        """Convert YouTube video to text."""
        # First parse the video ID
        if "youtube" in self.source:
            video_id = self.source.split("?v=")[1]
        elif "youtu.be" in self.source:
            video_id = self.source.split("/")[-1]
        else:  # Assume it's just the video ID
            video_id = self.source

        # Check if the video has already been converted
        cached = conversions_db.fetch(
            query={"answerer": "YouTubeAnswerer", "video_id": video_id}
        )
        if cached.items:
            return cached.items[0]["transcription"]

        # Then get the transcript
        response = requests.post(
            f'{KEYS.Transcription.api_url}/youtube',
            json={"video_id": video_id}
        )

        if not response.ok:
            raise ConversionError(
                "YouTube", 
                video_id, 
                f"YouTube transcription failed: {response.content.decode()}"
            )

        # Cache the transcription
        conversions_db.put(
            {
                "answerer": "YouTubeAnswerer",
                "video_id": video_id,
                "transcription": response.json()["transcription"]
            }
        )

        return response.json()["transcription"]
