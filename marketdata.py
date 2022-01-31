import finnhub
import time
from datetime import date, timedelta
from datetime import datetime as dt
import requests
from keys import finnhub_apiKey

fc = finnhub.Client(api_key=finnhub_apiKey)

def stockOvernightChange(symbol):
    try:
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
    except:
        print(f"Issue compiling {symbol = }")

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