# PLAYERS 
queryPlayersTable = """CREATE TABLE IF NOT EXISTS PLAYERS (
                NICK TEXT PRIMARY KEY DEFAULT DELETED,
                RECORD INT,
                NO_MSG_RECEIVED INT,
                NO_MSG_SENDED INT
                )"""
add_player_query = '''INSERT INTO PLAYERS 
                      (NICK, RECORD, NO_MSG_RECEIVED, 
                      NO_MSG_SENDED) VALUES (?,0,0,0)'''
get_players_query = '''SELECT * FROM PLAYERS ORDER BY RECORD DESC LIMIT ? OFFSET ?'''
get_player_query = '''SELECT * FROM PLAYERS WHERE NICK = ? '''
patch_player_record_query = '''UPDATE PLAYERS SET RECORD = ? WHERE NICK = ?'''
patch_player_received_query = '''UPDATE PLAYERS SET NO_MSG_RECEIVED = ? WHERE NICK = ?'''
patch_player_sended_query = '''UPDATE PLAYERS SET NO_MSG_SENDED = ? WHERE NICK = ?'''
put_player_query = '''UPDATE PLAYERS SET NICK = ?, RECORD =?, 
                    NO_MSG_RECEIVED = ?, NO_MSG_SENDED =? WHERE NICK = ?'''
delete_player_query = '''DELETE FROM PLAYERS WHERE NICK=?'''
counter_players_query = '''SELECT COUNT (*) FROM PLAYERS'''     
# MESSAGES                      
queryMessagesTable = """CREATE TABLE IF NOT EXISTS MESSAGES (
                        ID INTEGER PRIMARY KEY,
                        SENDER_NICK TEXT DEFAULT DELETED_PLAYER
                            REFERENCES PLAYERS(NICK) 
                                ON UPDATE CASCADE
                                ON DELETE SET DEFAULT,
                        RECEIVER_NICK TEXT DEFAULT DELETED_PLAYER
                            REFERENCES PLAYERS(NICK) 
                                ON UPDATE CASCADE    
                                ON DELETE SET DEFAULT,
                        TEXT_MESSAGE TEXT
                        )"""
update_sended_mess = '''UPDATE MESSAGES SET SENDER_NICK = ? WHERE SENDER_NICK = ?'''
update_received_mess = '''UPDATE MESSAGES SET RECEIVER_NICK = ? WHERE RECEIVER_NICK = ?'''
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
get_message_byID_SN_RN_query = '''SELECT * FROM MESSAGES WHERE 
                            ID = ? AND SENDER_NICK = ? AND RECEIVER_NICK = ?'''
delete_message_query = '''DELETE FROM MESSAGES WHERE ID=?'''
patch_msg_sender_nick_query = '''UPDATE MESSAGES SET SENDER_NICK = ? WHERE ID = ?'''
patch_msg_receiver_nick_query = '''UPDATE MESSAGES SET RECEIVER_NICK = ? WHERE ID = ?'''
patch_msg_text_message_query = '''UPDATE MESSAGES SET TEXT_MESSAGE = ? WHERE ID = ?'''
put_msg_query = '''UPDATE MESSAGES SET SENDER_NICK = ?, RECEIVER_NICK = ?, TEXT_MESSAGE = ? 
WHERE ID = ? '''

# Histories          
queryHistoriesTable = """CREATE TABLE IF NOT EXISTS HISTORIES (
ID INTEGER PRIMARY KEY,
DATE DATE,
G_NAME TEXT UNIQUE,
PLAYERS_TAB TEXT)"""
get_history_with_name = '''SELECT * FROM HISTORIES WHERE G_NAME = ?'''
get_history_with_id = '''SELECT * FROM HISTORIES WHERE ID = ?'''
get_all_histories = '''SELECT * FROM HISTORIES LIMIT ? OFFSET ?'''
add_history_query = '''INSERT INTO HISTORIES 
                      (DATE, G_NAME, PLAYERS_TAB) 
                      VALUES (?,?,?)'''
poe_post_dummy_history_query = '''INSERT INTO HISTORIES 
                      (DATE, G_NAME, PLAYERS_TAB) 
                      VALUES (NULL,NULL,"DummyHistory")'''
poe_put_history_query= '''UPDATE HISTORIES SET  
                      DATE = ?, G_NAME = ?, PLAYERS_TAB = ? 
                      WHERE ID = ?'''
counter_hists_query = '''SELECT COUNT (*) FROM HISTORIES'''  

# Player Merges
queryPlayerMergesTable = """CREATE TABLE IF NOT EXISTS PLAYER_MERGES (
ID INTEGER PRIMARY KEY,
DATE DATE NOT NULL,
NICK_FIRST TEXT NOT NULL,
NICK_SECOUND TEXT NOT NULL,
NICK_FINAL TEXT NOT NULL 
    DEFAULT DELETED_PLAYER
        REFERENCES PLAYERS(NICK) 
            ON UPDATE CASCADE    
            ON DELETE SET DEFAULT)"""
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