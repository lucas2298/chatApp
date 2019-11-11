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
        "insert into alltag values(:tag, :description, :lock, :question, :private, :response)", {'tag': intent['tag'], 'description': intent['description'], 'lock': intent['lock'], 'question': intent['question'], 'private': intent['privateOnly'], 'response': intent['responses']}
    )

# Push data to every tag in alltag
for intent in intents['intents']:
    for pattern in intent['patterns']:
        c.execute(
            "insert into patterns values(:tag, :patterns)", {'tag': intent['tag'], 'patterns': pattern}
        )
        
    for s in intent['selectList']:
        c.execute(
            "insert into selectlist values(:tag, :select)", {'tag': intent['tag'], 'select': s}
        )
    for key in intent['key']:
        if key != "":
            c.execute(
                "insert into key values(:tag, :key)", {'tag': intent['tag'], 'key': key}
            )

conn.commit()

conn.close()