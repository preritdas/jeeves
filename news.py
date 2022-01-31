import requests
from keys import news_apiKey

usBusinessURL = 'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=' + news_apiKey
usCOVIDURL = 'https://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=' + news_apiKey

def getFiveBusinessArticles():
    responses = []
    i = 0
    for i in range(5):
        response = requests.get(usBusinessURL).json()['articles'][i]['title']
        responses.append(response)
    compiled = f"1. {responses[0]} \n"\
                f"2. {responses[1]} \n"\
                f"3. {responses[2]} \n"\
                f"4. {responses[3]} \n"\
                f"5. {responses[4]} \n"
    return compiled

def getFiveCOVIDArticles():
    responses = []
    i = 0
    for i in range(5):
        response = requests.get(usCOVIDURL).json()['articles'][i]['title']
        responses.append(response)
    compiled = f"1. {responses[0]} \n"\
                f"2. {responses[1]} \n"\
                f"3. {responses[2]} \n"\
                f"4. {responses[3]} \n"\
                f"5. {responses[4]} \n"
    return compiled