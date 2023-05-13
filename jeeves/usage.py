"""Tracking app usage for reports."""
# External
import deta

# Internal
import datetime as dt
import pytz
import string
import random

# Project
from jeeves.keys import KEYS
from jeeves.config import CONFIG


deta = deta.Deta(KEYS.Deta.project_key)
usage_db = deta.Base("usage")
permissions_db = deta.Base("permissions")


# Standardized date and time formats

DT_FORMAT_DATE = "%Y-%m-%d"
DT_FORMAT_TIME = "%H:%M:%S"
DT_FORMAT = " ".join([DT_FORMAT_DATE, DT_FORMAT_TIME])


def log_use(
    phone_number: str,
    app_name: str,
    content: str,
    options: dict,
    time: dt.datetime | None = None
) -> str:
    """
    Store a use to the database. Returns the key of the new db entry.
    If no time is given directly, the exact time of function call is used.
    """
    # Check all are string except options (dict) and time
    assert all(isinstance(param, str) for param in [phone_number, app_name, content])

    if time:
        assert isinstance(time, dt.datetime)
        time = time.strftime(DT_FORMAT)
    else:
        time = dt.datetime.now(
            pytz.timezone(CONFIG.General.default_timezone)
        ).strftime(DT_FORMAT)

    payload = {
        "Phone": phone_number,
        "App": app_name,
        "Content": content,
        "Options": options,
        "Time": time
    }

    # If in sandbox, return a fake key and don't post to database
    if CONFIG.General.sandbox_mode:
        return "".join([random.choice(string.ascii_lowercase) for _ in range(12)])

    res: dict = usage_db.put(payload)
    return res["key"]


def _phone_to_name(phone_number: str) -> str:
    """
    Attempts to convert a phone number to a name. If not possible,
    the phone number is returned.

    Assuming all users were initialized in the permissions database, which is
    in fact necessary, all converstions theoretically should be successful.
    """
    users = permissions_db.fetch({"Phone": phone_number}).items

    if len(users) != 1:
        return phone_number

    return users[0]["Name"]


def usage_summary(date: dt.date | str = None) -> str:
    """
    Generates a usage summary based on the database.

    If `date` parameter is not given, statistics are generated for
    the current day.
    """
    if isinstance(date, str):
        date = dt.datetime.strptime(date, DT_FORMAT_DATE)

    logs = usage_db.fetch().items

    today = date or dt.date.today()
    today_logs = []
    for log in logs:
        if dt.datetime.strptime(log["Time"], DT_FORMAT).date() == today:
            today_logs.append(log)

    total_pings = len(today_logs)

    app_pings = {}
    for log in today_logs:
        if log["App"] not in app_pings:
            app_pings[log["App"]] = 1
            continue

        app_pings[log["App"]] += 1

    person_uses = {}
    for log in today_logs:
        person = _phone_to_name(log["Phone"])

        if person not in person_uses:
            person_uses[person] = 1
            continue

        person_uses[person] += 1

    return (
        f"On {today.strftime(DT_FORMAT_DATE)}, I was pinged {total_pings} times. "
        f"App-specific pings are below.\n\n{app_pings}"
        f"\n\nPerson-specific pings:\n\n{person_uses}"
    )
