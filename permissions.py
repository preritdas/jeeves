"""
Read permissions stored in a Deta Base.
"""
# External
import deta

# Project
import keys


deta = deta.Deta(keys.Deta.project_key)
permissions_db = deta.Base("permissions")


def db_init():
    """
    If there's nothing in the Base, fire it up with the proper
    fields and formatting.

    Call this function manually.
    """
    permissions_db.put(
        {
            "Name": "Prerit Das",
            "Phone": keys.Nexmo.mynumber,
            "Permissions": "all"
        }
    )


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
