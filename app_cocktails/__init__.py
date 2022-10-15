"""Get cocktail drink recommendations with ingredients and instructions."""
import utils

from . import data


APP_HELP = "Get cocktail drink recommendations with ingredients and instructions."
APP_OPTIONS = {}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    """Gather and report the drink info. String format it."""
    drink = data.random_cocktail()
    return str(drink)
