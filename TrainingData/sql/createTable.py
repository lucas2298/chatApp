import sqlite3
from employees import Employees

import json
with open('./TrainingData/sql/intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

conn = sqlite3.connect('./TrainingData/database/chatbot.db')

c = conn.cursor()

c.execute("""drop table alltag""")
c.execute("""drop table greeting""")
c.execute("""drop table companyInformation""")
c.execute("""drop table advice""")
c.execute("""drop table recruitmentInformation""")
c.execute("""drop table fresherInternship""")
c.execute("""drop table fresherInformation""")
c.execute("""drop table noSendCV""")
c.execute("""drop table sendCV""")
c.execute("""drop table employees""")
c.execute("""drop table endConversation""")

# Create table with each 

# Create table alltag
c.execute(
    """create table alltag(
        tag text primary key,
        lock text,
        question text,
        private integer
    )"""
)

# tag: greeting
c.execute(
    '''create table greeting(
        patterns text primary key,
        responses text
    )'''
)
# tag: companyInformation
c.execute(
    '''create table companyInformation(
        patterns text primary key,
        responses text
    )'''
)
# tag: advice
c.execute(
    '''create table advice(
        patterns text primary key,
        responses text
    )'''
)
# tag: recruitmentInformation
c.execute(
    '''create table recruitmentInformation(
        patterns text primary key,
        responses text
    )'''
)
# tag: fresherInternship
c.execute(
    '''create table fresherInternship(
        patterns text primary key,
        responses text
    )'''
)
# tag: fresherInformation
c.execute(
    '''create table fresherInformation(
        patterns text primary key,
        responses text
    )'''
)
# tag: noSendCV
c.execute(
    '''create table noSendCV(
        patterns text primary key,
        responses text
    )'''
)
# tag: sendCV
c.execute(
    '''create table sendCV(
        patterns text primary key,
        responses text
    )'''
)
# tag: employees
c.execute(
    '''create table employees(
        patterns text primary key,
        responses text
    )'''
)
# tag: endConversation
c.execute(
    '''create table endConversation(
        patterns text primary key,
        responses text
    )'''
)

conn.commit()

conn.close()

