import sqlite3
from employees import Employees

import json
with open('./TrainingData/sql/intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

def createTable():

    conn = sqlite3.connect('./TrainingData/database/chatbot.db')

    c = conn.cursor()

    c.execute("drop table alltag")
    c.execute("drop table patterns")
    c.execute("drop table selectlist")
    c.execute("drop table key")
    
    # Create table alltag
    c.execute(
        """create table alltag(
            tag text primary key,
            description text,
            lock text,
            question text,
            private integer,
            response text
        )"""
    )

    # Create table has all pattern
    c.execute(
        """create table patterns(
            tag text,
            patterns text,
            foreign key (tag) references alltag(tag)
        )"""
    )
    # Create table has all select list
    c.execute(
        """create table selectlist(
            tag text,
            selects text,
            foreign key (tag) references alltag(tag)
        )"""
    )
    # Create table has all key
    c.execute(
        """create table key(
            tag text,
            key text not null,
            foreign key (tag) references alltag(tag)
        )"""
    )

    conn.commit()

    conn.close()
createTable()