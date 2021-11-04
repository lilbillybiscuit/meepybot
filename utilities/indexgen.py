import sqlite3 as sl

con = sl.connect('../meepybot.db')

data=[
  ("vote_threshold", 6),
  ("vote_timeout", 300)
]

with con:
  con.executemany("INSERT INTO USER (id, value) values (?,?)", data)