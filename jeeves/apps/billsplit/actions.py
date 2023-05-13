"""User operations in the billsplit app."""
from jeeves.apps.billsplit import billsplit_db
from jeeves.apps.billsplit.billsplit_db import db


def _person_active(phone: str) -> bool:
    """Determines if a person is currently active in a session."""
    active_sessions = db.fetch({"Active": True}).items

    for session in active_sessions:
        if phone in session["People"]:
            return True

    return False


def query_phrase(phone: str) -> str:
    """
    If the phone is only involved in one active session, return the phrase.
    If they're in multiple or none, return an empty string.
    """
    active_sessions = db.fetch({"Active": True}).items
    appearances = [session for session in active_sessions if phone in session["People"]]

    if len(appearances) == 1:
        return appearances[0]["Phrase"]

    return ""


def create_session(sender: str, total: float, tip: float) -> str:
    """Create a session."""
    if _person_active(sender):
        return "It seems you are already part of an active session."

    session = billsplit_db.Session.new(sender, total, tip)
    return f"The session has been created. Share the phrase: {session.phrase}"


def status(phrase: str) -> str:
    """Get the status - how many people so far."""
    try:
        session = billsplit_db.Session.from_database(phrase)
    except billsplit_db.SessionNotFoundError:
        return "No session was found with that phrase."

    if session.active:
        active_phrase = "That session is active"
    else:
        active_phrase = "That session is inactive"

    return f"{active_phrase}. There are {session.person_count} so far."


def participate(sender: str, phrase: str, tip: float) -> str:
    """Participate - suggest tip."""
    try:
        session = billsplit_db.Session.from_database(phrase)
    except billsplit_db.SessionNotFoundError:
        return "No session was found with that phrase."

    session.log_person(sender, round(tip, 2))
    return f"You're in! {tip:.2f}% tip suggested."


def close(sender: str, phrase: str) -> str:
    """Close and finalize this session. Only the original creator can close."""
    try:
        session = billsplit_db.Session.from_database(phrase)
    except billsplit_db.SessionNotFoundError:
        return "No session was found with that phrase."

    if not sender == session.creator:
        return f"Only the session creator, {session.creator}, can close this session."

    session.finalize()
    return (
        f"The session is closed! Everyone, including you, "
        "should have received a notification."
    )
