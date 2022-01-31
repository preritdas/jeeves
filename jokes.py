import requests

def getJoke():
    url = "https://api.chucknorris.io/jokes/random"
    try:
        response = requests.get(url).json()["value"]
    except:
        response = "Error getting joke from source."
    return response