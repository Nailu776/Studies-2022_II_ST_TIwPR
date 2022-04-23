from http import HTTPStatus
from tornado.web            import HTTPError
import json
from .errorHandler import BaseHandler, errData
import tornado
import DataBase
import Models.models # Schemas for Swagger
# Players Handler 
# ~/players 
class PlayersH(BaseHandler):
  def get(self):
    """
      Description end-point
      ---
      tags:
        - Players
      summary: 
          Get players from the ranking.
      description: 
          This HTTP method is used to get a list of players 
          sorted by the points they have earned in their games.
      operationId: getPlayers
      responses:
          "200":
              description: 
                The ranking list successfully geted.
          "304":
              description: 
                The ranking list has not been modified since the last get.
          '400':
            description: Bad request
          '404':
            description: Not found
    """
    #EODescription end-point  
    self.set_etag_header()
    if self.check_etag_header():
      self.set_status(304) # 304 HTTP Response CODE
      return
    else:
      DataBase.db.cursor.execute(
        DataBase.queries.get_players_query)
      records = DataBase.db.cursor.fetchall()
      players_table = []
      for dbRecord in records:
          players_table.append(buildPlayerJSON_db(dbRecord))
      response = {}
      response['Response: '] = 'The ranking list successfully geted'
      response['Players: '] = players_table
      self.write(response)
  def post(self):
    """
      Description end-point
      ---
      tags:
        - Players
      summary: 
          Create a new player.
      description: 
          This HTTP method is used to create a new player.
      operationId: addPlayer      
      requestBody: 
        description: Create a new player.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PlayerPostSchema'
        required: true
      responses:
          '200':
              description: New player created.
          '400':
            description: Bad request
          '404':
            description: Not found
          '405':
            description: Invalid input
    """
    #EODescription end-point    
    request_data = tornado.escape.json_decode(self.request.body)
    DataBase.db.cursor.execute('''INSERT INTO PLAYERS 
                      (NICK, RECORD, NO_MSG_RECEIVED, 
                      NO_MSG_SENDED) VALUES (?,0,0,0)''',[request_data['nick']])
    DataBase.db.conn.commit()
    DataBase.db.cursor.execute(
      DataBase.queries.get_player_query, [request_data['nick']])
    dbRecord = DataBase.db.cursor.fetchone()
    response = {}
    response['Response: '] = 'New player created.'
    response['Player: '] = buildPlayerJSON_db(dbRecord)
    self.write(response)
# Players Details Handler
# ~/players/{u_name} 
class PlayersDetailsH(BaseHandler):
  def get(self, nick=None):
    """
      Description end-point
      ---
      tags:
        - Players
      summary: 
          Get single player details by nick.
      description: 
          This HTTP method is used to get the player details 
          by nick of a specific player.
      operationId: getPlayer
      parameters:
        - name: nick
          in: path
          description: Nick of player to get.
          required: true
          schema:
            type: string
      responses:
          "200":
            description: 
              Specific player successfully geted.
          "304":
            description: 
               Specific player has not been modified since the last get.
          "422":
            description: Wrong Nick.
          '400':
            description: Bad request
          '404':
            description: Not found
          '405':
            description: Invalid input
   """
    #EODescription end-point
    if nick:
      dbRecord = getPlayerFromDatabaseByNick(nick)
      if dbRecord:
        response = {}
        response['Response: '] = 'Specific player successfully geted.'
        response['Player: '] = buildPlayerJSON_db(dbRecord)
        self.write(response)
        return
    #else: Nick is missing or wrong err.
    raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
  def delete(self, nick=None):
    """
      Description end-point
      ---
      tags:
        - Players
      summary: 
          Delete single player by nick.
      description: 
          This HTTP method is used to delete a single player by nick.
      operationId: deletePlayer
      parameters:
        - name: nick
          in: path
          description: Nick of player to get.
          required: true
          schema:
            type: string    
      responses:
          "200":
              description: 
                  Specific player successfully deleted.
          "422":
              description: 
                  Wrong nick.
    """
    #EODescription end-point    
    if nick:
      dbRecord = getPlayerFromDatabaseByNick(nick)
      if dbRecord:
        # Delete Player From Database By Nick
        DataBase.db.cursor.execute(DataBase.queries.delete_player_query, [nick])
        DataBase.db.conn.commit()
        checkPlayerDeleted(nick)
        self.write("Player with nick: " + nick + " is successfully delted.")
        return
    #else: Nick is missing or wrong err.
    raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code 
  def patch(self, nick=None):
    """
      Description end-point
      ---
      tags:
        - Players
      summary: 
          Update (PATCH) the specific details of a single player by nick.
      description: 
          This HTTP method is used to update (PATCH) the specific details 
          of a single player by nick of a specific player.
      operationId: patchPlayer
      parameters:
        - name: nick
          in: path
          description: Nick of player to get.
          required: true
          schema:
            type: string     
      requestBody:
        description: Update a specific player.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PlayerUpdateSchema'
      responses:
          "200":
              description: 
                  Specific player successfully updated (patched).
          "422":
            description: Wrong Nick.
          '400':
            description: Bad request
          '404':
            description: Not found
          '405':
            description: Invalid input
    """
    #EODescription end-point   
    if nick:
      DataBase.db.cursor.execute(
        DataBase.queries.get_player_query, [nick])
      record = DataBase.db.cursor.fetchone()
      if record:
        data = {}
        indents = 0
        json_data = json.loads(self.request.body.decode("utf-8"))
        # points_record update
        if 'points_record' in json_data:
          query_data = (int(json_data['points_record']), str(nick))
          DataBase.db.cursor.execute(
            DataBase.queries.patch_player_record_query, query_data)
          data['Player points_record updated:'] = json_data['points_record']
          indents += 1
        # number of msg sendes update
        if 'no_msg_sended' in json_data:
          query_data = (int(json_data['no_msg_sended']), str(nick))
          DataBase.db.cursor.execute(
            DataBase.queries.patch_player_sended_query, query_data)
          data['Player no_msg_sended updated:'] = json_data['no_msg_sended']
          indents += 1
        # number of msg received update
        if 'no_msg_received' in json_data:
          query_data = (int(json_data['no_msg_received']), str(nick))
          DataBase.db.cursor.execute(
            DataBase.queries.patch_player_received_query, query_data)
          data['Player no_msg_received updated:'] = json_data['no_msg_received']
          indents += 1
        if indents == 0:
          data['Changes:'] = 'Nothing'
          indents += 1
        else:
          DataBase.db.conn.commit()
        self.write(json.dumps(data, sort_keys=True, indent=indents))
        return
    #else: Nick is missing or wrong err.
    raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
  def put(self, nick=None):
    """
      Description end-point
      ---
      tags:
        - Players
      summary: 
          Update (PUT) single player details by nick.
      description: 
          This HTTP method is used to update (PUT) the details 
          of a single player by nick of a specific player.
      operationId: putPlayer
      parameters:
        - name: nick
          in: path
          description: Nick of player to get.
          required: true
          schema:
            type: string     
        # - name: ETag
        #   in: header
        #   description: Used to prevent Lost Update Problem
        #   required: true
        #   schema:
        #     type: string 
      requestBody:
        description: Update a specific player.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PlayerUpdateSchema'
      responses:
          "200":
              description: 
                  Specific player successfully updated (puted).
          "422":
            description: Wrong Nick.
          '400':
            description: Bad request
          '404':
            description: Not found
          '405':
            description: Invalid input
    """
    #EODescription end-point    
    if nick:
      dbRecord = getPlayerFromDatabaseByNick(nick)
      if dbRecord:
        json_data = json.loads(self.request.body.decode("utf-8"))
        if len(json_data) == 3: # Check if got 3 arguments = records, no_msg_received and no_msg_sended
          if "points_record" and "no_msg_sended" and "no_msg_received" in json_data:
            query_data = (dbRecord[0], dbRecord[1], int(json_data['points_record']),
              int(json_data['no_msg_sended']), int(json_data['no_msg_received']), str(nick))
            DataBase.db.cursor.execute(
                DataBase.queries.put_player_query, query_data)
            DataBase.db.conn.commit()
            data = {}
            data['Player before update:'] = buildPlayerJSON_db(dbRecord)
            json_data['id'] = dbRecord[0]
            json_data['nick'] = dbRecord[1]
            player_json = buildPlayerJSON(json_data)
            data['Player after update:'] = player_json
            self.write(json.dumps(data, sort_keys=True, indent=2))
            return
    #else: Nick is missing or wrong err.
    raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
def getPlayerFromDatabaseByNick(nick):
  DataBase.db.cursor.execute(DataBase.queries.get_player_query, [nick])
  return DataBase.db.cursor.fetchone()
def buildPlayerJSON_db(dbRecord):
  player_json = {}
  player_json['ID'] = dbRecord[0]
  player_json['NICK'] = dbRecord[1]
  player_json['RECORD'] = dbRecord[2]
  player_json['NO_MSG_RECIEVED'] = dbRecord[3]
  player_json['NO_MSG_SENDED'] = dbRecord[4]
  return player_json
def buildPlayerJSON(json_data):
  player_json = {}
  player_json['ID'] = int(json_data['id'])
  player_json['NICK'] = str(json_data['nick'])
  player_json['RECORD'] = int(json_data['points_record'])
  player_json['NO_MSG_RECIEVED'] = int(json_data['no_msg_sended'])
  player_json['NO_MSG_SENDED'] = int(json_data['no_msg_received'])
  return player_json 
def checkPlayerDeleted(nick):
  # Check if player is gone
  DataBase.db.cursor.execute(DataBase.queries.get_player_query, [nick])
  dbRecord = DataBase.db.cursor.fetchone()
  if dbRecord: # If player exists raise error
    raise HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR)