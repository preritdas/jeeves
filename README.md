# Meet Jeeves.

_This was my first project and has since been retired._

Read the background from its [original source](https://jeeves.preritdas.com). The read-me below includes information on how to setup the program from scratch and how to deploy it. The files in their full form are in the repository and are regularly updated when I make significant or necessary changes. As such, the code in the read-me is likely outdated and should only be used in context or as a guide for building the program.

----
Jeeves is a personal assistant who texts me all the information I want, when I want it. I've included all code necessary to recreate what I have thus far. My API keys are the only element not included. In the code below, they’re locally imported as `from keys import keyName`. I've listed all necessary requisites at the end. So far, Jeeves is capable of the following:

- Market updates for indices or specific instruments
- Weather information, such as a day's temperature, forecast or umbrella necessity by location
- COVID information by location (see [covidinfo.preritdas.com](http://covidinfo.preritdas.com) for more on this!)
- COVID news by location
- Crypto prices, updates, and other relevant information

But Jeeves, through all his interactions and schemes, grows smarter each day.

## main.py

```python
import time
from datetime import datetime as dt
from covid import *
from marketdata import *
from texts import *
from weather import *
from news import *
import json
import sys

# Recipients format: "person": [phone number as string, city, state code]. note: only U.S. supported.
recipients = { #as many as you want
    "person1": ["14250000000", 'Seattle', 'WA'],
    "person2": ["1theirUS#", 'City', 'US State'],
    "person3": ["1theirUS#", 'City', 'US State']
}

# Use debug mode by including 'debug' anywhere after 'python main.py'
try:
    if 'debug' in sys.argv:
        recipients = {
            "me": [mynumber, "Yabadabadoobeedoo", "WA"]
        }
except:
    pass

def compileMessage(city, state):
    morningText = "Good morning, sir. " + f"As you slept, SPY moved {stockOvernightChange('SPY')}, "\
        f"QQQ moved {stockOvernightChange('QQQ')}, " + f"Apple moved {stockOvernightChange('AAPL')}, "\
        f"and NVDA moved {stockOvernightChange('NVDA')}. Futures maintained balance. \n\n"\
        f"Our Bitcoin holdings are worth {bitcoinPrice()} per coin, and the daily bar has moved {bitcoinChange()[0]} dollars, or {bitcoinChange()[1]}. "\
        f"Coinbase stock moved {stockOvernightChange('COIN')}, "\
        f"Brookfield moved {stockOvernightChange('BAM')}, "\
        f"and Halliburton moved {stockOvernightChange('HAL')}. "\
        f"The time is {dt.now().strftime('%H:%M')}. "\
        f"It is currently {getTemperature(city)} degrees outside, sir. My old gentleman, a weatherman, eloquently "\
        f"described today's forecast as '{getWeather(city)}.' \n\n"\
        f"I've gathered some COVID information from the paper, sir. In our state of {state}, the infection rate is {covidInfo(state).infRate}. "\
        f"There were {covidInfo(state).newCases} new cases today, and the positive testing rate is {covidInfo(state).posRate}%. "\
        f"{covidInfo(state).newDeaths} people died of COVID in the last day, but, sir, I anticipate my source to have reported this falsely. "\
        f"We both are fully vaccinated, sir, just as {covidInfo(state).vaxRate}% of our fellow residents. "\
        f"You may not find this to be particularly relevant, sir, but {covidInfo(state).freeBedPercentage}% of our hospital beds are empty. "\
        f"{covidInfo(state).covidBedPercentage}% of those filled are occupied by COVID patients."
        
    morningText2 = "\n\nSome COVID headlines, sir. \n\n" + f"{getFiveCOVIDArticles()} \n"\
        "I expect you to find my report helpful; I endeavour to give satisfaction. \n\n"\
        "- Jeeves."

    # morningText3 = "Strength test. Third message."

    return [morningText, morningText2]

# Send the message
def main():
    print('I am ready for the morning, sir.', '\n')
    
    # Print run mode (debug or run-now-despite-time)
    if 'go' in sys.argv:
        print("In 'run anyway' mode.")
    if 'debug' in sys.argv:
        print("In debug mode. Recipient list: ", "\n")
        print(json.dumps(recipients, indent = 4))

    while True:
        tic = time.perf_counter() # starting counting time
        currentTime = dt.now().strftime('%H-%M')
        if currentTime == '06-35' or 'go' in sys.argv: 
            successfulDeliveries = []
            failedDeliveries = []

            for recipient in recipients:
                try:
                    textContent = compileMessage(recipients[recipient][1], recipients[recipient][2])

                    i = 1
                    for content in textContent:
                        print(f"{recipient} part {i}: {content}", "\n")
                        i += 1

                    # Send messages 
                    textresponses = []
                    for message in textContent:
                        textresponse = sms.send_message(
                            {
                                "from": sender,
                                "to": recipients[recipient][0],
                                "text": message
                            }
                        )
                        textresponses.append(textresponse["messages"][0]["status"])
                        time.sleep(10)

                    i = 0
                    for i in range(len(textresponses)):
                        if textresponses[i] != '0':
                            failedDeliveries.append(recipient)
                            break
                        elif textresponses[i] == '0' and i == len(textresponses) - 1:
                            successfulDeliveries.append(recipient)
                            break


                    print("--------")
                    print('')
                    time.sleep(45)

                except: # If compiling returns an error
                    for recipient in recipients:
                        textresponse = sms.send_message(
                            {
                                "from": sender,
                                "to": recipients[recipient][0],
                                "text": "There was an error compiling the message, sir. This is usually due to an unexpected market holiday. I'll have this issue resolved shortly, sir."
                            }
                        )  
                        if textresponse["messages"][0]["status"] == '0':
                            successfulDeliveries.append(recipient)
                        else:
                            failedDeliveries.append(recipient)

            # End of day review
            print("Sir, I'm finished for the day, and shall be returning to my lair.")
            for person in successfulDeliveries:
                print("I successfully delivered to you." if person == 'me' else f"I successfully delivered to {person}.")
            print('')
            for person in failedDeliveries:
                print(f'Unfortunately, I failed delivering to {person}.')
            toc = time.perf_counter() # stop tracking time
            print(f"The whole process took me {round(toc - tic)} seconds, sir.")

            try:
                i = 0
                for i in range (len(sys.argv)):
                    if sys.argv[i] == 'go':
                        sys.argv[i] = 'modifiedNoGo'
            except:
                pass

            time.sleep(600)
        else:
            pass

if __name__ == "__main__":
    main()
```

The `main.py` program above is my execution program that runs 24/7 on a Linux server. It triggers automatically every morning at 6:35 a.m., according to the statement `if currentTime == '06:35'`. It compiles and sends a morning message to approximately 10 recipients across the country. 

By starting the program with the `go` parameter, ex. `python main.py go`, the program will run immediately despite the time not being 6:35. The `debug` parameter will use a shortened recipient list (my own, or the owner’s) for testing purposes. The parameters can be given in any order, and extra meaningless parameters will not affect the program.

It compiles weather and COVID data for each person based on their location, as the data collection functions take location as a parameter. I coded them this way so I can use the _same functions_ to send a message to anyone in any location, and it’s very convenient. 

Time breaks in between each text call, `sms.send_message()`, are unnecessary but I left them in regardless.

## marketdata.py

```python
import finnhub
import time
from datetime import date, timedelta
from datetime import datetime as dt
import requests
from keys import *

fc = finnhub.Client(api_key=finnhub_apiKey)

def stockOvernightChange(symbol):
    isoweekday = dt.today().isoweekday()
    if isoweekday==2 or isoweekday==3 or isoweekday == 4 or isoweekday==5:
        today = dt.today()
        yesterday = today - timedelta(days=1)
        beforeYesterday = today - timedelta(days=2)
        todayUNIX = int(time.mktime(today.timetuple()))
        yesterdayUNIX = int(time.mktime(yesterday.timetuple()))
        beforeYesterdayUNIX = int(time.mktime(beforeYesterday.timetuple()))

        #data

        stockOpen = fc.stock_candles(symbol, 'D', yesterdayUNIX, todayUNIX)['o'][0]
        stockClose = fc.stock_candles(symbol, 'D', beforeYesterdayUNIX, yesterdayUNIX)['c'][0]
        priceChange = stockOpen - stockClose
        percentChange = round((100*(priceChange/stockClose)), 3)
        percentChange = str(percentChange) + "%"
        return percentChange
    elif isoweekday == 1:
        today = dt.today()
        yesterday = today - timedelta(days=3)
        beforeYesterday = today - timedelta(days=4)
        todayUNIX = int(time.mktime(today.timetuple()))
        yesterdayUNIX = int(time.mktime(yesterday.timetuple()))
        beforeYesterdayUNIX = int(time.mktime(beforeYesterday.timetuple()))

        #data

        stockOpen = fc.stock_candles(symbol, 'D', yesterdayUNIX, todayUNIX)['o'][0]
        stockClose = fc.stock_candles(symbol, 'D', beforeYesterdayUNIX, yesterdayUNIX)['c'][0]
        priceChange = stockOpen - stockClose
        percentChange = round((100*(priceChange/stockClose)), 3)
        percentChange = str(percentChange) + "%"
        return percentChange
    elif isoweekday == 6:
        today = dt.today() - timedelta(days=1)
        yesterday = today - timedelta(days=1)
        beforeYesterday = yesterday - timedelta(days=1)
        todayUNIX = int(time.mktime(today.timetuple()))
        yesterdayUNIX = int(time.mktime(yesterday.timetuple()))
        beforeYesterdayUNIX = int(time.mktime(beforeYesterday.timetuple()))

        #data

        stockOpen = fc.stock_candles(symbol, 'D', yesterdayUNIX, todayUNIX)['o'][0]
        stockClose = fc.stock_candles(symbol, 'D', beforeYesterdayUNIX, yesterdayUNIX)['c'][0]
        priceChange = stockOpen - stockClose
        percentChange = round((100*(priceChange/stockClose)), 3)
        percentChange = str(percentChange) + "%"
        return percentChange
    elif isoweekday == 7:
        today = dt.today() - timedelta(days=2)
        yesterday = today - timedelta(days=3)
        beforeYesterday = yesterday - timedelta(days=1)
        todayUNIX = int(time.mktime(today.timetuple()))
        yesterdayUNIX = int(time.mktime(yesterday.timetuple()))
        beforeYesterdayUNIX = int(time.mktime(beforeYesterday.timetuple()))

        #data

        stockOpen = fc.stock_candles(symbol, 'D', yesterdayUNIX, todayUNIX)['o'][0]
        stockClose = fc.stock_candles(symbol, 'D', beforeYesterdayUNIX, yesterdayUNIX)['c'][0]
        priceChange = stockOpen - stockClose
        percentChange = round((100*(priceChange/stockClose)), 3)
        percentChange = str(percentChange) + "%"
        return percentChange
    else:
        return "Time error in method stockOvernightChange in marketdata.py."

def cryptoOvernightChange(symbol):
    today = dt.today()
    yesterday = today - timedelta(days=1)
    beforeYesterday = today - timedelta(days=2)
    todayUNIX = int(time.mktime(today.timetuple()))
    yesterdayUNIX = int(time.mktime(yesterday.timetuple()))
    beforeYesterdayUNIX = int(time.mktime(beforeYesterday.timetuple()))

    #data

    stockOpen = fc.crypto_candles(symbol, 'D', yesterdayUNIX, todayUNIX)['o'][0]
    stockClose = fc.crypto_candles(symbol, 'D', beforeYesterdayUNIX, yesterdayUNIX)['o'][0]
    priceChange = stockOpen - stockClose
    percentChange = round((100*(priceChange/stockClose)), 3)
    percentChange = str(percentChange) + "%"
    return percentChange

def bitcoinPrice():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return round(data["bpi"]["USD"]["rate_float"], 2)

def bitcoinChange():
    symbol = "BINANCE:BTCUSDT"
    today = dt.today()
    yesterday = today - timedelta(days=1)
    beforeYesterday = today - timedelta(days=2)
    yesterdayUNIX = int(time.mktime(yesterday.timetuple()))
    beforeYesterdayUNIX = int(time.mktime(beforeYesterday.timetuple()))
    stockClose = fc.crypto_candles(symbol, 'D', beforeYesterdayUNIX, yesterdayUNIX)['o'][0]
    bitcoinDollarChange = round((bitcoinPrice() - stockClose), 2)
    bitcoinDollarChangeStr = str(bitcoinDollarChange)
    bitcoinPercentChange = round((100*(bitcoinDollarChange/stockClose)), 3)
    bitcoinPercentChangeStr = str(bitcoinPercentChange) + "%"
    return [bitcoinDollarChangeStr, bitcoinPercentChangeStr]
```
This was by far the most painstaking aspect of the project! So many functions were required to get the necessary information with the ease demonstrated in `main.py`. I used Finnhub's free data API as I didn't want to use up any live trading account API rate limits. For a free API, their scope of data offerings is quite impressive. 

The function `stockOvernightChange()` caused some issues. I found that it worked well on Tuesday, Wednesday, Thursday, and Friday, but not on any other day. Eventually I realized my mistake: the function calls data from the current day, the day before, and the day before that. Only on those four weekdays are all three of the necessary days market days! So the function had to be made conditional, using various `timedeltas` to gather data from the earliest market day. For example, on Monday, it will pull data from Monday, Friday, and Thursday, instead of Monday, Sunday, and Saturday, which simply wouldn't work (for U.S. equities data).

The crypto functions were surprisingly easy to create and test. I attribute this to the fact that they're open 24/7. One of the main challenges in collecting equities data was manipulating the time component of data requests. A Python newbie, the best I could come up with was converting to and back from UNIX time to get the data I wanted from Finnhub's API. Often, this didn't work as expected, but with regards to crypto, posed no challenges.

## covid.py

```python
import requests
from keys import *

api_key = covid_apiKey

def queryUrl(state):
    return f"http://api.covidactnow.org/v2/state/{state}.json?apiKey=" + api_key

class covidInfo:
    def __init__(self, state):
        # Infection Rate
        try:
            self.infRate = float(requests.get(queryUrl(state)).json()['metrics']['infectionRate'])
        except:
            self.infRate = "NaN"
        
        # Positive Rate
        try:
            self.posRate = round(100*float(requests.get(queryUrl(state)).json()['metrics']['testPositivityRatio']), 2)
        except:
            self.posRate = "NaN"
        
        # Vax Rate
        try:
            self.vaxRate = round(100*float(requests.get(queryUrl(state)).json()['metrics']['vaccinationsCompletedRatio']), 2)
        except:
            self.vaxRate = "NaN"
        
        # Free Bed Percentage
        try:
            self.freeBedPercentage = round(100*float(requests.get(queryUrl(state)).json()['actuals']['hospitalBeds']['currentUsageTotal'])/\
                float(requests.get(queryUrl(state)).json()['actuals']['hospitalBeds']['capacity']), 2)
        except:
            self.freeBedPercentage = "NaN"
        
        # New Cases
        try:
            self.newCases = int(requests.get(queryUrl(state)).json()['actuals']['newCases'])
        except:
            self.newCases = "NaN"

        # New Deaths
        try:
            self.newDeaths = int(requests.get(queryUrl(state)).json()['actuals']['newDeaths'])
        except:
            self.newDeaths = "NaN"
        
        # Covid Bed Percentage
        try:
            self.covidBedPercentage = round(100*float(requests.get(queryUrl(state)).json()['actuals']['hospitalBeds']['currentUsageCovid'])/\
                float(requests.get(queryUrl(state)).json()['actuals']['hospitalBeds']['capacity']), 2)
        except:
            self.covidBedPercentage = "NaN"
```

I directly stole this element from my previous project, wrapping COVID data from CovidActNow's exhaustive database. I posted my code for that project at [covidinfo.preritdas.com](http://covidinfo.preritdas.com). 

I recently altered the code to `try` each statistic as certain values would occasionally be unavailable and crash the entire program. In this way, if there is an exception in requesting the data, `self.statistic = "NaN"` and will appear as “NaN” in the text content.

## news.py

```python
import requests
from keys import newsAPIKey

usBusinessURL = 'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=' + newsAPIKey
usCOVIDURL = 'https://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=' + newsAPIKey

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
```

This script grabs news articles from the internet and returns them in a listed format. For example, `print(getFiveCOVIDArticles())` returns:

1. FDA considers limiting authorization of certain monoclonal antibody treatments - CNN 
2. Is Sneezing a Symptom of COVID? How to Tell the Difference Between the Virus, Allergies and Flu - NBC Chicago 
3. COVID-19 in pregnant women may trigger fetal inflammation - WJW FOX 8 News Cleveland 
4. Dirty keto Vs clean keto for weight loss: What is the difference? - Times of India 
5. COVID-19: how long is contagious period for Omicron, Delta? - Business Insider 

## weather.py

```python
import requests, json
from keys import *

api_key = openweather_apiKey

def requestUrl(city):
    return 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + openweather_apiKey

def kelvinToFarenheit(temperature):
    return round((temperature - 273.15)*(9/5) + 32)

def getTemperature(city):
    response = requests.get(requestUrl(city)).json()
    return round(kelvinToFarenheit(response["main"]["temp"]))

def getWeather(city):
    response = requests.get(requestUrl(city)).json()
    return str(response["weather"][0]["main"]) + ", " + str(response["weather"][0]["description"])
```
This was certainly the easiest part. Weather fetching is usually the first applied project of anyone first learning to use Python APIs, and for good reason! A few short functions here, OpenWeather API `request` calls there, and we were on our way.

## texts.py

```python
import nexmo
from keys import *

vonageClient = nexmo.Client(key=nexmo_key, secret=nexmo_secret)
sms = nexmo.Sms(vonageClient)
```

This initiates the texting client.

## requirements.txt

```python
certifi==2021.10.8
cffi==1.15.0
charset-normalizer==2.0.10
cryptography==36.0.1
DateTime==4.3
Deprecated==1.2.13
finnhub-python==2.4.7
idna==3.3
nexmo==2.5.2
pycparser==2.21
PyJWT==2.3.0
pytz==2021.3
requests==2.27.1
urllib3==1.26.8
wrapt==1.13.3
zope.interface==5.4.0
```

Many of these are directly used libraries, others are dependencies. With `pip3` or `python3`, these can be installed in a virtual environment or root python installation with the command: `python3 -m pip install -r requirements.txt`. 

---- 
If you're interested in setting this up yourself, building on it, or giving me some suggestions/improvements, please [contact me](https://preritdas.com/contact)!
