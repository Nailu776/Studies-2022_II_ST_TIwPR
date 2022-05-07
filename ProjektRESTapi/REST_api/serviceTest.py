from DataBase import db, queries
import json
from datetime import datetime
import time
if __name__ == "__main__":
    # Create 100 players
    for i in range (1, 100):
        db.cursor.execute(queries.add_player_query,
            ["NickName"+str(i)])
    # Commit to see it in db.
    db.conn.commit()
    # Create 200 messages
    for i in range (1, 100):
        db.cursor.execute(
            queries.add_message_query,
            [ "NickName" + str(101 - i),
            "NickName" + str(i),
            "Message from " + str(101 - i) + " to " + str(i)])
        # Update numbers recived / sended msgs
        db.cursor.execute(
            queries.inc_message_sended_query,
            ["NickName" + str(101 - i)])
        db.cursor.execute(
            queries.inc_message_received_query,
            ["NickName" + str(i)])
        db.cursor.execute(
            queries.add_message_query,
            [ "NickName" + str(i),
             "NickName" + str(101 - i),
            "Message from " + str(i) + " to " + str(101 - i)])
        # Update numbers recived / sended msgs
        db.cursor.execute(
            queries.inc_message_sended_query,
            ["NickName" + str(i)])
        db.cursor.execute(
            queries.inc_message_received_query,
            ["NickName" + str(101 - i)])
    # Commit to see it in db.
    db.conn.commit()
    # Create 50 game histories
    for i in range (1, 50):
        # datetime object containing current date and time
        now = datetime.now()
        string_json = {
            "players_tab":[
          {
            "nick": "NickName1",
            "points": 10
          },
          {
            "nick": "NickName2",
            "points": 20
          },
          {
            "nick": "NickName3",
            "points": 30
          },
          {
            "nick": "NickName8",
            "points": 25
          },
          {
            "nick": "NickName9",
            "points": 40
          },
          {
            "nick": "NickName11",
            "points": 29
          },
          {
            "nick": "NickName15",
            "points": 23
          },
          {
            "nick": "NickName12",
            "points": 11
          }]
        }
        stringTab = json.dumps(string_json)
        db.cursor.execute(
            queries.poe_post_dummy_history_query)
        dbRecord_id = db.cursor.lastrowid
        db.cursor.execute(
            queries.poe_put_history_query,
            [now.strftime("%d/%m/%Y %H:%M:%S"),
            "RandomGame:" + str(i),
            stringTab, dbRecord_id])
        # print("I sleep for 1.1 sec. GHist no: " + str(i))
        time.sleep(1.1)
    # Commit.
    db.conn.commit()
    