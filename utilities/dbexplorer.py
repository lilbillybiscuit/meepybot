import sqlite3 as sl

con = sl.connect('../meepybot.db')

with con:
  data = con.execute("""
  SELECT * FROM USER where id = :key
  """, {"key": "vote_timeout"})
  for row in data:
    print(row)
'''
with con:
  val=8
  sql = "UPDATE USER SET value = ? WHERE id = ?"
  data=(str(val), 'vote_timeout')
  con.execute(sql, data)
  con.commit()'''