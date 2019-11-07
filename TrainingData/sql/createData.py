import sqlite3
from employees import Employees

import json
with open('./TrainingData/sql/intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

conn = sqlite3.connect('./TrainingData/database/chatbot.db')

c = conn.cursor()

# Push data to table

# Push data to alltag
for intent in intents['intents']:
    c.execute(
        "insert into alltag values(:tag, :description, :lock, :question, :private)", {'tag': intent['tag'], 'description': intent['description'], 'lock': intent['lock'], 'question': intent['question'], 'private': intent['privateOnly']}
    )

# Push data to every tag in alltag
# for intent in intents['intents']:
#     p = []
#     r = []
#     q = []
#     s = []
#     for pattern in intent['patterns']:
#         p.append(pattern)
#     for response in intent['responses']:
#         r.append(response)
#     for question in intent['question']:
#         q.append(question)
#     for select in intent['selectList']:
#         s.append(select)

#     lenMax = max(len(p), len(r), len(q), len)

#     while len(p) < len(r):
#         p.append("")
#     while len(p) > len(r):
#         r.append("")
#     for i in range(0, len(p)):
#         c.execute(
#             "insert into "+intent['tag']+" values(:patterns, :responses)", {'patterns': p[i], 'responses': r[i]}
#         )
    

conn.commit()

conn.close()