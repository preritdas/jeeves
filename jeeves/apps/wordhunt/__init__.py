"""WordHunt board solving app."""
from jeeves import utils

# import pyximport; pyximport.install(language_level=3)
from jeeves.apps.wordhunt import pure_wordhunt as wordhunt


APP_HELP = (
    "Solve a WordHunt board. Content is the board - top to bottom, left to right."
)
APP_OPTIONS = {
    "height": "board height, default 4",
    "width": "board width, default 4",
    "limit": "max number of results, default 20"
}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    if not content:
        return "You must provide the board layout as content."

    height = int(options.get("height", 4))
    width = int(options.get("width", 4))
    limit = int(options.get("limit", 20))

    if len(content) != height * width:
        return (
            f"The board is {height} tall and {width} wide, but you provided a "
            f"{len(content)} long board."
        )

    return wordhunt.Board.from_letters(content, width, height).print_results(limit)
