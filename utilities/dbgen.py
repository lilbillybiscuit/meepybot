import sqlite3 as sl

con = sl.connect('meepybot.db')

with con:
  try:
    con.execute("CREATE TABLE USER (id VARCHAR(20) NOT NULL PRIMARY KEY, value VARCHAR(50), datetime INTEGER);")
  except:
    print("Error handling database")
  try:
    con.execute("CREATE TABLE reqs (id INTEGER, action VARCHAR(100), datetime INTEGER)")
  except:
    print("Error handling database")

data=[
  ("vote_threshold", 6),
  ("vote_timeout", 300)
]

with con:
  con.executemany("INSERT INTO USER (id, value) values (?,?)", data)