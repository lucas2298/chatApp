import pymysql

db = pymysql.connect("localhost", "root", "", "chatbot")

table = db.cursor()

def createTable():

    table.execute("drop table keyunlock")
    table.execute("drop table selectlist")
    table.execute("drop table patterns")
    table.execute("drop table alltag")

    # Create table alltag
    table.execute(
        """create table alltag(
            tag varchar(32) primary key,
            description varchar(255),
            locks varchar(32),
            question varchar(255),
            private varchar(3),
            response varchar(255))"""
    )

    # Create table has all pattern
    table.execute(
        """create table patterns(
            id int not null auto_increment primary key,
            tag varchar(32),
            patterns varchar(255),
            foreign key (tag) references alltag(tag)
        )"""
    )
    # Create table has all select list
    table.execute(
        """create table selectlist(
            id int not null auto_increment primary key,
            tag varchar(32),
            selects varchar(255),
            foreign key (tag) references alltag(tag)
        )"""
    )
    # Create table has all key
    table.execute(
        """create table keyunlock(
            id int not null auto_increment primary key,
            tag varchar(32),
            keyUnlock varchar(32),
            foreign key (tag) references alltag(tag)
        )"""
    )

createTable()