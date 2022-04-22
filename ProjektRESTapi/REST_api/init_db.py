import sqlite3

# Connect to sqlite database
conn = sqlite3.connect('sqliteDB.db')
# cursor object
cursor = conn.cursor()
def init():
    # drop query
    cursor.execute("DROP TABLE IF EXISTS PLAYERS")
    # create query
    queryPlayers = """CREATE TABLE IF NOT EXISTS PLAYERS (
                    ID INT PRIMARY KEY NOT NULL,
                    NICK CHAR(20) NOT NULL,
                    RECORD INT,
                    NO_MSG_RECEIVED INT,
                    NO_MSG_SENDED INT )"""
    cursor.execute(queryPlayers)
    conn.commit()
