"""Groceries app."""
import datetime as dt

from utils import app_handler
from config import CONFIG

from apps.groceries import classification
from apps.groceries.utils import SETUPS
from permissions import deta_client


APP_HELP = "Organize your grocery list into categories."
APP_OPTIONS = {
    "setup": f"Custom store setup. Available: {', '.join(SETUPS.keys())}",
    "add": "ID of a previous list to add to it. "
    "ex. 'last' for your latest list, or the raw ID."
}


grocery_db = deta_client.Base("groceries")


def latest_grocery_list(phone: str) -> dict:
    """Finds the last grocery list belonging to `phone`. Returns an empty dictionary if there are no lists belonging to `phone`."""
    db_res = grocery_db.fetch({"phone": phone}).items

    if not db_res:
        return {}

    return max(
        db_res,
        key=lambda item: dt.datetime.strptime(
            item["time"], CONFIG.Groceries.full_dt_format
        )
    )


@app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    # Options
    setup = options.get("setup")

    # Check for a valid setup
    if setup and not setup.title() in SETUPS:
        available_setups = list(SETUPS.keys())
        return f"Invalid setup. Available setups: {', '.join(available_setups)}"

    if list_id := options.get("add"):
        # Get the user's last list
        old_list = (
            latest_grocery_list(options["inbound_phone"])
            if list_id == "last"
            else grocery_db.get(list_id)
        )

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
            "time": dt.datetime.now().strftime(CONFIG.Groceries.full_dt_format)
        }
    )

    return f"List ID: {put_item['key']}\n\n{sorted_list}"
