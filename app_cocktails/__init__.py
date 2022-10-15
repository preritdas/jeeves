"""Get cocktail drink recommendations with ingredients and instructions."""
import utils


APP_HELP = "Get cocktail drink recommendations with ingredients and instructions."
APP_OPTIONS = {}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    return "Cocktail."
