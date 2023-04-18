"""
Read permissions stored in a Deta Base.
"""
# External
import deta

# Project
from keys import KEYS


deta_client = deta.Deta(KEYS["Deta"]["project_key"])
permissions_db = deta_client.Base("permissions")


def db_init() -> str:
    """
    If there's nothing in the Base, fire it up with the proper
    fields and formatting. Returns the key of the added field
    for testing purposes (so it can be removed automatically in a test environment).

    This function was designed to be called manually.
    """
    db_res: dict = permissions_db.put(
        {
            "Name": "Prerit Das",
            "Phone": KEYS["Twilio"]["my_number"],
            "Permissions": "all"
        }
    )

    return db_res["key"]


# If there's nothing in the database, initialize it.
if not permissions_db.fetch().items:
    db_init()


def check_permissions(phone: str, app_name: str) -> bool:
    items = permissions_db.fetch(query={"Phone": phone}).items

    if not items: return False

    for entry in items:
        permissions = [ele.strip() for ele in entry["Permissions"].lower().split(",")]

        if "all" in permissions: 
            return True

        if app_name.lower() in permissions:
            return True

    return False
