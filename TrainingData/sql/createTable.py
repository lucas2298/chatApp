import sqlite3
from employees import Employees

import json
with open('./TrainingData/sql/intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

def createTable():

    conn = sqlite3.connect('./TrainingData/database/chatbot.db')

    c = conn.cursor()

    c.execute("""drop table alltag""")
    c.execute("drop table traindata")
    
    # Create table alltag
    c.execute(
        """create table alltag(
            tag text primary key,
            description text,
            lock text,
            question text,
            private integer
        )"""
    )

    # Create table has all pattern and response
    c.execute(
        """create table traindata(
            tag text,
            patterns text,
            responses text,
            foreign key (tag) references alltag(tag)
        )"""
    )

    conn.commit()

    conn.close()

