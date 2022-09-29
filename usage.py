"""Tracking app usage for reports."""
import deta

import keys


deta = deta.Deta(keys.Deta.project_key)
usage_db = deta.Base("usage")


def store_use(phone_number: str, app_name: str, content: str, options: dict) -> None:
    """Store a use to the database."""
    # Check all are string except options (dict)
    assert all(
        isinstance(param, str) for param in [
            phone_number, app_name, content
        ]
    )

    payload = {
        "Phone": phone_number,
        "App": app_name,
        "Content": content,
        "Options": options
    }

    usage_db.put(payload)
