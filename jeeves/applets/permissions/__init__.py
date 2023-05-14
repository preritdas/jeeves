"""Applet to create and update user permissions."""
from jeeves import utils


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
    raise NotImplementedError
