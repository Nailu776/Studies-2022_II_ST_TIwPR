import sqlite3
from . import queries
# Connect to sqlite database
conn = sqlite3.connect('DataBase/sqliteDB.db')
# cursor object
cursor = conn.cursor()
def init_players():
    # drop query
    #cursor.execute("DROP TABLE IF EXISTS PLAYERS")
    cursor.execute(queries.queryPlayersTable)
    conn.commit()
def init_messages():
    # drop query
    # cursor.execute("DROP TABLE IF EXISTS MESSAGES")
    cursor.execute(queries.queryMessagesTable)
    conn.commit()
def init_histories():
    # drop query
    # cursor.execute("DROP TABLE IF EXISTS HISTORIES")
    cursor.execute(queries.queryHistoriesTable)
    conn.commit()
def init_merges():
    # drop query
    # cursor.execute("DROP TABLE IF EXISTS PLAYER_MERGES")
    cursor.execute(queries.queryPlayerMergesTable)
    conn.commit()
def init():
    init_players()
    init_messages()
    init_histories()
    init_merges()