"""Applet to create and update user permissions."""
import utils

from apps.permissions import query
from apps.permissions import operations


APP_HELP = (
    "Add permissions for a new user or update those of a current one. "
    "Message content should be the new permissions."
)
APP_OPTIONS = {
    "action": "REQUIRED, either 'create', 'update', or 'view'.",
    "phone": "REQUIRED, phone number of new or existing user.",
    "name": "MAYBE, only needed if adding a new user, or for convenience."
}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict[str, str]) -> str:
    """Update permissions in the database."""
    content = content.lower()  # all db permissions are in lower case

    if not (action := options.get("action")):
        return "You must provide an action. See app help, options: help = yes."

    if options["action"] not in {"view", "delete"} and not content:
        return "You must provide the user's permissions as content when not using " \
            "the view action."

    key = query.query(options.get("name", ""), options.get("phone", ""))

    if action == "create":
        if not (name := options.get("name")) or not (phone := options.get("phone")):
            return "You must provide both a name and phone number " \
                "when creating permissions."
        
        if key:
            return f"Permissions already exist for {name.title()}."

        operations.create_permissions(name, phone, content)
        return f"Successfully created permissions for {name.title()}."

    if action == "view":
        if not key:
            return "I didn't find an entry based on the name and/or phone " \
                "you provided."
        
        return f"The permissions for {query.name(key)} are below." \
            f"\n\n{operations.read_permissions(key)}"

    if action == "update":
        if not key:
            return "I didn't find an entry based on the name and/or phone " \
                "you provided."

        operations.update_permissions(key, content)
        return f"Successfully updated {query.name(key)}'s permissions." \
            f"\n\n{query.value(key)}"
        

    if action == "delete":
        if not key:
            return "I didn't find an entry based on the name and/or phone " \
                "you provided."

        name = query.name(key)
        operations.delete_permissions(key)
        return f"Successfully deleted the permissions entry of {name}."
        