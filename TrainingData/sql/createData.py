import pymysql

db = pymysql.connect("localhost", "root", "", "chatbot")

import json
with open('./TrainingData/sql/intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

from createTable import createTable

createTable()

table = db.cursor()

# Push data to table

# Push data to alltag
for intent in intents['intents']:
    sql = "insert into alltag values(%s, %s, %s, %s, %s, %s)"
    table.execute(sql, (intent['tag'], intent['description'], intent['lock'], intent['question'], intent['privateOnly'], intent['responses']))

# Push data to every tag in alltag
for intent in intents['intents']:
    sql = "insert into patterns(tag, patterns) values(%s, %s)"
    for pattern in intent['patterns']:
        table.execute(sql, (intent['tag'], pattern))
        
    sql = "insert into selectlist(tag, selects) values(%s, %s)"
    for s in intent['selectList']:
        table.execute(sql, (intent['tag'], s))

    sql = "insert into keyunlock(tag, keyUnlock) values(%s, %s)"
    for key in intent['key']:
        if key != "":
            table.execute(sql, (intent['tag'], key))

db.commit()
db.close()