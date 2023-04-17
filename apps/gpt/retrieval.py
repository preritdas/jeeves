"""Retrieval mechanisms."""
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.question_answering import load_qa_chain

from bs4 import BeautifulSoup
import requests

from abc import ABC, abstractmethod

import keys


llm = ChatOpenAI(model_name="gpt-4", openai_api_key=keys.OpenAI.API_KEY, temperature=0)
embeddings = OpenAIEmbeddings(openai_api_key=keys.OpenAI.API_KEY)
splitter = TokenTextSplitter(
    encoding_name="cl100k_base", 
    chunk_size=300, 
    chunk_overlap=50
)
qa_chain = load_qa_chain(llm)


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

    def answer(self, query: str) -> str:
        """
        First converts the initial source, then queries it. The query must be a string, 
        and the answer will be a string, to comply with the string-in-string-out nature
        of an LLM agent.
        """
        text = self.convert()
        docs = splitter.create_documents([text])
        vectorstore = FAISS.from_documents(docs, embeddings)

        _find_similar = lambda k: vectorstore.similarity_search(query, k=k)
        similar_docs = _find_similar(10)

        return qa_chain.run(input_documents=similar_docs, question=query)


class TextAnswerer(BaseAnswerer):
    """Answerer for text."""

    def convert(self) -> str:
        return self.source


class WebsiteAnswerer(BaseAnswerer):
    """Answerer for websites."""

    def convert(self) -> str:
        """Convert website to text."""
        response_content = requests.get(self.source).content
        soup = BeautifulSoup(response_content, "html.parser")

        for script in soup(["script", "style"]):
            script.decompose()

        return " ".join(string for string in soup.stripped_strings)
