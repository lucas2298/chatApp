import sqlite3

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute(
    """create table employess(
        first text,
        last text,
        pay integer
    )""")
