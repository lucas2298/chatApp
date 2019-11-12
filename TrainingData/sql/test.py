#!/usr/bin/python
# -*- coding: utf8 -*-

#import algorithm
import numpy as np
import random

#import NLP lib
import tflearn
import tensorflow as tf
import nltk 
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

#Loading data training

import pymysql

db = pymysql.connect("localhost", "root", "", "chatbot")

#Classification
words = [] #All word in every sentence
classes = []
documents = []
stop_words = ['?', '.', ',']

table = db.cursor()

table.execute(
    'select tag, patterns from patterns'
)
data = table.fetchall()

for i in data:
	tag = i[0]
	pattern = i[1]
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

print(classes)