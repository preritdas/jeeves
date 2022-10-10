"""Groceries app."""
import datetime as dt

import utils
import config

from . import classification
from permissions import deta


APP_HELP = "Organize your grocery list into categories."
APP_OPTIONS = {
    "setup": "custom store setups, ex. whole foods",
    "add": "add to a previous grocery list, ex. yes",
    "id": "required with 'add', previous list ID"
}


grocery_db = deta.Base("groceries")


def latest_grocery_list(phone: str) -> dict:
    """Finds the last grocery list belonging to `phone`. Returns an empty dictionary if there are no lists belonging to `phone`."""
    db_res = grocery_db.fetch({"phone": phone}).items
    
    if not db_res: 
        return {}

    return max(
        db_res, 
        key = lambda item: dt.datetime.strptime(
            item["time"], 
            config.Groceries.FULL_DT_FORMAT
        )
    )
    

@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict):
    # Options
    setup = options.get("setup", None)

    if (list_id := options.get("add", None)):
        # Get the user's last list
        old_list = latest_grocery_list(options["inbound_phone"]) if list_id == "last" \
            else grocery_db.get(list_id)

        if not old_list:
            return f"No existing list was found."

        # Append old list to current list 
        old_list = old_list["list"]
        content += f"\n{old_list}"

    # List
    sorted_list = classification.classify_grocery_list(content, setup=setup)

    # IDs
    put_item = grocery_db.put(
        {
            "list": content,
            "phone": options["inbound_phone"],
            "time": dt.datetime.now().strftime(config.Groceries.FULL_DT_FORMAT)
        }
    )
    
    return f"List ID: {put_item['key']}\n\n{sorted_list}"
    