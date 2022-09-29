"""Tracking app usage for reports."""
import deta

import datetime as dt

import keys


deta = deta.Deta(keys.Deta.project_key)
usage_db = deta.Base("usage")


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
        "Time": time.strftime("%H:%M:%S")
    }

    usage_db.put(payload)


def usage_summary() -> str:
    """Generates a usage summary based on the database."""
    logs = usage_db.fetch().items

    total_pings = len(logs)
    
    app_pings = {}
    for log in logs:
        if log["App"] not in app_pings:
            app_pings[log["App"]] = 1

        app_pings[log["App"]] += 1


