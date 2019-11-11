#!/usr/bin/python
# -*- coding: utf8 -*-

#Retore all of our data structures
import pickle
data = pickle.load(open("./Server/traindatas/training_data", "rb"))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

#Load our saved model
import tflearn
import tensorflow as tf
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy')

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='./Server/traindatas/tflearn_logs')

model.load('./Server/traindatas/model.tflearn')

import inputProcessing
import random

ERROR_THRESHOLD = 0.25
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([inputProcessing.bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

locks = {}

# Database
import sqlite3
conn = sqlite3.connect('./Server/database/chatbot.db', check_same_thread=False)
table = conn.cursor()
table.execute(
    "select * from alltag"
)
temp = table.fetchall()
# All tag
tag = []
lock = []
question = []
privateOnly = []
response = []
for i in temp:
    tag.append(i[0])
    lock.append(i[2])
    question.append(i[3])
    privateOnly.append(i[4])
    response.append(i[5])

def responses(sentence, userID, show_details=False):
    results = classify(sentence)
    if not userID in locks:
        locks[userID] = ''
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        for lenRes in range(0, len(results)):
            for i in range(0, len(tag)):
                # find a tag matching the first result
                if tag[i] == results[lenRes][0]:
                    # Kiem tra tinh trang lock
                    if locks[userID] == '':
                        if privateOnly[i] == "no":
                            # Them lock cho user
                            locks[userID] = lock[i]
                            # Tra ket qua
                            data = []
                            data.append(response[i])
                            table.execute(
                                "select selects from selectlist "
                                "where tag = :tag", {'tag': tag[i]}
                            )
                            selectList = table.fetchall()
                            for s in selectList:
                                data.append(s[0])
                            if question[i] != "":
                                data.append(question[i]+'+')
                            return data
                    else:
                        table.execute(
                            "select key from key "
                            "where tag = :tag", {'tag': tag[i]}
                        )
                        temp = table.fetchall()
                        for key in temp:
                            if locks[userID] == key[0]:
                                data = []
                                data.append(response[i])
                                table.execute(
                                    "select selects from selectlist "
                                    "where tag = :tag", {'tag': tag[i]}
                                )
                                selectList = table.fetchall()
                                for s in selectList:
                                    data.append(s[0])
                                if question[i] != "":
                                    data.append(question[i]+'+')
                                return data
                    break
            for i in range(0, len(tag)):
                # find a tag matching the first result
                if tag[i] == results[lenRes][0]:
                    if privateOnly[i] == "no":
                        # Them lock cho user
                        locks[userID] = lock[i]
                        # Tra ket qua
                        data = []
                        data.append(response[i])
                        table.execute(
                            "select selects from selectlist "
                            "where tag = :tag", {'tag': tag[i]}
                        )
                        selectList = table.fetchall()
                        for s in selectList:
                            data.append(s[0])
                        if question[i] != "":
                            data.append(question[i]+'+')
                        return data
                    break

conn.commit()
# conn.close()