# PLAYERS
queryPlayersTable = """CREATE TABLE IF NOT EXISTS PLAYERS (
                ID INTEGER PRIMARY KEY,
                NICK CHAR(20) NOT NULL UNIQUE,
                RECORD INT,
                NO_MSG_RECEIVED INT,
                NO_MSG_SENDED INT )"""
get_players_query = '''SELECT * FROM PLAYERS ORDER BY RECORD DESC'''
get_player_query = '''SELECT * FROM PLAYERS WHERE NICK = ? '''
patch_player_record_query = '''UPDATE PLAYERS SET RECORD = ? WHERE NICK = ?'''
patch_player_received_query = '''UPDATE PLAYERS SET NO_MSG_RECEIVED = ? WHERE NICK = ?'''
patch_player_sended_query = '''UPDATE PLAYERS SET NO_MSG_SENDED = ? WHERE NICK = ?'''
put_player_query = '''UPDATE PLAYERS SET ID = ?, NICK = ?, RECORD =?, 
NO_MSG_RECEIVED = ?, NO_MSG_SENDED =? WHERE NICK = ?'''
delete_player_query = '''DELETE FROM PLAYERS WHERE NICK=?'''
add_player_query = '''INSERT INTO PLAYERS 
                      (NICK, RECORD, NO_MSG_RECEIVED, 
                      NO_MSG_SENDED) VALUES (?,0,0,0)'''
                      
# MESSAGES                      
queryMessagesTable = """CREATE TABLE IF NOT EXISTS MESSAGES (
ID INTEGER PRIMARY KEY,
SENDER_NICK CHAR(20) NOT NULL,
RECEIVER_NICK CHAR(20) NOT NULL,
TEXT_MESSAGE TEXT )"""
add_message_query = '''INSERT INTO MESSAGES 
                      (SENDER_NICK, RECEIVER_NICK, TEXT_MESSAGE) 
                      VALUES (?,?,?)'''
get_message_query = '''SELECT * FROM MESSAGES WHERE SENDER_NICK = ? AND
                     RECEIVER_NICK = ? AND TEXT_MESSAGE = ?'''
inc_message_sended_query = '''UPDATE PLAYERS SET 
NO_MSG_SENDED = NO_MSG_SENDED + 1 WHERE NICK = ?'''
inc_message_received_query = '''UPDATE PLAYERS SET 
NO_MSG_RECEIVED = NO_MSG_RECEIVED + 1 WHERE NICK = ?'''
get_messages_query = '''SELECT * FROM MESSAGES WHERE SENDER_NICK = ? AND
                     RECEIVER_NICK = ? '''
get_message_byID_query = '''SELECT * FROM MESSAGES WHERE ID = ?'''
delete_message_query = '''DELETE FROM MESSAGES WHERE ID=?'''
patch_msg_sender_nick_query = '''UPDATE MESSAGES SET SENDER_NICK = ? WHERE ID = ?'''
patch_msg_receiver_nick_query = '''UPDATE MESSAGES SET RECEIVER_NICK = ? WHERE ID = ?'''
patch_msg_text_message_query = '''UPDATE MESSAGES SET TEXT_MESSAGE = ? WHERE ID = ?'''
put_msg_query = '''UPDATE MESSAGES SET SENDER_NICK = ?, RECEIVER_NICK = ?, TEXT_MESSAGE = ? 
WHERE ID = ? '''

# Histories          
queryHistoriesTable = """CREATE TABLE IF NOT EXISTS HISTORIES (
ID INTEGER PRIMARY KEY,
DATE DATE NOT NULL,
G_NAME CHAR(20) NOT NULL UNIQUE,
PLAYERS_TAB TEXT NOT NULL)"""
get_history_with_name = '''SELECT * FROM HISTORIES WHERE G_NAME = ?'''
get_all_histories = '''SELECT * FROM HISTORIES'''
add_history_query = '''INSERT INTO HISTORIES 
                      (DATE, G_NAME, PLAYERS_TAB) 
                      VALUES (?,?,?)'''

# Player Merges
queryPlayerMergesTable = """CREATE TABLE IF NOT EXISTS PLAYER_MERGES (
ID INTEGER PRIMARY KEY,
DATE DATE NOT NULL,
NICK_FIRST CHAR(20) NOT NULL,
NICK_SECOUND CHAR(20) NOT NULL,
NICK_FINAL CHAR(20) NOT NULL)"""
get_all_merges = '''SELECT * FROM PLAYER_MERGES'''
get_merge_by_id = '''SELECT * FROM PLAYER_MERGES WHERE ID = ?'''
create_merge_req = '''
        INSERT INTO PLAYER_MERGES 
            (DATE, NICK_FIRST, NICK_SECOUND, NICK_FINAL) 
                VALUES (?,?,?,?)'''
execute_merge = '''
        UPDATE PLAYERS SET NICK = ?, 
        RECORD = MAX((SELECT RECORD FROM PLAYERS WHERE NICK = ?), 
                        (SELECT RECORD FROM PLAYERS WHERE NICK = ?)),
        NO_MSG_RECEIVED = (SELECT NO_MSG_RECEIVED FROM PLAYERS WHERE NICK = ?) + 
                        (SELECT NO_MSG_RECEIVED FROM PLAYERS WHERE NICK = ?),
        NO_MSG_SENDED = (SELECT NO_MSG_SENDED FROM PLAYERS WHERE NICK = ?) + 
                        (SELECT NO_MSG_SENDED FROM PLAYERS WHERE NICK = ?)
        WHERE NICK = ?'''