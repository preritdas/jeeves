from . import classification

def handler(content: str, options: dict):
    if options.get("help", None):
        return "Organize your grocery list by item category.\n\n" \
            "Available options:\n" \
            "- setup: custom store setup, ex. whole foods"

    # Options
    setup = options.get("setup", None)

    return classification.classify_grocery_list(content, setup=setup)
    