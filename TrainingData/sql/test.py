import sqlite3
from employees import Employees

import json
with open('./TrainingData/sql/intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

conn = sqlite3.connect('./TrainingData/database/chatbot.db')

table = conn.cursor()

table.execute(
    'select tag from alltag'
)
alltag = table.fetchall()
print(alltag)

for i in alltag:
    tag = i[0]
    print(tag)
    table.execute(
        'select patterns from '+tag
    )
    temp = table.fetchall()
    print(temp)
    for tmp in temp:
        print(tmp[0])
    break
    

conn.commit()

conn.close()

