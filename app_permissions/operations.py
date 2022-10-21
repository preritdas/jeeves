"""Database management CRUD operations: updating, deleting, viewing, creating."""
from permissions import permissions_db


def create_permissions(name: str, phone: str, value: str) -> str:
    """
    Create an entry in the permissions db. Returns the key
    of the created item.
    """
    return permissions_db.put(
        {
            "Name": name,
            "Phone": phone,
            "Permissions": value
        }
    )


def read_permissions(key: str) -> str:
    """Returns the permissions value by key."""
    return permissions_db.get(key)["Permissions"]


def update_permissions(key: str, value: str) -> str:
    """Updates permissions by key. Returns the same key."""
    permissions_db.update(
        updates = {
            "Permissions": value
        },
        key = key
    )

    return key


def delete_permissions(key: str) -> str:
    """Deletes an entry and returns the key of the item deleted."""
    permissions_db.delete(key)
    return key
