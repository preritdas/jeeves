"""
Responsible for turning a list of groceries with quantity into a classified
ordered list.
"""
# External
import translators

# Project
from . import grocery_utils


def _parse_list(grocery_list: str) -> set[tuple[int, str]]:
    """Takes in a list of groceries prefaced with their quantity. Example below.

    3 apples
    1 banana
    2 chicken

    Args:
        grocery_list (str): List of groceries in the format specified above.

    Returns:
        set[tuple[int, str]]: List of tuples with quantity and item name. Plurality
        in the name is preserved.
    """
    assert isinstance(grocery_list, str)

    grocery_list_split = grocery_list.splitlines()
    while '' in grocery_list_split: grocery_list_split.remove('')
    
    items = []
    for item in grocery_list_split:
        split = item.split()

        try: item_tup = int(split[0]), translators.google(" ".join(split[1:]))
        except ValueError: item_tup = "", translators.google(" ".join(split))

        items.append(tuple(item_tup))

    return set(items)


def _check_item_format(item):
    """
    Format of an item to be checked in the mapping.
    Handles paranthesis and caps.
    """
    check_item = item
    if "(" in item:  # paranthesis specifications
        check_item = item[:item.find("(")].strip()

    return grocery_utils.singularize(check_item).lower()


def _classify(item: str, setup: str) -> tuple[str, str]:
    """
    Determines the category of item. Returns an empty string if no category
    is matched. Returns a tuple of category and item useful if translated.
    """
    check_item = _check_item_format(item)

    for category in grocery_utils.MAPPING(setup):
        if check_item in grocery_utils.MAPPING(setup)[category]: 
            return category, item

    return "", item  # always return a translation to english


def _order_classification(classification: dict, setup: str) -> dict[str, list[tuple[int, str]]]:
    """Reorder categories to match the mapping."""
    for category in classification:
        if category == "none": continue
        classification[category] = sorted(
            classification[category], 
            key = lambda item: grocery_utils.MAPPING(setup)[category].index(
                _check_item_format(item[1])
            )
        )

    classification_keys = list(classification.keys())
    if "none" in classification_keys: 
        none_present = True
        classification_keys.remove("none")
    else:
        none_present = False

    key_order = sorted(
        classification_keys, 
        key = lambda category: list(grocery_utils.MAPPING(setup).keys()).index(category)
    )

    if none_present: 
        key_order.append("none")
    
    return {key: classification[key] for key in key_order}


def _classify_items(grocery_list: str, setup: str) -> dict[str, list[tuple[int, str]]]:
    """Classify the grocery list."""
    return_classifications = {"none": []}
    for item_tup in (parsed_list := _parse_list(grocery_list)):
        # Update the item if it was translated by _classify
        item_tup = list(item_tup)
        category, item_tup[1] = _classify(item_tup[1], setup=setup)
        item_tup = tuple(item_tup)

        if not category: 
            return_classifications["none"].append(item_tup)
        elif category not in return_classifications:
            return_classifications[category] = [item_tup]
        else:
            return_classifications[category].append(item_tup)

    # return return_classifications
    return _order_classification(return_classifications, setup=setup)


def _format_list(item_list: dict[str, list[tuple[int | str, str]]]) -> str:
    """Turn the classified list into a string grocery list."""
    return_str = ""
    for category, items in item_list.items():
        if not items: continue
        return_str += f"{category.title()}: \n"

        for pos, item in enumerate(items): 
            return_str += f"- {str(item[0]) + ' ' if item[0] else ''}{item[1]}".strip()
            if pos < len(items) - 1: return_str += '\n'

        return_str += "\n\n"
    
    return return_str[:-2]


def classify_grocery_list(grocery_list: str, setup: str = None) -> str:
    """Classify the grocery list and return a formatted string grocery list."""
    return _format_list(_classify_items(grocery_list, setup=setup))
