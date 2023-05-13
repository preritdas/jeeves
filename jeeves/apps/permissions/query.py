"""Query the permissions database."""
from permissions import permissions_db


class QueryError(Exception):
    pass


def query(name: str = "", phone: str = "") -> str:
    """
    Queries the database and returns the key if found, or an empty
    string if not found.

    Raises
    """
    if not name and not phone:
        return ""

    if phone:
        db_res = permissions_db.fetch({"Phone": phone})

        if len(db_res.items) == 1:
            return db_res.items[0]["key"]

        if len(db_res.items) > 1:
            raise QueryError(
                "Multiple users found with the same phone number. "
                "This is almost certainly an error."
            )

        return ""  # none found

    db_res = permissions_db.fetch({"Name": name.title()})

    if len(db_res.items) == 1:
        return db_res.items[0]["key"]

    if len(db_res.items) > 1:
        raise QueryError(f"Multiple users found with the name '{name}'.")

    return ""  # none found


def name(key: str) -> str:
    """Gets the name of an entry based on key."""
    return permissions_db.get(key)["Name"]


def value(key: str) -> str:
    """Gets the permissions value of an entry based on key."""
    return permissions_db.get(key)["Permissions"]
