"""WordHunt board solving app."""
import utils

from . import wordhunt


APP_HELP = "Solve a WordHunt board. Content is the board - top to bottom, left to right."
APP_OPTIONS = {
    "height": "board height, default 4",
    "width": "board width, default 4",
    "limit": "max number of results, default 20"
}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    if not content:
        return "You must provide the board layout as content."

    height = options.get("height", 4)
    width = options.get("width", 4)
    limit = options.get("limit", 20)

    res = wordhunt.all_possibilities(wordhunt.create_board(content, width, height))
    return wordhunt.print_results(res, limit)
