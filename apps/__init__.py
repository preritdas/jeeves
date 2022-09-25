import groceries
import wordhunt


def handler(content: str, user: str):
    """Handler for apps."""
    available_apps = ""
    for app in PROGRAMS.keys():
        available_apps += f"\n{app}"

    return f"The following apps are available.\n{available_apps}"


PROGRAMS = {
    "apps": handler,
    "groceries": groceries.handler,
    "wordhunt": wordhunt.handler
}
