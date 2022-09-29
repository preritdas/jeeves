"""Registered apps."""
# Project
import utils

# Apps
import app_groceries
import app_wordhunt
import app_echo
import app_permissions
import app_jokes
import app_weather
import app_invite


@utils.app_handler(app_help = "See a list of available apps.")
def handler(content: str, options: dict):
    """Handler for apps."""
    available_apps = ""
    for app in sorted(PROGRAMS.keys()):
        available_apps += f"\n{app}"

    return f"The following apps are available.\n{available_apps}"


PROGRAMS = {
    "apps": handler,
    "groceries": app_groceries.handler,
    "wordhunt": app_wordhunt.handler,
    "echo": app_echo.handler,
    "permissions": app_permissions.handler,
    "jokes": app_jokes.handler,
    "weather": app_weather.handler,
    "invite": app_invite.handler
}
