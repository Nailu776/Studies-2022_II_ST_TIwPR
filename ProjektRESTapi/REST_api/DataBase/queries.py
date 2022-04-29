
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