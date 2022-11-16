# Cryptocurrency Midterm Project 1

import json
import pandas as pd
import requests
import numpy as np
import os

try:
    !pip install opendatasets
except:
    "Error installing package. Please do 'pip install opendatasets' in your terminal"
import opendatasets as od
from pathlib import Path
import sqlite3


# Download the data directly from Kaggle
### ---- When prompted for username, enter: neilhansaria
### ---- When prompted for key, enter: 7802e1a1e16e2061e9ca28cd2a9105ef
od.download("https://www.kaggle.com/datasets/maharshipandya/-cryptocurrency-historical-prices-dataset", force=True)


# Convert csv to dataframe for easy data processing
path = os.getcwd()
path1 = path + "/-cryptocurrency-historical-prices-dataset/dataset.csv"
try:
    data = pd.read_csv(path1)
except:
    print("File not found")
    
    
# Asks the user for the type of conversion, if wanted
inp1 = ''
conn = None
to_j = None
def inp():
    inp1 = input("The data is in csv format. Would you like to convert it to another type. Press y for yes and n for no: ")

    if inp1 == 'y':
        inp2 = input("Press s for SQL or j for JSON: ")
        if inp2 == 's':
            Path('my_data.db').touch()
            conn = sqlite3.connect('my_data.db')
            c = conn.cursor()
            data.to_sql('data', conn, if_exists='append', index = False)
            return 's'
        elif inp2 == 'j':
            to_j1 = data.to_json()
            with open('my_data.json', 'w', encoding='utf-8') as f:
                json.dump(to_j1, f, ensure_ascii=False, indent=4)
            
            return 'j'
        else:
            print("Error! Input valid type")
            inp()
    elif inp1 == 'n':
        return 'n'
    else:
        print("Error! Input valid answer")
        inp()
            
decision = inp()

# Modifies the data by adding a percent change column
data['percent_change'] = (((data['open'] - data['close'])/data['open'])*100)
data1 = data.round({'percent_change': 2})


# Writes converted data to disk 
if decision == 's':
    conn = sqlite3.connect('my_data.db')
    c = conn.cursor()
    data1.to_sql('data1', conn, if_exists='replace', index = False)

if decision == 'j':
    to_j1 = data1.to_json()
    with open('my_data_mod.json', 'w', encoding='utf-8') as f:
        json.dump(to_j1, f, ensure_ascii=False, indent=4)


# Summary of the data ingestion
rows = len(data1.axes[0])
cols = len(data1.axes[1])
print("")
print("The data is first downloaded from Kaggle and saved directly onto the user's disk. The user is then asked " +
     "whether or not to convert the data to a different type, after which it is converted and then stored on " +
     "the local disk. Then, the data is modified to add another column, and stored on the local disk. " + 
     "This modified data has " + str(rows) + " records and " + str(cols) + " columns.")
