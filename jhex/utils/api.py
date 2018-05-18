import json, requests, urllib2
import random
import datetime
from requests.auth import HTTPBasicAuth

#takes in ticker
#returns stock market data from api
def get_info(ticker):
    keyfile = open("keys.txt", "r")
    av_key = keyfile.readline().replace("\n", "").replace("\r", "")


    link = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&apikey=" + av_key

    u = urllib2.urlopen(link)
    
    info = u.read()
    
    results = json.loads(info)
    return results
#return json.dumps(results, indent=4)

#takes in a ticker and a date
#returns stock market data from a specific date
def get_date(ticker, date):
    info = get_info(ticker)
    return info["Time Series (Daily)"][date]

#takes in a ticker
#returns live stock market data for today
def get_today(ticker):
    today = '{:%Y-%m-%d}'.format(datetime.date.today())
    return get_date(ticker, today)

print(get_info('MSFT'));
#print(get_date('MSFT', '2018-05-17'));
#print(get_today('MSFT'));
