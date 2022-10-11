"""Registered apps."""
# Project
import utils
import permissions

# Apps
import app_groceries
import app_wordhunt
import app_echo
import app_permissions
import app_jokes
import app_weather
import app_invite
import app_usage
import app_rt


@utils.app_handler(app_help = "See a list of available apps.")
def handler(content: str, options: dict):
    """Handler for apps. Filters by permissions."""
    accessible_apps: list[str] = [
        app for app in PROGRAMS.keys() if permissions.check_permissions(
            phone = options.get("inbound_phone"),
            app_name = app
        )
    ]

    available_apps = ""
    for app in sorted(accessible_apps):
        available_apps += f"\n{app}"

    return f"The following apps are available to you.\n{available_apps}"


PROGRAMS = {
    "apps": handler,
    "groceries": app_groceries.handler,
    "wordhunt": app_wordhunt.handler,
    "echo": app_echo.handler,
    "permissions": app_permissions.handler,
    "jokes": app_jokes.handler,
    "weather": app_weather.handler,
    "invite": app_invite.handler,
    "usage": app_usage.handler,
    "rt": app_rt.handler
}
