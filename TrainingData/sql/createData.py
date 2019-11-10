import sqlite3

import json
with open('./TrainingData/sql/intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

from createTable import createTable

createTable()

conn = sqlite3.connect('./TrainingData/database/chatbot.db')

c = conn.cursor()

# Push data to table

# Push data to alltag
for intent in intents['intents']:
    c.execute(
        "insert into alltag values(:tag, :description, :lock, :question, :private)", {'tag': intent['tag'], 'description': intent['description'], 'lock': intent['lock'], 'question': intent['question'], 'private': intent['privateOnly']}
    )

# Push data to every tag in alltag
for intent in intents['intents']:
    p = []
    r = []
    for pattern in intent['patterns']:
        p.append(pattern)
    for response in intent['responses']:
        r.append(response)

    while len(p) < len(r):
        p.append("")
    while len(p) > len(r):
        r.append("")
    for i in range(0, len(p)):
        c.execute(
            "insert into traindata values(:tag, :patterns, :responses)", {'tag': intent['tag'],'patterns': p[i], 'responses': r[i]}
        )
    

conn.commit()

conn.close()