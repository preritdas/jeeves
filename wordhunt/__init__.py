from . import wordhunt


def handler(content: str, options: dict):
    height = options.get("height", 4)
    width = options.get("width", 4)
    limit = options.get("limit", 20)

    res = wordhunt.all_possibilities(wordhunt.create_board(content, width, height))
    return wordhunt.print_results(res, limit)
