import texts

import groceries
import wordhunt


def handler(content: str, user: str):
    """Handler for apps."""
    available_apps = ""
    for app in PROGRAMS.keys():
        available_apps += f"\n{app}"

    texts.send_message(
        content = f"The following apps are available.\n{available_apps}",
        recipient = user
    )

    return "", 204


PROGRAMS = {
    "apps": handler,
    "groceries": groceries.handler,
    "wordhunt": wordhunt.handler
}
