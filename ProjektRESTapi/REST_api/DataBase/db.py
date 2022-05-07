import sqlite3
from . import queries
reset = False
# Connect to sqlite database
conn = sqlite3.connect('DataBase/sqliteDB.db')
# cursor object
cursor = conn.cursor()
def init_players():
    cursor.execute("DROP TABLE IF EXISTS PLAYERS")
    cursor.execute(queries.queryPlayersTable)
    cursor.execute(queries.add_player_query,
        ["DELETED_PLAYER"])
def init_messages():
    cursor.execute("DROP TABLE IF EXISTS MESSAGES")
    cursor.execute(queries.queryMessagesTable)
def init_histories():
    cursor.execute("DROP TABLE IF EXISTS HISTORIES")
    cursor.execute(queries.queryHistoriesTable)
def init_merges():
    cursor.execute("DROP TABLE IF EXISTS PLAYER_MERGES")
    cursor.execute(queries.queryPlayerMergesTable)
def init():
    if reset:
        init_players()
        init_messages()
        init_histories()
        init_merges()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("PRAGMA foreign_keys")
    conn.commit()