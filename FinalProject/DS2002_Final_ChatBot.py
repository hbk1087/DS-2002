#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 00:46:32 2022

@author: neilhansaria
"""

import nltk 

nltk.download('punkt')
from nltk import word_tokenize,sent_tokenize

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
#read more on the steamer https://towardsdatascience.com/stemming-lemmatization-what-ba782b7c0bd8
import numpy as np 
import tflearn
import tensorflow as tf
import random
import json
import pickle
from pymongo import MongoClient
import pandas as pd



def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://hbk10871:DSISFUN@cluster0.4rxgntk.mongodb.net/test"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['DS2002Project2Final1']



dbname = get_database()
collection_name = dbname["Netflix"]




with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
               bag.append(1)
            else:
              bag.append(0)
    
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)
    
    with open("data.pickle","wb") as f:
        pickle.dump((words, labels, training, output), f)



net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)


def chat():
    print("Start talking with the bot! Ask a question!(type quit to stop)")
    print("Suggested questions: ")
    print("What were the top 5 shows on Netflix before 2000?")
    print("List the top movies on Netflix from France.")
    print("List all the shows on Netflix with a score above a 9.")
    print("What is the most popular genre of movies on Netflix?")
    print("What is the average number of seasons of top 25 shows?")
    print("What is the averague duration of Netflix shows from Japan? What is the averague duration of Netflix shows from the US?")
    print("List the movies on Netflix and the country they are from of the last 5 years")
    print("How long was the best movie on Netflix last year?")
    print("What was the top movie on Netflix in 2020?")
    print("What is the longest movie top movie on Netflix? What is the shortest?")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        result = model.predict([bag_of_words(inp, words)])[0]
        result_index = np.argmax(result)
        tag = labels[result_index]

        if result[result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
            if responses == "1":
                cursor = collection_name.find({"$and":[{"TYPE":"Show"},
                                  {"RELEASE_YEAR":{"$lt":2000}}]})
                count = 0
                while count < 5:
                    for record in cursor:
                        print(record['TITLE'])
                        count += 1
            elif responses == "2":
                cursor = collection_name.find({"$and":[{"TYPE":"Movie"},
                                  {"MAIN_PRODUCTION":"FR"}]})

                for record in cursor:
                    print(record['TITLE'])
            elif responses == "3":
                cursor = collection_name.find({"$and":[{"TYPE":"Show"},
                                  {"SCORE":{"$gt":8.9}}]})
                for record in cursor:
                    print(record['TITLE'])
            elif responses == "4":
                df = pd.DataFrame(list(collection_name.find()))
                df2 = df.groupby(['MAIN_GENRE'])['MAIN_GENRE'].count().sort_values(ascending=False)
                M = df2.max()
                q = df2[df2 == M].index[0]
                print("The most popular genre for movies on Netflix is " + q)
            elif responses == "5":
                df = pd.DataFrame(list(collection_name.find()))
                df1 = df[df['TYPE'] == "Show"].head(25)
                m = round(df1['NUMBER_OF_SEASONS'].mean())
                print("The average number of seasons for the top 25 shows on Netlifx is " + m)
            elif responses == "6":
                df = pd.DataFrame(list(collection_name.find()))
                df1 = df[df['TYPE'] == "Show"]
                dfj = df1[df1['MAIN_PRODUCTION'] == "JP"]
                dfu = df1[df1['MAIN_PRODUCTION'] == "US"]
                jm = dfj['DURATION'].mean()
                um = dfu['DURATION'].mean()
                print("The average duration for shows from Japan on Netlifx is " + str(jm) + " minutes")
                print("The average duration for shows from the US on Netlifx is " + str(um) + " minutes")
            elif responses == "7":
                df = pd.DataFrame(list(collection_name.find()))
                df1 = df[df['TYPE'] == "Movie"]
                df2 = df1[df1['RELEASE_YEAR'] >= 2018]
                
                for x in range(len(df2)):
                    print("Movie: " + df2.iloc[x,1] + ", Country: " + df2.iloc[x,6])
            elif responses == "8":
                df = pd.DataFrame(list(collection_name.find()))
                df1 = df[df['TYPE'] == "Movie"]
                df2 = df1[df1['RELEASE_YEAR'] == 2021]
                print("The movie " + df2.iloc[0, 1] + " has a duration of " + str(df2.iloc[0, 4] )+ " minutes")
            elif responses == "9":
                df = pd.DataFrame(list(collection_name.find()))
                df1 = df[df['TYPE'] == "Movie"]
                df2 = df1[df1['RELEASE_YEAR'] == 2020]
                print("The top movie on Netflix in 2020 was: " + df2.iloc[0, 1])
            elif responses == "10":
                df = pd.DataFrame(list(collection_name.find()))
                df1 = df[df['TYPE'] == "Movie"]
                df2 = df1.sort_values(['DURATION'], ascending=False)
                print("The longest top movie on Netflix was: " + df2.iloc[0, 1] + " with a duration of " + str(df2.iloc[0, 4]) + " minutes")
                print("The shortest top movie on Netflix was: " + df2.iloc[len(df2)-1, 1] + " with a duration of " + str(df2.iloc[len(df2)-1, 4]) + " minutes")
                
                

        else:
            print("I didnt get that. Can you try one of the questions in the correct format. Here are some suggestions")
            print("What were the top 5 shows on Netflix before 2000?")
            print("List the top movies on Netflix from France.")
            print("List all the shows on Netflix with a score above a 9.")
            print("What is the most popular genre of movies on Netflix?")
            print("What is the average number of seasons of top 25 shows?")
            print("What is the averague duration of Netflix shows from Japan? What is the averague duration of Netflix shows from the US?")
            print("List the movies on Netflix and the country they are from of the last 5 years")
            print("How long was the best movie on Netflix last year?")
            print("What was the top movie on Netflix in 2020?")
            print("What is the longest movie top movie on Netflix? What is the shortest?")
chat()
