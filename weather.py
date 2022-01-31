import requests
from keys import openweather_apiKey

api_key = openweather_apiKey

def requestUrl(city):
    return 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + openweather_apiKey

def kelvinToFarenheit(temperature):
    return round((temperature - 273.15)*(9/5) + 32)

def getTemperature(city):
    response = requests.get(requestUrl(city)).json()
    if response["cod"] != "404":
        return round(kelvinToFarenheit(response["main"]["temp"]))
    else:
        return "error bad city name"

def getWeather(city):
    response = requests.get(requestUrl(city)).json()
    if response["cod"] != "404":
        return str(response["weather"][0]["main"]) + ", " + str(response["weather"][0]["description"])
    else:
        return "error bad city name"