from http import HTTPStatus
import http.client
from tornado.web            import HTTPError
import json
from .errorHandler import BaseHandler, errData
import DataBase


# Schemas for Swagger
import Schemas.PlayerSchemas 

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
      parameters:
        - name: If-None-Match
          in: header
          required: false
          description: Used to check if we have an up-to-date list.
          schema:
            type: string
            # NOTE default value is usefull for debuging
            # default: '"ETag"' 
        - name: limit
          in: query
          required: false
          description: Limit the number of players to get.
          schema:
            type: integer
            format: int64
        - name: page
          in: query
          required: false
          description: Number of page of players to get.
          schema:
            type: integer
            format: int64
      responses:
          "200":
              description: The ranking list successfully geted.
          "304":
              description:  
                The ranking list has not been modified since the last get.
    """
    #EODescription end-point  

    # Paging
    limit = self.get_query_argument("limit", None)
    page = self.get_query_argument("page", None)
    if page is None or limit is None:
      page = 0
      limit = 10
    else: 
      limit = int(limit) 
      if limit < 1:
        limit = 10
      page = int(page)
      if page < 1:
        page = 0
      else:
        page = (page - 1) * limit
    get_query_data = [limit, page]
    # Get list of players from db
    DataBase.db.cursor.execute(
      DataBase.queries.get_players_query, get_query_data)
    records = DataBase.db.cursor.fetchall()
    players_table = []
    for dbRecord in records:
        players_table.append(buildPlayerJSON_db(dbRecord))
    response = {}
    response['Response'] = 'The ranking list successfully geted.'
    response['Players'] = players_table
    self.write(response)
    # Number of players in table
    DataBase.db.cursor.execute(
      DataBase.queries.counter_players_query)
    no_players = DataBase.db.cursor.fetchone()
    # print(no_players[0])
    # Add link header with number of players
    if((no_players[0] - page - limit) > 0):
      nextpage = " <http://localhost:8000/players/?limit=" + str(limit) + "&page=" + str(int((page/limit)+2)) + ">; rel=next; NumOf Players: " + str(no_players[0])
    else:
      nextpage = "No next page. Num of players: " + str(no_players[0])
    self.add_header('Link', nextpage)
    self.check_modified_resp()
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
        description: New player attributes.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PlayerPostSchema'
          # NOTE text/html to DEBUG CONTENT TYPE CHECKER
          text/html:
            schema:
              $ref: '#/components/schemas/PlayerPostSchema'
        required: true
      responses:
          '201':
            description: New player created.
          '400':
            description: Nick not unique or bad JSON.
    """
    #EODescription end-point

    # Check if content type == app json
    contentType = self.request.headers.get("content-type", "")
    # print(contentType)
    if(contentType != "application/json"):
      errData['Cause'] = 'Expected json.'
      raise HTTPError(HTTPStatus.BAD_REQUEST)
    try:
      # Try to add new player
      request_data = json.loads(self.request.body.decode("utf-8"))\
      # Exception if nick is not unique
      DataBase.db.cursor.execute(
        DataBase.queries.add_player_query,
        [request_data['nick']])
      DataBase.db.conn.commit()
      # Check if player is added
      DataBase.db.cursor.execute(
        DataBase.queries.get_player_query, 
        [request_data['nick']])
      dbRecord = DataBase.db.cursor.fetchone()
    except:
      errData['Cause'] = 'Nick not unique or bad JSON.'
      raise HTTPError(HTTPStatus.BAD_REQUEST)
    else:
      response = {}
      response['Response'] = 'New player created.'
      response['Player'] = buildPlayerJSON_db(dbRecord)
      self.set_status(HTTPStatus.CREATED)
      self.write(response)

#  Players Details Handler
# ~/players/{nick} 
class PlayersDetailsH(BaseHandler):
  def get(self, nick):
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
        - name: If-None-Match
          in: header
          required: false
          description: Used to check if we have an up-to-date player.
          schema:
            type: string
            # NOTE default value is usefull for debuging
            # default: '"ETag"'
      responses:
          "200":
            description: 
              Specific player successfully geted.
          "304":
            description: 
               Specific player has not been modified since the last get.
          "400":
            description: Missing or wrong nick.
   """
    #EODescription end-point
          
    if nick:
      dbRecord = getPlayerFromDatabaseByNick(nick) 
      if dbRecord:
        response = {}
        response['Response'] = 'Specific player successfully geted.'
        response['Player'] = buildPlayerJSON_db(dbRecord)
        self.write(response)
        # 304 if not modified
        self.check_modified_resp()
      else: 
        # Nick is wrong err.   
        errData['Cause'] = 'Nick is wrong.'
        # 400 Error Code 
        raise HTTPError(HTTPStatus.BAD_REQUEST) 
    else: 
      # Nick is missing err.
      errData['Cause'] = 'Nick is missing.'
      # 400 Error Code
      raise HTTPError(HTTPStatus.BAD_REQUEST) 
  def delete(self, nick):
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
          description: Nick of player to delete.
          required: true
          schema:
            type: string 
        - name: If-Match
          in: header
          required: false
          description: Used to prevent lost-update-problem.
          schema:
            type: string
            # NOTE default value is usefull for debuging
            # default: '"ETag"'   
      responses:
          "200":
            description: 
              Specific player successfully deleted.
          "400":
            description: Missing nick.
          "404":
            description: Player not found. Nick is wrong.
          "412":
            description: Precondition Failed. Entity changed.
          "428":
            description: Precondition Required. Etag is missing.
          "500":
            description: 
              Server did not delete player successfully.  
              Player still exists.
    """
    #EODescription end-point 
       
    if nick:
      dbRecord = getPlayerFromDatabaseByNick(nick)
      if dbRecord:
        # Check precondition.
        response = {}
        response['Response'] = 'Specific player successfully geted.'
        response['Player'] = buildPlayerJSON_db(dbRecord)
        self.write(response)
        if not self.check_if_match():  
          # Error
          self._headers['Content-Type'] = "text/html; charset=utf-8"
          self.write("HTTP error code: {} {}\n".format(str(self._status_code),
                  http.client.responses[self._status_code]))  
          self.write("Cause: " + errData['Cause'])
          return
        else:
          # Precondition passed.
          # Delete Player From Database By Nick
          DataBase.db.cursor.execute(DataBase.queries.delete_player_query, [nick])
          DataBase.db.conn.commit()
          # NOTE this is used to debug debug 500
          # DataBase.db.cursor.execute(DataBase.queries.add_player_query, [nick]) 
          checkPlayerDeleted(nick)
          self._headers['Content-Type'] = "text/html; charset=utf-8"
          self.write("Player with nick: " + nick + " is successfully delted.")
          return 
      else: 
        # Nick is wrong err.  
        errData['Cause'] = 'Player not found. Nick is wrong.'
         # 404 Error Code
        raise HTTPError(HTTPStatus.NOT_FOUND)
    else:
      # Nick is missing err.
      errData['Cause'] = 'Nick is missing.'
      # 400 Error Code
      raise HTTPError(HTTPStatus.BAD_REQUEST) 
  def patch(self, nick):
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
          description: Nick of player to update.
          required: true
          schema:
            type: string  
        - name: If-Match
          in: header
          required: false
          description: Used to prevent lost-update-problem.
          schema:
            type: string
            # NOTE default value is usefull for debuging
            # default: '"ETag"' 
      requestBody:
        description: Update a specific player.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PlayerUpdateSchema'
          # NOTE text/html to DEBUG CONTENT TYPE CHECKER
          text/html:
            schema:
              $ref: '#/components/schemas/PlayerUpdateSchema'
      responses:
          "200":
              description: 
                  Specific player successfully updated (patched).
          "400":
            description: 
              Nick is missing or something in request body is not in correct format. Or expected json in req body.
          "404":
            description: Nick is wrong.
          "412":
            description: Precondition Failed. Entity changed.
          "428":
            description: Precondition Required. Etag is missing.
    """
    #EODescription end-point 
  
    # Check if content type == app json
    contentType = self.request.headers.get("content-type", "")
    # print(contentType)
    if(contentType != "application/json"):
      errData['Cause'] = 'Expected json.'
      raise HTTPError(HTTPStatus.BAD_REQUEST)
    if nick:
      dbRecord = getPlayerFromDatabaseByNick(nick)
      if dbRecord:
        # Check precondition.
        response = {}
        response['Response'] = 'Specific player successfully geted.'
        response['Player'] = buildPlayerJSON_db(dbRecord)
        self.write(response)
        if not self.check_if_match():  
          # Error
          self._headers['Content-Type'] = "text/html; charset=utf-8"
          self.write("HTTP error code: {} {}\n".format(str(self._status_code),
                  http.client.responses[self._status_code]))  
          self.write("Cause: " + errData['Cause'])
          return
        else:
          # Precondition passed.
          data = {}
          indents = 0
          try: 
            json_data = json.loads(self.request.body.decode("utf-8"))
            # points_record update
            if 'points_record' in json_data:
              query_data = (int(json_data['points_record']), str(nick))
              DataBase.db.cursor.execute(
                DataBase.queries.patch_player_record_query, query_data)
              data['Player points_record updated'] = json_data['points_record']
              indents += 1
            # number of msg sendes update
            if 'no_msg_sended' in json_data:
              query_data = (int(json_data['no_msg_sended']), str(nick))
              DataBase.db.cursor.execute(
                DataBase.queries.patch_player_sended_query, query_data)
              data['Player no_msg_sended updated'] = json_data['no_msg_sended']
              indents += 1
            # number of msg received update
            if 'no_msg_received' in json_data:
              query_data = (int(json_data['no_msg_received']), str(nick))
              DataBase.db.cursor.execute(
                DataBase.queries.patch_player_received_query, query_data)
              data['Player no_msg_received updated'] = json_data['no_msg_received']
              indents += 1
          except:
            errData['Cause'] = 'Check if request body is correct.'
            raise HTTPError(HTTPStatus.BAD_REQUEST)
          else:
            if indents == 0:
              data['Changes'] = 'Nothing'
              indents += 1
            else:
              DataBase.db.conn.commit()
              # Calculate new etag 
              dbRecord = getPlayerFromDatabaseByNick(nick)
              response = {}
              response['Response'] = 'Specific player successfully geted.'
              response['Player'] = buildPlayerJSON_db(dbRecord)
              self.write(response)
              self.set_my_etag_header()
              # Vanish response
              self._write_buffer = []
            self.write(json.dumps(data, sort_keys=True, indent=indents))
            return  
      else: 
        # Nick is wrong err. 
        errData['Cause'] = 'Player not found. Nick is wrong.'
         # 404 Error Code
        raise HTTPError(HTTPStatus.NOT_FOUND)
    else:
      # Nick is missing err.
      errData['Cause'] = 'Nick is missing.'
      # 400 Error Code
      raise HTTPError(HTTPStatus.BAD_REQUEST) 
  def put(self, nick):
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
        - name: If-Match
          in: header
          required: false
          description: Used to prevent lost-update-problem.
          schema:
            type: string
            # NOTE default value is usefull for debuging
            # default: '"ETag"' 
      requestBody:
        description: Update a specific player.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PlayerUpdateSchema'
          # NOTE text/html to DEBUG CONTENT TYPE CHECKER
          text/html:
            schema:
              $ref: '#/components/schemas/PlayerUpdateSchema'
      responses:
          "200":
              description: 
                  Specific player successfully updated (puted).
          "400":
            description: 
              Nick is missing or something in request body is not in correct format. Or expected json in req body.
          "404":
            description: Nick is wrong.
          "412":
            description: Precondition Failed. Entity changed.
          "428":
            description: Precondition Required. Etag is missing.
    """
    #EODescription end-point  
    
    # Check if content type == app json
    contentType = self.request.headers.get("content-type", "")
    # print(contentType)
    if(contentType != "application/json"):
      errData['Cause'] = 'Expected json.'
      raise HTTPError(HTTPStatus.BAD_REQUEST)
    if nick:
      dbRecord = getPlayerFromDatabaseByNick(nick)
      if dbRecord:
        # Check precondition.
        response = {}
        response['Response'] = 'Specific player successfully geted.'
        response['Player'] = buildPlayerJSON_db(dbRecord)
        self.write(response)
        if not self.check_if_match():  
          # Error
          self._headers['Content-Type'] = "text/html; charset=utf-8"
          self.write("HTTP error code: {} {}\n".format(str(self._status_code),
                  http.client.responses[self._status_code]))  
          self.write("Cause: " + errData['Cause'])
          return
        else:
          # Precondition passed.
          data = {}
          data['Player before update'] = response['Player']
          try:
            request_data = json.loads(self.request.body.decode("utf-8"))
          except:
            errData['Cause'] = 'Check if request body is correct.'
            raise HTTPError(HTTPStatus.BAD_REQUEST)
          else:
            if len(request_data) != 3:
                errData['Cause'] = 'Request body require 3 elements.'
                raise HTTPError(HTTPStatus.BAD_REQUEST)
            else:
                # NOTE Check if got 3 arguments:
                # points_record, no_msg_sended and no_msg_received
                try:
                  query_data = (dbRecord[0], int(request_data['points_record']),
                    int(request_data['no_msg_sended']), int(request_data['no_msg_received']), str(nick))
                except:
                    errData['Cause'] = 'Check if request body is correct.'
                    raise HTTPError(HTTPStatus.BAD_REQUEST)
                else:
                  DataBase.db.cursor.execute(
                      DataBase.queries.put_player_query, query_data)
                  DataBase.db.conn.commit()
                  # Calculate new etag 
                  DataBase.db.cursor.execute(
                    DataBase.queries.get_player_query, [nick])
                  dbRecord = DataBase.db.cursor.fetchone()
                  response['Response'] = 'Specific player successfully geted.'
                  response['Player'] = buildPlayerJSON_db(dbRecord)
                  self.write(response)
                  self.set_my_etag_header()
                  # Vanish response
                  self._write_buffer = []
                  request_data['nick'] = dbRecord[0]
                  player_json = buildPlayerJSON(request_data)
                  data['Player after update'] = player_json
                  self.write(json.dumps(data, sort_keys=True, indent=2))
                  return  
      else:  
        # Nick is wrong err.
        errData['Cause'] = 'Player not found. Nick is wrong.'
        # 404 Error Code
        raise HTTPError(HTTPStatus.NOT_FOUND) 
    else:
      # Nick is missing err.
      errData['Cause'] = 'Nick is missing.'
       # 400 Error Code
      raise HTTPError(HTTPStatus.BAD_REQUEST)

# Usefull functions
def getPlayerFromDatabaseByNick(nick):
  DataBase.db.cursor.execute(DataBase.queries.get_player_query, [nick])
  return DataBase.db.cursor.fetchone()
def buildPlayerJSON_db(dbRecord):
  player_json = {}
  player_json['NICK'] = dbRecord[0]
  player_json['RECORD'] = dbRecord[1]
  player_json['NO_MSG_RECIEVED'] = dbRecord[2]
  player_json['NO_MSG_SENDED'] = dbRecord[3]
  return player_json
def buildPlayerJSON(json_data):
  player_json = {}
  player_json['NICK'] = str(json_data['nick'])
  player_json['RECORD'] = int(json_data['points_record'])
  player_json['NO_MSG_RECIEVED'] = int(json_data['no_msg_sended'])
  player_json['NO_MSG_SENDED'] = int(json_data['no_msg_received'])
  return player_json 
def checkPlayerDeleted(nick):
  if getPlayerFromDatabaseByNick(nick): 
    # If player exists raise error
    errData['Cause'] = 'Server did not delete player successfully. Player still exists.'
    raise HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR)