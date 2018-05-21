import json, requests, urllib2
import random
import datetime
from requests.auth import HTTPBasicAuth

def get_apikey():
    keyfile = open("keys.txt", "r")
    av_key = keyfile.readline().replace("\n", "").replace("\r", "")
    return av_key

#takes in ticker
#returns stock market data from api
def get_info(ticker):
    av_key = get_apikey()

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
    print today
    return get_date(ticker, today)

#takes in a string
#if length > 2, add a leading 0 
def add_zero(strg):
    if len(strg) < 2:
        return "0" + strg
    else:
        return strg
    
#takes in a ticker, month, year
#month and year are ints
#returns a dict of data
'''
def get_month(ticker, month, year):
    num_days = 0
    list_data = {}
    if month == 4 or month == 6 or month == 9 or month == 11:
        num_days = 30
    elif month == 2:
        num_days = 28
    else:
        num_days = 31
    for x in xrange(4):
        curr_day = x + 1
        curr_date = str(year) + "-" + add_zero(str(month)) + "-" + add_zero(str(curr_day))
        #print curr_date

        list_data[curr_date] = get_date(ticker, curr_date)
        #list_data.append(get_date(ticker, curr_date))

    return list_data
        
    #curr_day = '{:%Y-%m-%d}'.format(datetime.date.today())
    #return get_date(ticker, today)
'''

#takes ticker
#returns dictionary of data with key being date Y-M-D and value being a dict of data
def get_last_month_info(ticker):
    uv = get_apikey()
    
    link = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&apikey=" + uv
    
    u = urllib2.urlopen(link)
    
    info = u.read()
    
    results = json.loads(info)
    
    return results["Time Series (Daily)"]

def get_last_month(ticker):
    info = get_last_month_info(ticker)
    sorted_dict = sorted(info)
    return sorted_dict
    #print info.keys()

#print(get_info('MSFT'))
#print(get_date('MSFT', '2018-05-14'))
#print(get_today('MSFT'))
print(get_last_month("MSFT"))
#print add_zero("05")
