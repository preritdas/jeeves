"""Gather data from APIs for cocktail info."""
import requests


ENDPOINT = "https://www.thecocktaildb.com/api/json/v1/1/"


def _parse_ingredients(raw_drink: dict) -> dict:
    """Returns a dictionary mapping between ingredient names and their quantities."""
    all_ingredients = {}

    for n_ingredient in range(1, 16):
        if not raw_drink[(loc := f"strIngredient{n_ingredient}")]:
            break
    
        all_ingredients[raw_drink[loc].strip()] = \
            raw_drink[f"strMeasure{n_ingredient}"].strip()

    return all_ingredients


def random_cocktail() -> dict:
    """Get a random cocktail."""
    response = requests.get(ENDPOINT + "random.php").json()
    
    # Ensure the result is actually a cocktail
    while response["drinks"][0]["strCategory"] != "Cocktail":
        return random_cocktail()

    raw_drink = response["drinks"][0]
    drink_attrs = {
        "name": raw_drink["strDrink"],
        "ingredients": _parse_ingredients(raw_drink),
        "instructions": raw_drink["strInstructions"]
    }

    return drink_attrs
