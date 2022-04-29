# PLAYERS
queryPlayersTable = """CREATE TABLE IF NOT EXISTS PLAYERS (
                ID INTEGER PRIMARY KEY,
                NICK CHAR(20) NOT NULL UNIQUE,
                RECORD INT,
                NO_MSG_RECEIVED INT,
                NO_MSG_SENDED INT )"""
get_players_query = '''SELECT * FROM PLAYERS'''
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
TEXT_MESSAGE CHAR(500) )"""
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