import sqlite3
from employees import Employees

# conn = sqlite3.connect('employees.db')
conn = sqlite3.connect('./TrainingData/database/chatbot.db')

c = conn.cursor()

c.execute(
    """drop table employees
    """
)

c.execute(
    """create table employees(
        first text,
        last text,
        pay integer
    )"""
)

emps = {}

emps[0] = Employees('John', 'Doe', 100)
emps[1] = Employees('Via', 'Pi', 122)
emps[2] = Employees('ahihi', 'ahuhu', 111)
emps[3] = Employees('1', '2', 3)
emps[4] = Employees('1', '2', 3)

for i in emps:
    emp = emps[i]
    c.execute(
        "insert into employees values(?, ?, ?)", (emp.first, emp.last, emp.pay)
    )

hihi = "tag"

c.execute(
    "select * from " + hihi
)

print(c.fetchall())

conn.commit()

conn.close()

