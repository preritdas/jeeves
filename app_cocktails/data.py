"""Gather data from APIs for cocktail info."""
import requests


ENDPOINT = "https://www.thecocktaildb.com/api/json/v1/1/"


def _parse_ingredients(raw_drink: dict) -> dict:
    """Returns a dictionary mapping between ingredient names and their quantities."""
    


def random_cocktail() -> dict:
    """Get a random cocktail."""
    response = requests.get(ENDPOINT + "random.php").json()
    
    # Ensure the result is actually a cocktail
    while response["drinks"][0]["strCategory"] != "Cocktail":
        return random_cocktail()

    raw_drink = response["drinks"][0]
    drink_attrs = {"name": raw_drink["strDrink"]}
    
    return raw_drink







if __name__ == '__main__':
    print(random_cocktail())
