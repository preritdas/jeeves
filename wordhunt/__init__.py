from . import wordhunt


def handler(content: str, options: dict):
    if options.get("help", None):
        return "Solve a WordHunt board.\n\n" \
            "Available options:\n" \
            "- height: board height, default 4" \
            "- width: board width, default 4" \
            "- limit: results limit, default 20"

    height = options.get("height", 4)
    width = options.get("width", 4)
    limit = options.get("limit", 20)

    res = wordhunt.all_possibilities(wordhunt.create_board(content, width, height))
    return wordhunt.print_results(res, limit)
