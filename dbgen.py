import sqlite3 as sl

con = sl.connect('meepybot.db')

with con:
  con.execute("""
  CREATE TABLE USER (id VARCHAR(20) NOT NULL PRIMARY KEY, value VARCHAR(50), datetime INTEGER);
  """)
