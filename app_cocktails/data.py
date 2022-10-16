"""Gather data from APIs for cocktail info."""
# External
import requests

# Local
from dataclasses import dataclass

# App-level
from . import errors


ENDPOINT = "https://www.thecocktaildb.com/api/json/v1/1/"


@dataclass
class Drink:
    """Class for holding drink information, with string formatting."""
    name: str
    ingredients: dict[str, str]
    instructions: str

    @classmethod
    def from_response(cls, response: requests.Response, all_drinks: bool = False):
        """
        Return a `Drink` instance based on a raw response from the API.
        This could be more convenient than inputting the name, ingredients, and
        parsed instructions manually using the __init__ constructor.
        """
        response = response.json()

        if not response["drinks"]:
            raise errors.DrinkNotFoundError()
        
        assert response
        assert len(response["drinks"]) >= 1

        if not all_drinks:
            raw_drink = response["drinks"][0]

            return cls(
                name = raw_drink["strDrink"].strip(),
                ingredients = _parse_ingredients(raw_drink),
                instructions = raw_drink["strInstructions"].strip()
            )

        drinks: list[Drink] = []
        for raw_drink in response["drinks"]:
            drinks.append(
                cls(
                    name = raw_drink["strDrink"].strip(),
                    ingredients = _parse_ingredients(raw_drink),
                    instructions = raw_drink["strInstructions"].strip()
                )
            )

        return drinks


    def __str__(self) -> str:
        """String format the drink."""
        ingredients_list = []
        for ingredient, amount in self.ingredients.items():
            ingredients_list.append(f"{ingredient.lower()} - {amount.lower()}")

        ingredients_str = "\n".join(ingredients_list)

        return f"Behold, the {self.name.title()}. Here's what you'll need.\n\n" \
            f"{ingredients_str}\n\n{self.instructions}\n\nEnjoy!"


def search_cocktail(cocktail_name: str) -> list[Drink]:
    """
    Search cocktails matching the query `cocktail_name`. 
    If no cocktail is found, returns an empty list.
    """
    response = requests.get(ENDPOINT + f"search.php?s={cocktail_name.strip()}")

    if not response.json()["drinks"]:
        return None

    return Drink.from_response(response, all_drinks=True)


def _parse_ingredients(raw_drink: dict) -> dict[str, str]:
    """Returns a dictionary mapping between ingredient names and their quantities."""
    all_ingredients = {}

    for n_ingredient in range(1, 16):
        if not raw_drink[(loc := f"strIngredient{n_ingredient}")]:
            break
    
        measurement: str | None = raw_drink[f"strMeasure{n_ingredient}"]

        if measurement:
            measurement = measurement.strip()
        else:
            measurement = "Up to you."

        all_ingredients[raw_drink[loc].strip()] = measurement

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
