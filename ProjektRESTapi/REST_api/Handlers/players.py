from http import HTTPStatus
import http.client
from tornado.web            import HTTPError
from tornado.escape         import utf8
import json
from .errorHandler import BaseHandler, errData
import tornado
import DataBase
import Models.models # Schemas for Swagger
import hashlib
from asyncio.windows_events import NULL
from typing import   Optional
# Players Handler 
# ~/players 
class PlayersH(BaseHandler):
  # Check if modified
  def check_modified_resp(self):
    # Check etag: if equals then response is not modified
    self.set_my_etag_header()
    if self.check_etag_header():
      # Vanish response
      self._write_buffer = []
      self.set_status(HTTPStatus.NOT_MODIFIED)
      return
    else:
      # Etag changed so return with response body
      return
  # Override etag functions
  def compute_etag(self):
    return NULL
  def compute_my_etag(self) -> Optional[str]:
      """Computes the etag header to be used for this request.

      By default uses a hash of the content written so far.

      May be overridden to provide custom etag implementations,
      or may return None to disable tornado's default etag support.
      """
      hasher = hashlib.sha1()
      for part in self._write_buffer:
          hasher.update(part)
      return '"%s"' % hasher.hexdigest()
  def set_my_etag_header(self) -> None:
      """Sets the response's Etag header using ``self.compute_etag()``.

      Note: no header will be set if ``compute_etag()`` returns ``None``.

      This method is called automatically when the request is finished.
      """
      etag = self.compute_my_etag()
      if etag is not None:
          self.set_header("Etag", etag)
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
            #TODO comment that default after debugging
            # default: '"ETag"' 
      responses:
          "200":
              description: The ranking list successfully geted.
          "304":
              description:  
                The ranking list has not been modified since the last get.
    """
    #EODescription end-point  
    # Get list of players from db
    DataBase.db.cursor.execute(
      DataBase.queries.get_players_query)
    records = DataBase.db.cursor.fetchall()
    players_table = []
    for dbRecord in records:
        players_table.append(buildPlayerJSON_db(dbRecord))
    response = {}
    response['Response'] = 'The ranking list successfully geted'
    response['Players'] = players_table
    self.write(response)
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
        required: true
      responses:
          '200':
            description: New player created.
          '422':
            description: A player with this nick perhaps already exists.
    """
    #EODescription end-point
    try:
      # Try to add new player
      request_data = tornado.escape.json_decode(self.request.body)
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
      errData['Cause'] = 'A player with this nick perhaps already exists.'
      raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY)
    else:
      response = {}
      response['Response'] = 'New player created.'
      response['Player'] = buildPlayerJSON_db(dbRecord)
      self.write(response)
# Players Details Handler
# ~/players/{u_name} 
class PlayersDetailsH(BaseHandler):
  # Check if etag match
  def check_if_match(self) -> bool:
    self.set_my_etag_header()
    # Vanish get player response
    self._write_buffer=[]
    # Check if etag in request exists
    req_etag = self.request.headers.get("If-Match", "")
    # TODO check if it's legal to do If-None-Match = If-Match
    self.request.headers['If-None-Match'] = req_etag
    if req_etag:
      # Check etag: if equals then entity is not modified
      if not self.check_etag_header():
        # Etag changed so entitiy is modified
        errData['Cause'] = 'Entity changed.'
        self.set_status(HTTPStatus.PRECONDITION_FAILED)
        return False
      else:
        # Go on you got up-to-date entity
        return True
    else:
      errData['Cause'] = 'ETag is missing.'
      self.set_status(HTTPStatus.PRECONDITION_REQUIRED)
      return False
  # Check if modified
  def check_modified_resp(self):
    # Check etag: if equals then response is not modified
    self.set_my_etag_header()
    if self.check_etag_header():
      # Vanish response
      self._write_buffer = []
      self.set_status(HTTPStatus.NOT_MODIFIED)
      return
    else:
      # Etag changed so return with response body
      return
  # Override etag functions
  def compute_etag(self):
    return NULL
  def compute_my_etag(self) -> Optional[str]:
      """Computes the etag header to be used for this request.

      By default uses a hash of the content written so far.

      May be overridden to provide custom etag implementations,
      or may return None to disable tornado's default etag support.
      """
      hasher = hashlib.sha1()
      for part in self._write_buffer:
          hasher.update(part)
      return '"%s"' % hasher.hexdigest()
  def set_my_etag_header(self) -> None:
      """Sets the response's Etag header using ``self.compute_etag()``.

      Note: no header will be set if ``compute_etag()`` returns ``None``.

      This method is called automatically when the request is finished.
      """
      etag = self.compute_my_etag()
      if etag is not None:
          self.set_header("Etag", etag)
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
            #TODO comment that default after debugging
            # default: '"ETag"'
      responses:
          "200":
            description: 
              Specific player successfully geted.
          "304":
            description: 
               Specific player has not been modified since the last get.
          "422":
            description: Missing or wrong nick.
   """
    #EODescription end-point
    #      
    if nick:
      dbRecord = getPlayerFromDatabaseByNick(nick) 
      if dbRecord:
        response = {}
        response['Response'] = 'Specific player successfully geted.'
        response['Player'] = buildPlayerJSON_db(dbRecord)
        self.write(response)
        self.check_modified_resp()
      else: # Nick is wrong err.   
        errData['Cause'] = 'Nick is wrong.'
        raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
    else: # Nick is missing err.
      errData['Cause'] = 'Nick is missing.'
      raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
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
            #TODO comment that default after debugging
            default: '"ETag"'   
      responses:
          "200":
            description: 
              Specific player successfully deleted.
          "422":
            description: Missing nick.
          "404":
            description: Player not found.
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
          #TODO comment this after debug 500
          # DataBase.db.cursor.execute(DataBase.queries.add_player_query, [nick]) 
          checkPlayerDeleted(nick)
          self._headers['Content-Type'] = "text/html; charset=utf-8"
          self.write("Player with nick: " + nick + " is successfully delted.")
          return
      # Nick is wrong err.  
      else:  
        errData['Cause'] = 'Player not found.'
        raise HTTPError(HTTPStatus.NOT_FOUND) # 422 Error Code
    # Nick is missing err.
    else:
      errData['Cause'] = 'Nick is missing.'
      raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
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
            #TODO comment that default after debugging
            # default: '"ETag"' 
      requestBody:
        description: Update a specific player.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PlayerPatchSchema'
      responses:
          "200":
              description: 
                  Specific player successfully updated (patched).
          "422":
            description: Nick is missing.
          "404":
            description: Nick is wrong.
          "428":
            description: Precondition Required. Etag is missing.
          "412":
            description: Precondition Failed. Entity is modified.
    """
    #EODescription end-point 
    if nick:
      DataBase.db.cursor.execute(
        DataBase.queries.get_player_query, [nick])
      dbRecord = DataBase.db.cursor.fetchone()
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
          if indents == 0:
            data['Changes'] = 'Nothing'
            indents += 1
          else:
            DataBase.db.conn.commit()
            # Calculate new etag 
            DataBase.db.cursor.execute(
              DataBase.queries.get_player_query, [nick])
            dbRecord = DataBase.db.cursor.fetchone()
            response = {}
            response['Response'] = 'Specific player successfully geted.'
            response['Player'] = buildPlayerJSON_db(dbRecord)
            self.write(response)
            self.set_my_etag_header()
            # Vanish response
            self._write_buffer = []
          self.write(json.dumps(data, sort_keys=True, indent=indents))
          return
      # Nick is wrong err.  
      else:  
        errData['Cause'] = 'Player not found.'
        raise HTTPError(HTTPStatus.NOT_FOUND) # 422 Error Code
    # Nick is missing err.
    else:
      errData['Cause'] = 'Nick is missing.'
      raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
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
            #TODO comment that default after debugging
            # default: '"ETag"' 
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
            description: Nick is missing.
          "404":
            description: Nick is wrong.
          "428":
            description: Precondition Required. Etag is missing.
          "412":
            description: Precondition Failed. Entity is modified.
    """
    #EODescription end-point    
    if nick:
      dbRecord = getPlayerFromDatabaseByNick(nick)
      if dbRecord:
        # Check precondition.
        response = {}
        response['Response: '] = 'Specific player successfully geted.'
        response['Player: '] = buildPlayerJSON_db(dbRecord)
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
          json_data = json.loads(self.request.body.decode("utf-8"))
          if len(json_data) == 3: 
            # todo Check if got 3 arguments = records, no_msg_received and no_msg_sended
            if "points_record" and "no_msg_sended" and "no_msg_received" in json_data:
              query_data = (dbRecord[0], dbRecord[1], int(json_data['points_record']),
                int(json_data['no_msg_sended']), int(json_data['no_msg_received']), str(nick))
              DataBase.db.cursor.execute(
                  DataBase.queries.put_player_query, query_data)
              DataBase.db.conn.commit()
              # Calculate new etag 
              DataBase.db.cursor.execute(
                DataBase.queries.get_player_query, [nick])
              dbRecord = DataBase.db.cursor.fetchone()
              response = {}
              response['Response: '] = 'Specific player successfully geted.'
              response['Player: '] = buildPlayerJSON_db(dbRecord)
              self.write(response)
              self.set_my_etag_header()
              # Vanish response
              self._write_buffer = []
              data = {}
              data['Player before update:'] = buildPlayerJSON_db(dbRecord)
              json_data['id'] = dbRecord[0]
              json_data['nick'] = dbRecord[1]
              player_json = buildPlayerJSON(json_data)
              data['Player after update:'] = player_json
              self.write(json.dumps(data, sort_keys=True, indent=2))
              return
      # Nick is wrong err.  
      else:  
        errData['Cause'] = 'Player not found.'
        raise HTTPError(HTTPStatus.NOT_FOUND) # 422 Error Code
    # Nick is missing err.
    else:
      errData['Cause'] = 'Nick is missing.'
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
  if getPlayerFromDatabaseByNick(nick): # If player exists raise error
    errData['Cause'] = 'Server did not delete player successfully. Player still exists.'
    raise HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR)