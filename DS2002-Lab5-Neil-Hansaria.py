#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 23:50:36 2022

@author: neilhansaria
"""

#Lab 5: Python Webscraping and MongoDB lab

import pandas as pd
import numpy as np
import json
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import sys

# Get longitude and longitude from Google Maps geocode

zip = input("Enter zipcode to get weather: ")
goog_req = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDMDGg3nHBmE_q0QpZobdYoXCUvMiC2NAU&components=postal_code:" + zip
goog = requests.get(goog_req)
soup_g = BeautifulSoup(goog.content, 'html.parser')
site_json=json.loads(soup_g.text)

try:
    lat = str(site_json['results'][0]['geometry']['location']['lat'])
    lng = str(site_json['results'][0]['geometry']['location']['lng'])
except:
    print("Error with zip. Please try again with another zip code.")
    sys.exit()


# Get data from weather wesbite using lat and lng
url = "https://forecast.weather.gov/MapClick.php?lat=" + lat + "&lon=" + lng
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

soup.find_all('img', class_='forecast-icon')

seven_day = soup.find(id="detailed-forecast-body")
forecast_labels = seven_day.find_all(class_="col-sm-2 forecast-label")
forecast_text = seven_day.find_all(class_="col-sm-10 forecast-text")

periods = [pt.get_text() for pt in forecast_labels]
descs = [pt.get_text() for pt in forecast_text]

#Get city name to display
city = soup.find(id="seven-day-forecast")
city1 = city.find_all(class_="panel-title")
city_list = [pt.get_text() for pt in city1]
print("7 Day Forecast For " + city_list[0].strip())
print("")

# Print the 7 day forecast
for i in range(0,len(periods)):
    print(periods[i] + ": ")
    print(descs[i])
    print("")



curr = soup.find(id="current_conditions_detail")
curr_conditions = curr.find_all("td")
curr1 = [pt.get_text() for pt in curr_conditions]

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

curr_dict = Convert(curr1)

#curr_dict['Last update'].strip()
print("Humidity: " + curr_dict['Humidity'])
print("Wind Speed: " + curr_dict['Wind Speed'])
print("Dewpoint: " + curr_dict['Dewpoint'])
print("Last Update: " + curr_dict['Last update'].strip())

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://hbk10871:DSISFUN@cluster0.4rxgntk.mongodb.net/test"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['weather']

dbname = get_database()
collection_name = dbname["weather_1"]

res = {periods[i]: descs[i] for i in range(len(periods))}
res['City'] = city_list[0].strip()
curr_dict1 = {'Humidity': curr_dict['Humidity'], "Wind Speed": curr_dict['Wind Speed'], "Dewpoint": curr_dict['Dewpoint'], "Last Update": curr_dict['Last update'].strip()}

collection_name.insert_many([res,curr_dict1])

