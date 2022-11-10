"""Test the billsplit app."""
import pytest

from apps import billsplit
from apps.billsplit.actions import billsplit_db


@pytest.fixture
def temporary_session(default_inbound):
    new_session = billsplit_db.Session.new(default_inbound["msisdn"], 100, 10)
    yield new_session.phrase
    billsplit_db.db.delete(new_session.key)


# ---- A few misc tests ----

def test_stringify_session_obj(temporary_session):
    session_query = billsplit_db.Session.from_database(temporary_session)

    assert "session" in str(session_query)


# ---- Full flow ----

def test_full_flow(mocker, default_options):
    """Test the full logic flow of a session playing out."""
    # Ensure no texts are actually sent in the process
    mocker.patch("apps.billsplit.billsplit_db.texts.config.General.SANDBOX_MODE", True)

    # Test creation
    default_options["action"] = "start"
    default_options["total"] = "100"

    res = billsplit.handler("13", default_options)
    assert "has been created" in res

    session_phrase = res[-11:]  # three three-letter words + two spaces

    # Test participation
    res = billsplit.handler("15", {"inbound_phone": "11234567890", "phrase": session_phrase})
    assert "you're in" in res.lower()

    # Test status
    res = billsplit.handler(session_phrase, {"inbound_phone": default_options["inbound_phone"], "action": "status"})
    assert "active" in res.lower()

    # Test status with no phrase provided (query)
    res = billsplit.handler("", {"inbound_phone": default_options["inbound_phone"], "action": "status"})
    assert "active" in res.lower()

    # Test closing not as the original creator
    res = billsplit.handler(
        session_phrase,
        {
            "inbound_phone": "11234567890",
            "action": "close"
        }
    )

    assert "Only the session creator" in res

    # Test closing
    res = billsplit.handler(session_phrase, {"inbound_phone": default_options["inbound_phone"], "action": "close"})
    assert "closed" in res
    assert "notification" in res

    # Test status on inactive session
    res = billsplit.handler(
        session_phrase,
        {
            "inbound_phone": default_options["inbound_phone"],
            "action": "status"
        }
    )

    assert "inactive" in res

    # Cleanup - delete the database entry
    session_key = billsplit_db.db.fetch({"Phrase": session_phrase}).items[0]["key"]
    billsplit_db.db.delete(session_key)


def test_close_no_phrase(mocker, default_options):
    # Ensure no texts are actually sent in the process
    mocker.patch("apps.billsplit.billsplit_db.texts.config.General.SANDBOX_MODE", True)

    # Create a session
    res = billsplit.handler(
        content = "15", 
        options = {
            **default_options,
            "action": "start", 
            "total": "100"
        }
    )

    phrase = res[-11:]

    # Close the session with no phrase
    res = billsplit.handler("", {**default_options, "action": "close"})
    assert "close" in res.lower()

    # Cleanup
    billsplit.actions.db.delete(
        billsplit.actions.db.fetch({"Phrase": phrase}).items[0]["key"]
    )


def test_close_no_phrase_multiple_sessions(default_options):
    """
    Ensure an error is reported to user if they are involved in
    multiple sessions but try to close a session with no phrase.
    """
    session_1 = billsplit.actions.billsplit_db.Session.new(
        sender = default_options["inbound_phone"],
        total = 95,
        tip = 12
    )

    session_2 = billsplit.actions.billsplit_db.Session.new(
        sender = default_options["inbound_phone"],
        total = 91,
        tip = 14
    )

    # Try closing a session without a key
    res = billsplit.handler(
        "", {**default_options, "action": "close"}
    )

    assert "provide the phrase" in res.lower()

    # Cleanup
    billsplit.actions.db.delete(session_1.key)
    billsplit.actions.db.delete(session_2.key)


# ---- Unique features ----

def test_handler(default_options):
    res = billsplit.handler("", default_options)
    assert res


def test_start_session_person_active(temporary_session, default_options):
    """The temporary_session fixture creates a session with the default number."""
    default_options["action"] = "start"
    default_options["total"] = "100"

    res = billsplit.handler("13", default_options)
    assert "It seems" in res


def test_closing(mocker, temporary_session, default_options):
    mocker.patch("apps.billsplit.billsplit_db.texts.config.General.SANDBOX_MODE", True)

    default_options["action"] = "close"

    res = billsplit.handler(temporary_session, default_options)
    assert "closed!" in res


def test_no_session_found_status(default_options):
    """
    Intentionally use a very long (invalid) phrase to prevent the minute chance that 
    a session does actually exist.
    """
    res = billsplit.handler(
        content = "albsdchasdcassdjlhca",
        options = {
            **default_options,
            "action": "status"
        }
    )

    assert "No session was found" in res


def test_no_session_found_participate(default_options):
    """
    Intentionally use a very long (invalid) phrase to prevent the minute chance that 
    a session does actually exist.
    """
    res = billsplit.handler(
        content = "15",
        options = {
            **default_options,
            "phrase": "albsdchasdcassdjlhca"
        }
    )

    assert "No session was found" in res


def test_no_session_found_close(default_options):
    """
    Intentionally use a very long (invalid) phrase to prevent the minute chance that 
    a session does actually exist.
    """
    res = billsplit.handler(
        content = "albsdchasdcassdjlhca",
        options = {
            **default_options,
            "action": "close"
        }
    )

    assert "No session was found" in res


def test_non_unique_phrase(mocker):
    """Mock the `_generate_phrase` function."""
    mocker.patch("apps.billsplit.actions.billsplit_db._generate_phrase", return_value="def not new")
    assert billsplit.actions.billsplit_db._generate_phrase() == "def not new"

    # Temporarily create that session
    original_session = billsplit.actions.billsplit_db.Session.new("00000000000", 100, 15)

    with pytest.raises(Exception):
        new_session = billsplit.actions.billsplit_db.Session.new("00000000000", 100, 15)

    billsplit.actions.db.delete(original_session.key)


def test_multiple_phrases_from_database():
    """
    Test error raised when creating a `Session` using `.from_database`
    when there already exists a session with that phrase.
    
    Note that this should never happen as phrase duplication is handled on the
    creation side.
    """
    session = billsplit.actions.billsplit_db.Session.new("00000000000", 100, 16)

    # Deploy a new session to the database with the same phrase
    dup_key = billsplit.actions.db.put(
        {
            "Active": False,
            "Creator": "00000000000",
            "People": {"00000000000": 14},
            "Phrase": session.phrase,
            "Total": 98
        }
    )["key"]

    with pytest.raises(Exception):
        billsplit.actions.billsplit_db.Session.from_database(session.phrase)

    # Cleanup
    assert session.key
    billsplit.actions.db.delete(session.key)
    billsplit.actions.db.delete(dup_key)

    for item in billsplit.actions.db.fetch(dict(Creator="00000000000")).items:
        billsplit.actions.db.delete(item["key"])


def test_key_from_non_deployed():
    session = billsplit.actions.billsplit_db.Session(
        phrase = "top gun dog",
        total = 100,
        creator = "00000000000",
        people = {"00000000000": 13},
        active = True
    )

    assert not session.key


# ---- Not enough information - handler errors ----

def test_start_with_no_total(default_options):
    default_options["action"] = "start"
    res = billsplit.handler("15", default_options)

    assert "You must supply a total" in res


def test_start_invalid_total(default_options):
    default_options["total"] = "notnumber"
    default_options["action"] = "start"
    res = billsplit.handler("15", default_options)

    assert "invalid" in res.lower()


def test_start_no_content(default_options):
    default_options["total"] = "100"
    default_options["action"] = "start"
    res = billsplit.handler("", default_options)

    assert "tip as content" in res.lower()


def test_start_invalid_tip(default_options):
    default_options["action"] = "start"
    default_options["total"] = "100"
    res = billsplit.handler("weird", default_options)

    assert "invalid tip" in res.lower()


def test_status_no_phrase(default_options):
    default_options["action"] = "status"
    res = billsplit.handler("", default_options)

    assert "must provide" in res.lower()
    assert "phrase" in res.lower()


def test_participate_invalid_tip(default_options, temporary_session):
    res = billsplit.handler(
        content = "weird", 
        options = {
            **default_options,
            "phrase": temporary_session
        }
    )

    assert "invalid tip" in res.lower()
