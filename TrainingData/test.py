import sqlite3
from employees import Employees

import json
with open('intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

conn = sqlite3.connect('./database/chatbot.db')

c = conn.cursor()

c.execute("""drop table tag""")
c.execute("""drop table greeting""")

c.execute(
    """create table tag(
        tag text primary key,
        lock text
    )"""
)

emps = {}

for intent in intents['intents']:
    c.execute(
        "insert into tag values(?, ?)", (intent['tag'], intent['lock'])
    )

# tag: greeting
c.execute(
    '''create table greeting(
        patterns text,
        responses text,
        key text,
        privateOnnly integer
    )'''
)
# tag: companyInformation
c.execute(
    '''create table greeting(
        patterns text,
        responses text,
        key text,
        privateOnnly integer
    )'''
)


for intent in intents['intents']:
    if (intent['tag'] == 'greeting'):
        for pattern in intent['patterns']:
            c.execute(
                "insert into greeting(patterns) values(:patterns)", {'patterns': pattern}
            )
        break

conn.commit()

conn.close()

