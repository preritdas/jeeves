import utils

from . import classification
from permissions import deta


APP_HELP = "Organize your grocery list into categories."
APP_OPTIONS = {
    "setup": "custom store setups, ex. whole foods",
    "add": "add to a previous grocery list, ex. yes",
    "id": "required with 'add', previous list ID"
}


grocery_db = deta.Base("groceries")


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict):
    # Options
    setup = options.get("setup", None)

    if options.get("add", None):
        old_key = options["id"]
        old_list = grocery_db.get(old_key)

        if not old_list:
            return f"No existing list was found with ID {options['id']}."

        # Append old list to current list 
        old_list = old_list["list"]
        content += f"\n{old_list}"

    # List
    sorted_list = classification.classify_grocery_list(content, setup=setup)

    # IDs
    key = grocery_db.put({"list": content})["key"]
    
    return f"List ID: {key}\n\n{sorted_list}"
    