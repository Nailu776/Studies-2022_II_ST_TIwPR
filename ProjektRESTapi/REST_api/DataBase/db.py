import sqlite3
from . import queries
# Connect to sqlite database
conn = sqlite3.connect('DataBase/sqliteDB.db')
# cursor object
cursor = conn.cursor()
reset = True
def init_players():
    # drop query
    cursor.execute("DROP TABLE IF EXISTS PLAYERS")
    cursor.execute(queries.queryPlayersTable)
    cursor.execute(queries.add_player_query,
        ["DELETED_PLAYER"])
    cursor.execute(queries.add_player_query,
        ["NICK3"])
    cursor.execute(queries.add_player_query,
        ["NICK5"])
    cursor.execute(queries.add_player_query,
        ["NICK6"])
    cursor.execute(queries.add_player_query,
        ["NICK0"])
    for i in range (1, 100):
        cursor.execute(queries.add_player_query,
            ["Gracz"+str(i)])
    conn.commit()
def init_messages():
    # drop query
    cursor.execute("DROP TABLE IF EXISTS MESSAGES")
    cursor.execute(queries.queryMessagesTable)

    
    for i in range (1, 100):
        cursor.execute(
            queries.add_message_query,
            ["NICK0",
            "NICK6",
            "test"])
    conn.commit()
def init_histories():
    # drop query
    cursor.execute("DROP TABLE IF EXISTS HISTORIES")
    cursor.execute(queries.queryHistoriesTable)
    conn.commit()
def init_merges():
    # drop query
    cursor.execute("DROP TABLE IF EXISTS PLAYER_MERGES")
    cursor.execute(queries.queryPlayerMergesTable)
    conn.commit()
def init():
    if reset:
        init_players()
        init_messages()
        init_histories()
        init_merges()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("PRAGMA foreign_keys")
    conn.commit()