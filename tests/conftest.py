"""Fixtures etc."""
import pytest
from bson.objectid import ObjectId

import datetime as dt
import pytz
import string
import random

from jeeves.config import CONFIG
from jeeves import usage  # fixture for temporary logs for report
from jeeves.permissions.database import PERMISSIONS_COLL  # fixtures for temporary users

from jeeves.agency.make_calls.database import Call
from jeeves.agency.logs_callback import create_callback_handlers
from jeeves.agency.user_memory.database import UserMemory


@pytest.fixture(scope="session")
def default_inbound() -> dict[str, str]:
    random_inbound = "".join(
        [str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) for _ in range(10)]
    )

    # Add US country code
    random_inbound = "1" + random_inbound

    return {
        "phone_number": random_inbound,
        "body": "app: apps",
    }


@pytest.fixture
def default_options(default_inbound) -> dict[str, str]:
    return {"inbound_phone": default_inbound["phone_number"]}


@pytest.fixture(scope="session")
def temporary_user(default_inbound) -> dict[str, str]:
    """Temporary random user with maximum permissions."""
    first_name = "".join(random.sample(string.ascii_lowercase, 5)).title()
    last_name = "".join(random.sample(string.ascii_lowercase, 5)).title()

    user_attrs = {
        "Name": f"{first_name} {last_name}",
        "Phone": default_inbound["phone_number"],
        "Timezone": "EST",
        "UseApplets": True,
        "GenderMale": True,
        "ZapierAccessToken": None,
        "ZapierRefreshToken": None,
        "TelegramID": None
    }

    _id: ObjectId = PERMISSIONS_COLL.insert_one(user_attrs).inserted_id
    yield user_attrs

    # Delete the user
    PERMISSIONS_COLL.delete_one({"_id": _id})


@pytest.fixture
def temp_usage_logs():
    """
    Generate two temporary elements in the usage log so a usage report
    can be generated on that log. Delete the log afterwards.
    """
    usage_payloads = [
        {
            "phone_number": "12223334455",
            "app_name": "groceries",
            "content": "apples\nbananas",
            "options": {"setup": "whole foods"},
            "time": dt.datetime.now(pytz.timezone(CONFIG.General.default_timezone))
        },
        {
            "phone_number": "12223334455",
            "app_name": "groceries",
            "content": "chicken",
            "options": {"inbound_phone": "12223334455"},
            "time": dt.datetime.now(pytz.timezone(CONFIG.General.default_timezone))
        }
    ]

    keys = [usage.log_use(**payload) for payload in usage_payloads]
    yield usage_payloads

    # Remove the temporary logs
    for key in keys:
        usage.usage_db.delete(key)


@pytest.fixture
def who_are_you_twilio_recording() -> str:
    """Twilio audio recording asking 'who are you?'"""
    return (
        "https://api.twilio.com/2010-04-01/Accounts/ACe84ee0dbced3a3132211427153ae959a"
        "/Recordings/REed31c6f0df039c1d98b23288ae87fc73"
    )


@pytest.fixture(scope="session")
def outbound_call_key() -> str:
    """Call ID for outbound call."""
    call = Call.create(
        recipient_desc="Epic Restaurant",
        goal="Make a reservation for 2 people at 7pm on Friday"
    )

    # Add the greeting to the conversation as if it was spoken
    # the handler does this automatically
    call.convo += f"Jeeves: {call.greeting}"
    call.upload()

    yield call.key

    # Remove the temporary call
    call.delete()


@pytest.fixture(scope="session")
def callback_uid() -> str:
    """UID for callback manager."""
    test_uid = dt.datetime.now(
        pytz.timezone(CONFIG.General.default_timezone)
    ).isoformat().replace(':', ';')
    return f"test-{test_uid}"


@pytest.fixture(scope="session")
def callback_handlers(callback_uid):
    """Callback manager with testing uid."""
    return create_callback_handlers(uid=callback_uid)


@pytest.fixture(scope="session")
def temporary_user_memory(default_inbound) -> str:
    """Temporary user memory for testing. Yields the phone number."""
    user_memory = UserMemory.from_user_phone(default_inbound["phone_number"])
    user_memory.add_entry("My favorite color is blue.")
    user_memory.add_entry("I parked my car on level 2.")

    yield default_inbound["phone_number"]

    # Remove the temporary user memory
    user_memory.purge()
