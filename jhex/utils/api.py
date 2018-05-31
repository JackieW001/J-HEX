import json, requests, urllib2, random, datetime, pprint, os
from requests.auth import HTTPBasicAuth

DIR = os.path.dirname(__file__) or '.'
DIR += '/../keys.txt'

def get_apikey():
    keyfile = open(DIR, "r")
    av_key = keyfile.readline().replace("\n", "").replace("\r", "")
    return av_key

#takes ticker
#returns dictionary of data with key being date Y-M-D and value being a dict of data
def get_info(ticker, time_frame):
    uv = get_apikey()
    link = "https://www.alphavantage.co/query?function=" + time_frame + "&symbol=" + ticker + "&apikey=" + uv
    u = urllib2.urlopen(link)
    info = u.read()
    results = json.loads(info)
    return results

#takes in a ticker and a date
#returns stock market data from a specific date
def get_date(ticker, date):
    info = get_info(ticker, "TIME_SERIES_DAILY")
    return info["Time Series (Daily)"][date]

#takes in a ticker
#returns live stock market data for today
def get_today(ticker):
    today = '{:%Y-%m-%d}'.format(datetime.date.today())
    #print today
    return get_date(ticker, today)

#takes ticker
#returns the dict of the last 7 days w/ key being date and value being data
def get_last_days(ticker, time_frame, num_dates):
    time_frame2 = ""
    if time_frame == "TIME_SERIES_DAILY":
        time_frame2 = "Time Series (Daily)"
    elif time_frame == "TIME_SERIES_WEEKLY":
        time_frame2 = "Weekly Time Series"
    elif time_frame == "TIME_SERIES_MONTHLY":
        time_frame2 = "Monthly Time Series"
    info = get_info(ticker, time_frame)[time_frame2]
    sorted_dict = sorted(info)
    #return sorted_dict
    length = len(sorted_dict)
    dates = sorted_dict[length - num_dates:length]
    retVal = {}
    for x in dates:
        retVal[x] = info[x]
    return retVal

'''
#takes in a string
#if length > 2, add a leading 0 
def add_zero(strg):
    if len(strg) < 2:
        return "0" + strg
    else:
        return strg
'''

pp = pprint.PrettyPrinter(indent=4)

#print(get_info('MSFT', "TIME_SERIES_DAILY"))
#print(get_date('MSFT', '2018-05-14'))
#print(get_today('MSFT'))
#pp.pprint(get_last_days("MSFT", "TIME_SERIES_DAILY", 7))
#pp.pprint(get_last_days("MSFT", "TIME_SERIES_WEEKLY", 8))
#pp.pprint(get_last_days("MSFT", "TIME_SERIES_MONTHLY", 12))
#print add_zero("05")
