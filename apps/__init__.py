import groceries
import wordhunt
import echo
import perms
import jokes


def handler(content: str, options: dict):
    """Handler for apps."""
    available_apps = ""
    for app in PROGRAMS.keys():
        available_apps += f"\n{app}"

    return f"The following apps are available.\n{available_apps}"


PROGRAMS = {
    "apps": handler,
    "groceries": groceries.handler,
    "wordhunt": wordhunt.handler,
    "echo": echo.handler,
    "permissions": perms.handler,
    "jokes": jokes.handler
}
