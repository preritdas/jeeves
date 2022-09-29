"""Tracking app usage for reports."""
import deta

import datetime as dt

import keys


deta = deta.Deta(keys.Deta.project_key)
usage_db = deta.Base("usage")


DT_FORMAT_DATE = "%Y-%m-%d"
DT_FORMAT_TIME = "%H:%M:%S"
DT_FORMAT = " ".join([DT_FORMAT_DATE, DT_FORMAT_TIME])


def store_use(
    phone_number: str, 
    app_name: str, 
    content: str, 
    options: dict, 
    time: dt.time
) -> None:
    """Store a use to the database."""
    # Check all are string except options (dict) and time
    assert all(
        isinstance(param, str) for param in [
            phone_number, app_name, content
        ]
    )

    payload = {
        "Phone": phone_number,
        "App": app_name,
        "Content": content,
        "Options": options,
        "Time": time.strftime(DT_FORMAT)
    }

    usage_db.put(payload)


def usage_summary(date: dt.date = None) -> str:
    """
    Generates a usage summary based on the database.
    
    If `date` parameter is not given, statistics are generated for 
    the current day.
    """
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

    return f"On {today.strftime(DT_FORMAT_DATE)}, I was pinged {total_pings} times." \
        f"App-specific pings are below.\n\n{app_pings}"
