import sqlite3 as sl
from os.path import exists
if(not exists("quizhistory.db")):
    con = sl.connect('quizhistory.db')
    with con:
        con.execute("""
            CREATE TABLE USER (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                qid INTEGER,
                var TEXT,
                right INTEGER
            );
        """)
