"""Database handling for the billsplit app."""
import deta

import string
import random

import keys
import texts


deta_client = deta.Deta(keys.Deta.PROJECT_KEY)
db = deta_client.Base("billsplit")

{
    "Phrase": "cat dog mouth",
    "Total": 98.23,
    "People": {
        "12223334455": 15  # suggested tip
    },
    "Active": True
}


class SessionNotFoundError(Exception):
    """If a session is queried by phrase but doesn't exist."""
    pass


class Session:
    """A bill splitting session."""
    def __init__(self, phrase: str, total: float, people: dict[str, float], active: bool) -> None:
        self.phrase = phrase
        self.total = float(total)
        self.people = people
        self.active = active

    @property
    def deployed(self) -> bool:
        """If the session is deployed to the database."""
        return len(db.fetch({"Phrase": self.phrase}).items) == 1

    @property
    def person_count(self) -> int:
        """The number of users logged thus far."""
        self._download()
        return len(self.people)

    @classmethod
    def new(cls, sender: str, total: float, tip: float) -> "Session":
        """Create a new session from scratch."""
        new_obj = cls(
            phrase = "".join(random.sample(string.ascii_lowercase, 5)),
            total = float(total),
            people = {sender: tip},
            active = True
        )

        new_obj.create()
        return new_obj

    def create(self) -> str:
        """
        Deploys the session to the database. Returns the unique key, not the phrase.
        If the session has already been deployed, an empty string is returned.
        """
        if self.deployed: return ""

        # Deploy session to database
        return db.put(
            {
                "Phrase": self.phrase,
                "Total": self.total,
                "People": self.people,
                "Active": self.active
            }
        )

    def _download(self) -> None:
        """Update the instance variables based on the database."""
        self = self.from_database(self.phrase)

    def _post(self) -> None:
        """Replace the database session with local attributes."""
        db.update(
            updates = {
                "Phrase": self.phrase,
                "Total": float(self.total),
                "People": self.people,
                "Active": self.active
            },
            key = self.key
        )

    @property
    def key(self) -> str:
        """Unique database key, *not the Phrase*."""
        if not self.deployed: return ""
        return db.fetch(dict(Phrase=self.phrase)).items[0]["key"]

    @classmethod
    def from_database(cls, phrase: str) -> "Session":
        """Create a `Session` object based on a phrase from the database."""
        db_query = db.fetch(dict(Phrase=phrase)).items

        if len(db_query) == 0:
            raise SessionNotFoundError(f"No session was found with the phrase {phrase}.")
        
        if len(db_query) > 1:
            raise Exception(
                "Multiple sessions found with the same phrase." 
                "This shoudl never be triggered. Check the database."
            )

        session = db_query[0]
        return cls(
            phrase = session["Phrase"],
            total = float(session["Total"]),
            people = session["People"],
            active = session["Active"]
        )

    def log_person(self, phone: str, tip: float) -> str:
        """Log a person's contribution."""
        self._download()
        self.people[phone] = float(tip)
        self._post()

    def finalize(self) -> None:
        """Terminate the session and inform everyone of their dues."""
        self._download()
        self.active = False

        final_tip = sum(self.people.values()) / len(self.people)
        final_total = self.total + (self.total * (final_tip / 100))
        individual_amount = final_total / len(self.people)

        for person in self.people:
            texts.send_message(f"You owe {individual_amount}.", person)

        self._post()

    def __str__(self) -> str:
        self._download()
        return f"This is a session with the phrase {self.phrase}, total {self.total}, " \
            f"and {self.person_count} people participating. {self.deployed = }."


def test_run():
    session = Session.new("14259023246", 100, 12)
    print(session)

    phrase = session.phrase

    query_session = Session.from_database(phrase)
    print(query_session)

    query_session.log_person("12223334455", 13.2)
    print(query_session)

    query_session.finalize()
    print(query_session)