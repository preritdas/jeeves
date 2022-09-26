from . import classification
from permissions import deta


grocery_db = deta.Base("groceries")


def handler(content: str, options: dict):
    if options.get("help", None):
        return "Organize your grocery list by item category.\n\n" \
            "Available options:\n" \
            "- setup: custom store setup, ex. whole foods"

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
    