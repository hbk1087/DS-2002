import os
import json
import pprint
import requests
import yfinance as yf
import requests.exceptions
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import time


x = input("Enter stock ticker symbol: ")

nameurl = 'https://query1.finance.yahoo.com/v7/finance/quote'
querystring = {"symbols": x}

url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/"

header_var ={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.request("GET",nameurl, headers=header_var,params=querystring)
stock_json = response.json()

query_str = {"symbol": x, "modules":"defaultKeyStatistics"}
response2 = requests.request("GET",url, headers=header_var,params=query_str)
stock_json2 = response2.json()

query_str3 = {"symbol": x, "modules":"financialData"}
response3 = requests.request("GET",url, headers=header_var,params=query_str3)
stock_json3 = response3.json()


nameticker = stock_json['quoteResponse']['result'][0]['symbol']
fullname = stock_json['quoteResponse']['result'][0]['longName']
curr_price = stock_json3['quoteSummary']['result'][0]['financialData']['currentPrice']['fmt']
tar_meanprice = stock_json3['quoteSummary']['result'][0]['financialData']['targetMeanPrice']['fmt']
total_cash = stock_json3['quoteSummary']['result'][0]['financialData']['totalCash']['fmt']
profit_margin = stock_json2['quoteSummary']['result'][0]['defaultKeyStatistics']['profitMargins']['fmt']

today = dt.datetime.now()
d = dt.timedelta(days = 5)
a = today - d
d4 = today.strftime("%b-%d-%Y")
a4 = a.strftime("%b-%d-%Y")



final = {}
final['Name Ticker'] = nameticker
final['Full Name of Stock'] = fullname
final['Current Price'] = curr_price
final['Target Mean Price'] = tar_meanprice
final['Cash on Hand'] = total_cash
final['Profit Margins'] = profit_margin
final["Date Pulled"] = d4

print('Name Ticker: ' + nameticker)
print('Full Name of Stock: ' + fullname)
print('Current Price: ' + curr_price)
print('Target Mean Price: ' + tar_meanprice)
print('Cash on Hand: '+ total_cash)
print('Profit Margins: ' + profit_margin)



with open('mydata.json', 'w') as f:
    json.dump(final, f)


graphurl = 'https://query1.finance.yahoo.com/v7/finance/chart/'
query_str4 = {"symbol": x, 'range': "5d", "interval": "1d", "metrics": "high"}
response4 = requests.request("GET",graphurl, headers=header_var,params=query_str4)
stock_json4 = response4.json()

dates = stock_json4['chart']['result'][0]['timestamp']
dates1 = [dt.datetime.fromtimestamp(date) for date in dates]
dates2 = [date.strftime("%b-%d-%Y") for date in dates1]

#print(dt.datetime(dates1[0]))
prices = stock_json4['chart']['result'][0]['indicators']['quote'][0]['high']

print(prices)
print(dates2)

fig, ax = plt.subplots(figsize=(12,12))

# Add x-axis and y-axis
ax.plot(dates1,
       prices,
       color='green')

# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Price",
       title="Prices over Last 5 days of " + fullname)

plt.show()
