import sqlite3
import nltk
from employees import Employees

import json
with open('./TrainingData/sql/intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

conn = sqlite3.connect('./TrainingData/database/chatbot.db')

table = conn.cursor()

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

conn.commit()

conn.close()

