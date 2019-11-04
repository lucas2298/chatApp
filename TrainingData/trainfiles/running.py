#!/usr/bin/python
# -*- coding: utf8 -*-

#Retore all of our data structures
import pickle
data = pickle.load(open("./TrainingData/trainfiles/training_data", "rb"))
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
model = tflearn.DNN(net, tensorboard_dir='./TrainingData/trainfiles/tflearn_logs')

model.load('./TrainingData/trainfiles/model.tflearn')

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

lock = {}

# def response(sentence, userID, show_details=False):
#     results = classify(sentence)
#     if not userID in lock:
#         lock[userID] = 'close'
#     # if we have a classification then find the matching intent tag
#     if results:
#         print(results)
#         # loop as long as there are matches to process
#         for lenRes in range(0, len(results)):
#             for i in intents['intents']:
#                 # find a tag matching the first result
#                 print(lock[userID])
#                 print(i['key'])
#                 print("\n")
#                 if i['tag'] == results[lenRes][0]:
#                     # Kiem tra tinh trang lock
#                     if lock[userID] == 'close':
#                         if i['privateOnly'] == "no":
#                             # Them lock cho user
#                             lock[userID] = i['lock']
#                             # Tra ket qua
#                             data = []
#                             data.append(random.choice(i['responses']))
#                             for s in i['selectList']:
#                                 data.append(s)
#                             if i['question'] != "":
#                                 data.append(i['question']+'+')
#                             return data
#                     else:
#                         if lock[userID] in i['key']:
#                             data = []
#                             data.append(random.choice(i['responses']))
#                             for s in i['selectList']:
#                                 data.append(s)
#                             if i['question'] != "":
#                                 data.append(i['question']+'+')
#                             lock[userID] = i['lock']                            
#                             return data
#                     break
#             for i in intents['intents']:
#                 # find a tag matching the first result
#                 if i['tag'] == results[lenRes][0]:
#                     if i['privateOnly'] == "no":
#                         # Them lock cho user
#                         lock[userID] = i['lock']
#                         # Tra ket qua
#                         data = []
#                         data.append(random.choice(i['responses']))
#                         for s in i['selectList']:
#                             data.append(s)
#                         if i['question'] != "":
#                             data.append(i['question']+'+')
#                         return data
#                     break