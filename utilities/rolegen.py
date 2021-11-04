import sqlite3 as sl
import discord



con = sl.connect('../meepybot.db')

drop = False
try:
  nothing=2
  with con:
    con.execute("DROP TABLE roles")
except:
  print("Error dropping table")

with con:
  con.execute("CREATE TABLE ROLES (name VARCHAR(40) NOT NULL PRIMARY KEY, id VARCHAR(50), datetime INTEGER);")
