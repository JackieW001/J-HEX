import json, requests, urllib2
import random
import datetime
from requests.auth import HTTPBasicAuth


def get_info():
    keyfile = open("keys.txt", "r")
    av_key = keyfile.readline().replace("\n", "").replace("\r", "")


    link = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=" + av_key

    u = urllib2.urlopen(link)
    
    info = u.read()
    
    results = json.loads(info)
    return results
#return json.dumps(results, indent=4)

def get_date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    current = str(year) + "-" + str(month) + "-" + str(day)
    return current

def get_today():
    info = get_info()
    return info["Time Series (Daily)"]["2018-05-17"]#[get_date()]

#print(get_info());
#print(get_date());
print(get_today());
'''
search_results = search_results["results"]["trackmatches"]["track"]

print artist.upper()

results = requests.get(link)
print results
'''
