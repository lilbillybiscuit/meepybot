import sqlite3 as sl

con = sl.connect('meepybot.db')
"""
with con:
  data = con.execute("SELECT * FROM USER where id = :key", {"key": "vote_timeout"})
  for row in data:
    print(row)
"""
with con:
  data = con.execute("SELECT * FROM pins")
  for row in data:
    print(row)