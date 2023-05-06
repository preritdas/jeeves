"""
Long term memory tool. Jeeves decides when to store items, 
then uses the tool to retrieve items to get more information.
"""
from deta import Deta

from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

import datetime as dt

from keys import KEYS
from parsing import validate_phone_number
from apps.gpt.user_memory.models import Entry


# Memory database
memory_db = Deta(KEYS.Deta.project_key).Base("user_memory")


# Question answering stuff
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=KEYS.OpenAI.api_key, temperature=0)
embeddings = OpenAIEmbeddings(openai_api_key=KEYS.OpenAI.api_key)
splitter = TokenTextSplitter(
    encoding_name="cl100k_base", chunk_size=300, chunk_overlap=50
)


class UserMemory:
    def __init__(self, user_phone: str, entries: list[Entry]):
        self.entries = entries
        self.user_phone = validate_phone_number(user_phone)

    @classmethod
    def from_user_phone(cls, user_phone: str) -> None:
        """Get all entries from a user."""
        entries = memory_db.fetch({"user_phone": validate_phone_number(user_phone)}).items
        return cls(user_phone=user_phone, entries=[Entry(**entry) for entry in entries])

    def add_entry(self, content: str) -> None:
        """Add an entry to the user's memory."""
        entry = Entry(
            datetime=dt.datetime.now(),
            user_phone=self.user_phone,
            content=content
        )

        memory_db.put(entry.to_dict())
        return

    def answer_question(self, question: str) -> str:
        """
        First converts the initial source, then queries it. The query must be a string,
        and the answer will be a string. This does not work with the string-in-string-out
        nature of an LLM agent, so it is not exposed to the user.
        """
        docs = [Document(page_content=entry.content) for entry in self.entries]
        vectorstore = FAISS.from_documents(docs, embeddings)

        _find_similar = lambda k: vectorstore.similarity_search(question, k=k)
        similar_docs = _find_similar(15)

        # Adjust the instructions based on the source
        PREFIX = (
            "You are a User Memory Answerer. Your context is notes from "
            "someone's memory. Use the user's memory, nothing else, to "
            "answer the question."
        )
        qa_chain = load_qa_chain(llm)
        qa_chain.llm_chain.prompt.messages[0].prompt.template = (
            PREFIX + qa_chain.llm_chain.prompt.messages[0].prompt.template
        )

        return qa_chain.run(input_documents=similar_docs, question=question)
