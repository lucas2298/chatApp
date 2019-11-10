#!/usr/bin/python
# -*- coding: utf8 -*-

#import algorithm
import numpy as np
import random
import sqlite3

#import NLP lib
import tflearn
import tensorflow as tf
import nltk 
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

#Loading data training

conn = sqlite3.connect('./TrainingData/database/chatbot.db')

#Classification
words = [] #All word in every sentence
classes = []
documents = []
stop_words = ['?', '.', ',']

table = conn.cursor()

table.execute(
    'select tag from alltag'
)
alltag = table.fetchall()

for i in alltag:
    tag = i[0]
    table.execute(
        "select patterns from traindata "
        "where tag = :tag", {'tag': tag}
    )
    patterns = table.fetchall()
    for j in patterns:
    	pattern = j[0]
    	w = nltk.word_tokenize(pattern)
    	words.extend(w)
    	documents.append((w, tag))
    classes.append(tag)

#Stem and lower word, but we are using vietnamese language so we only lowercase them
words = [w.lower() for w in words if w not in stop_words]
#Remove duplicates words
words = sorted(list(set(words)))
#remove duplicates classes
classes = sorted(list(set(classes)))

#Create training data
training = []
output = []
#Create an empty array for our output
output_empty = [0]*len(classes)

#Training set, bag of words for each sentence
for doc in documents:
	#Initialize our bag of words
	bag = []
	#List of tokenized words for the pattern
	pattern_words = doc[0]
	#Stem each word
	# pattern_words = [stemmer.stem(w.lower()) for w in pattern_words]
	#Create bag of words array
	for w in words:
		bag.append(1) if w in pattern_words else bag.append(0)
	#Output is a '0' for each tag and '1' for current tag
	output_row = list(output_empty)
	output_row[classes.index(doc[1])] = 1
	training.append([bag, output_row])

#Shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)

#Create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])

# reset underlying graph data
tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy')

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='./TrainingData/trainfiles/tflearn_logs')
# Start training (apply gradient descent algorithm)
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('./TrainingData/trainfiles/model.tflearn')

# save all of our data structures
import pickle
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "./TrainingData/trainfiles/training_data", "wb" ) )

conn.commit()

conn.close()