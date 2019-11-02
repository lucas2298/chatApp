import sqlite3
from employees import Employees

import json
with open('./TrainingData/sql/intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

conn = sqlite3.connect('./TrainingData/database/chatbot.db')

c = conn.cursor()

c.execute("""drop table tag""")
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


c.execute(
    """create table tag(
        tag text primary key,
        lock text
    )"""
)

# Create table tag
for intent in intents['intents']:
    c.execute(
        "insert into tag values(?, ?)", (intent['tag'], intent['lock'])
    )

# Create table with each tag
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
    '''create table companyInformation(
        patterns text,
        responses text,
        key text,
        privateOnnly integer
    )'''
)
# tag: advice
c.execute(
    '''create table advice(
        patterns text,
        responses text,
        key text,
        privateOnnly integer
    )'''
)
# tag: recruitmentInformation
c.execute(
    '''create table recruitmentInformation(
        patterns text,
        responses text,
        key text,
        privateOnnly integer
    )'''
)
# tag: fresherInternship
c.execute(
    '''create table fresherInternship(
        patterns text,
        responses text,
        key text,
        privateOnnly integer
    )'''
)
# tag: fresherInformation
c.execute(
    '''create table fresherInformation(
        patterns text,
        responses text,
        key text,
        privateOnnly integer
    )'''
)
# tag: noSendCV
c.execute(
    '''create table noSendCV(
        patterns text,
        responses text,
        key text,
        privateOnnly integer
    )'''
)
# tag: sendCV
c.execute(
    '''create table sendCV(
        patterns text,
        responses text,
        key text,
        privateOnnly integer
    )'''
)
# tag: employees
c.execute(
    '''create table employees(
        patterns text,
        responses text,
        key text,
        privateOnnly integer
    )'''
)
# tag: endConversation
c.execute(
    '''create table endConversation(
        patterns text,
        responses text,
        key text,
        privateOnnly integer
    )'''
)

# Push data to table
for intent in intents['intents']:
    if (intent['tag'] == 'greeting'):
        for pattern in intent['patterns']:
            c.execute(
                "insert into greeting(patterns) values(:patterns)", {'patterns': pattern}
            )
        for response in intent['responses']:
            c.execute(
                "insert into greeting(responses) values(:responses)", {'responses': response}
            )
        break

conn.commit()

conn.close()

