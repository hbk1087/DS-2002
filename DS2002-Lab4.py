#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 22:12:48 2022

@author: neilhansaria
"""

import os
import json
import pprint
import requests
import yfinance as yf
import requests.exceptions
import pandas as pd

def get_api_response(url, response_type):
    try:
        response = requests.get(url)
        response.raise_for_status()
    
    except requests.exceptions.HTTPError as errh:
        return "An Http Error occurred: " + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred: " + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred: " + repr(errt)
    except requests.exceptions.RequestException as err:
        return "An Unknown Error occurred: " + repr(err)

    if response_type == 'json':
        result = json.dumps(response.json(), sort_keys=True, indent=4)
    elif response_type == 'dataframe':
        result = pd.json_normalize(response.json())
    else:
        result = "An unhandled error has occurred!"
        
    return result

def get_api_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    
    except requests.exceptions.HTTPError as errh:
        return "An Http Error occurred: " + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred: " + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred: " + repr(errt)
    except requests.exceptions.RequestException as err:
        return "An Unknown Error occurred: " + repr(err)
        
    return response.json()

x = input("Enter stock ticker: ")

nameurl = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=" + x

url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + x

#print(nameurl)
data1 = yf.Ticker(x)
data = yf.download(x, start="2020-10-01", end="2022-10-14")

#data1.to_csv("/Users/neilhansaria/Downloads/data1dslab4.csv")

#n1 = get_api_data(url)

data1.info()