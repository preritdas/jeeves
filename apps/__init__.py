"""Registered apps."""
# Project
import parsing

# Apps
import groceries
import wordhunt
import echo
import perms
import jokes
import weather
import invite


@parsing.app_handler(app_help = "See a list of available apps.")
def handler(content: str, options: dict):
    """Handler for apps."""
    available_apps = ""
    for app in sorted(PROGRAMS.keys()):
        available_apps += f"\n{app}"

    return f"The following apps are available.\n{available_apps}"


PROGRAMS = {
    "apps": handler,
    "groceries": groceries.handler,
    "wordhunt": wordhunt.handler,
    "echo": echo.handler,
    "permissions": perms.handler,
    "jokes": jokes.handler,
    "weather": weather.handler,
    "invite": invite.handler
}
