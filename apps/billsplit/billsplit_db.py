"""Database handling for the billsplit app."""
import deta
import requests

import random

from keys import KEYS
import texts


deta_client = deta.Deta(KEYS.Deta.project_key)
db = deta_client.Base("billsplit")


class SessionNotFoundError(Exception):
    """If a session is queried by phrase but doesn't exist."""
    pass


def _generate_phrase():
    response = requests.get("https://www.mit.edu/~ecprice/wordlist.10000")
    words = [
        word.decode("ascii") for word in response.content.splitlines() if len(word) == 3
    ]
    return " ".join(random.sample(words, 3))


class Session:
    """A bill splitting session."""

    def __init__(
        self,
        phrase: str,
        total: float,
        creator: str,
        people: dict[str, float],
        active: bool
    ) -> None:
        self.phrase = phrase
        self.total = float(total)
        self.creator = creator
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
        phrase = _generate_phrase()

        attempts = 0
        while len(db.fetch({"Phrase": phrase}).items) != 0:
            phrase = _generate_phrase()
            attempts += 1

            if attempts > 20:
                raise Exception("20 attempts were made to generate a unique phrase.")

        new_obj = cls(
            phrase=phrase,
            total=float(total),
            creator=sender,
            people={sender: tip},
            active=True
        )

        new_obj.create(creator_phone=sender)
        return new_obj

    def create(self, creator_phone: str) -> str:
        """
        Deploys the session to the database. Returns the unique key, not the phrase.
        If the session has already been deployed, an empty string is returned.
        """
        if self.deployed:
            return ""

        # Deploy session to database
        return db.put(
            {
                "Phrase": self.phrase,
                "Total": self.total,
                "Creator": str(creator_phone),
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
            updates={
                "Phrase": self.phrase,
                "Total": float(self.total),
                "People": self.people,
                "Active": self.active
            },
            key=self.key
        )

    @property
    def key(self) -> str:
        """Unique database key, *not the Phrase*."""
        if not (fetch_res := db.fetch(dict(Phrase=self.phrase)).items):
            return ""

        return fetch_res[0]["key"]

    @classmethod
    def from_database(cls, phrase: str) -> "Session":
        """Create a `Session` object based on a phrase from the database."""
        # Cleanup the phrase - whitespace in between words
        phrase = " ".join(word.strip() for word in phrase.strip().split(" ") if word)

        # Search for items with that phrase (ideally only 1)
        db_query = db.fetch(dict(Phrase=phrase)).items

        if len(db_query) == 0:
            raise SessionNotFoundError(
                f"No session was found with the phrase {phrase}."
            )

        if len(db_query) > 1:
            raise Exception(
                "Multiple sessions found with the same phrase."
                "This should never be triggered. Check the database."
            )

        session = db_query[0]
        return cls(
            phrase=session["Phrase"],
            total=float(session["Total"]),
            creator=session["Creator"],
            people=session["People"],
            active=session["Active"]
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

        message = (
            f"The tab is closed, with an average tip of {final_tip:.2f}%. "
            f"Your portion is ${individual_amount:.2f}."
        )

        for person in self.people:
            texts.send_message(message, person)

        self._post()

    def __str__(self) -> str:
        self._download()
        return (
            f"This is a session with the phrase {self.phrase}, total {self.total}, "
            f"and {self.person_count} people participating. {self.deployed = }."
        )
