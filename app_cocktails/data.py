"""Gather data from APIs for cocktail info."""
import requests

from dataclasses import dataclass


ENDPOINT = "https://www.thecocktaildb.com/api/json/v1/1/"


@dataclass
class Drink:
    """Class for holding drink information, with string formatting."""
    name: str
    ingredients: dict[str, str]
    instructions: str

    def __str__(self) -> str:
        """String format the drink."""
        ingredients_list = []
        for ingredient, amount in self.ingredients.items():
            ingredients_list.append(f"{ingredient.lower()} - {amount.lower()}")

        ingredients_str = "\n".join(ingredients_list)

        return f"Behold, the {self.name.title()}. Here's what you'll need.\n\n" \
            f"{ingredients_str}\n\n{self.instructions}\n\nEnjoy!"


def _parse_ingredients(raw_drink: dict) -> dict:
    """Returns a dictionary mapping between ingredient names and their quantities."""
    all_ingredients = {}

    for n_ingredient in range(1, 16):
        if not raw_drink[(loc := f"strIngredient{n_ingredient}")]:
            break
    
        all_ingredients[raw_drink[loc].strip()] = \
            raw_drink[f"strMeasure{n_ingredient}"].strip()

    return all_ingredients


def random_cocktail() -> Drink:
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

    return Drink(**drink_attrs)
