import sqlite3 as sl

con = sl.connect('meepybot.db')

with con:
    try:
        con.execute("CREATE TABLE USER (id VARCHAR(20) NOT NULL PRIMARY KEY, value VARCHAR(50), datetime INTEGER);")
    except:
        print("Error handling database user")
    try:
        con.execute("CREATE TABLE reqs (id INTEGER PRIMARY KEY, channel INTEGER, action VARCHAR(100), datetime INTEGER, guild INTEGER);")
    except:
        print("Error handling database reqs")
    try:
        con.execute("CREATE TABLE pins (channel INTEGER, message_id INTEGER, datetime INTEGER, additional_pins VARCHAR(100)); ")
    except:
        print("Error handling database pins")
    try:
        con.execute("CREATE TABLE slowmoded (user_id INTEGER, channel INTEGER, datetime INTEGER, slowmode_time);")
    except:
        print("Error handling database slowmoded")

    try:
        con.execute("CREATE TABLE strikes (user_id INTEGER, guild_id INTEGER, strikes INTEGER, UNIQUE (user_id, guild_id))")
    except:
        print("Error handling database strikes")
data=[
  ("vote_threshold", 6),
  ("vote_timeout", 300),
  ("slowmodetime", 5),
]

with con:
  con.executemany("INSERT INTO USER (id, value) values (?,?)", data)