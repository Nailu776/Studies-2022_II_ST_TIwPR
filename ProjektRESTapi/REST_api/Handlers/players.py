from http import HTTPStatus
from tornado.web            import HTTPError
from Models.models import PlayerModel
import json
from .errorHandler import BaseHandler
import tornado
players = []
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
          Get Players from players_ranking.
      description: 
          This HTTP methode is used to get a list of players 
          sorted by the points they have earned in their games.
      operationId: getPlayers
      responses:
          "200":
              description: 
                  The ranking list successfully geted.
          "304":
              description: 
                  The ranking list has not been modified since the last get.
    """
    #EOD  
    self.write({'players': players})
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
              $ref: '#/components/schemas/PlayerModel'
        required: true
      responses:
          '200':
              description: Todo item created.
              content: {}
          '405':
              description: Invalid input
              content: {}
    """
    #EOD  
    players.append(json.loads(self.request.body))
    self.write({'message': 'New player created.'})

# Players Details Handler
# ~/players/{u_name} 
class PlayersDetailsH(BaseHandler):
  def get(self, id=None):
    """
      Description end-point
      ---
      tags:
        - Players
      summary: 
          Get single player details by ID.
      description: 
          This HTTP method is used to get the details 
          of a single player by ID of a specific player.
      operationId: getPlayer
      parameters:
        - name: id
          in: path
          description: ID of player to get.
          required: true
          schema:
            type: integer
            format: int64
      responses:
          "200":
              description: 
                  Specific player successfully geted.
          "304":
              description: 
                  Specific player has not been modified since the last get.
          "422":
              description: 
                  Wrong ID.
    """
    #EOD  
    if id:
      if int(id) < len(players):
          self.write({'player': players[int(id)]})
      else:
          """
              The HyperText Transfer Protocol (HTTP) 422 Unprocessable Entity response status code 
              indicates that the server understands the content type of the request entity, 
              and the syntax of the request entity is correct, but it was unable to process 
              the contained instructions.
          """
          #EOED  
          self.write({'message': 'ID out of range.'})
          raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
    else:
      """
          The HyperText Transfer Protocol (HTTP) 422 Unprocessable Entity response status code 
          indicates that the server understands the content type of the request entity, 
          and the syntax of the request entity is correct, but it was unable to process 
          the contained instructions.
      """
      #EOED 
      self.write({'message': 'ID missing.'})
      raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
  def patch(self, id=None):
    """
      Description end-point
      ---
      tags:
        - Players
      summary: 
          Update (PATCH) the specific details of a single player by ID.
      description: 
          This HTTP method is used to update (PATCH) the specific details 
          of a single player by ID of a specific player.
      operationId: patchPlayer
      parameters:
        - name: id
          in: path
          description: ID of player to patch.
          required: true
          schema:
            type: integer
            format: int64      
      requestBody:
        description: Update a specific player.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PlayerModel'
      responses:
          "200":
              description: 
                  Specific player successfully updated (puted).
          "422":
              description: 
                  Wrong ID.
    """
    #EOD  
    if id:
      if int(id) < len(players):
          data = {}
          indents = 0
          request_data = tornado.escape.json_decode(self.request.body)
          print( request_data.keys())
          # points_record update
          if 'points_record' in request_data.keys():
            players[int(id)]['points_record'] = int(request_data['points_record'])
            data['Player points_record updateed:'] = request_data['points_record']
            indents += 1
          # number of msg sendes update
          if 'no_msg_sended' in request_data.keys():
            players[int(id)]['no_msg_sended'] = int(request_data['no_msg_sended'])
            data['Player no_msg_sended updateed:'] = request_data['no_msg_sended']
            indents += 1
          # number of msg received update
          if 'no_msg_received' in request_data.keys():
            players[int(id)]['no_msg_received'] = int(request_data['no_msg_received'])
            data['Player no_msg_received updateed:'] = request_data['no_msg_received']
            indents += 1
          if indents == 0:
            data['Changes:'] = 'Nothing'
            indents += 1
          self.write(json.dumps(data, sort_keys=True, indent=indents))
      else:
          """
              The HyperText Transfer Protocol (HTTP) 422 Unprocessable Entity response status code 
              indicates that the server understands the content type of the request entity, 
              and the syntax of the request entity is correct, but it was unable to process 
              the contained instructions.
          """
          #EOED  
          self.write({'message': 'ID out of range.'})
          raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
    else:
      """
          The HyperText Transfer Protocol (HTTP) 422 Unprocessable Entity response status code 
          indicates that the server understands the content type of the request entity, 
          and the syntax of the request entity is correct, but it was unable to process 
          the contained instructions.
      """
      #EOED 
      self.write({'message': 'ID missing.'})
      raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
  def put(self, id=None):
    """
      Description end-point
      ---
      tags:
        - Players
      summary: 
          Update (PUT) single player details by ID.
      description: 
          This HTTP method is used to update (PUT) the details 
          of a single player by ID of a specific player.
      operationId: putPlayer
      parameters:
        - name: id
          in: path
          description: ID of player to put.
          required: true
          schema:
            type: integer
            format: int64      
      requestBody:
        description: Update a specific player.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PlayerModel'
        required: true
      responses:
          "200":
              description: 
                  Specific player successfully updated (puted).
          "422":
              description: 
                  Wrong ID.
    """
    #EOD  
    if id:
      if int(id) < len(players):
          data = {}
          data['Player before update:'] = players[int(id)]
          #self.write({'Player before update:': players[int(id)]})
          #self.flush()
          players[int(id)] = json.loads(self.request.body)
          data['Player after update:'] = players[int(id)]
          #self.write({'Player after update:': players[int(id)]})
          self.write(json.dumps(data, sort_keys=True, indent=2))
      else:
          """
              The HyperText Transfer Protocol (HTTP) 422 Unprocessable Entity response status code 
              indicates that the server understands the content type of the request entity, 
              and the syntax of the request entity is correct, but it was unable to process 
              the contained instructions.
          """
          #EOED  
          self.write({'message': 'ID out of range.'})
          raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
    else:
      """
          The HyperText Transfer Protocol (HTTP) 422 Unprocessable Entity response status code 
          indicates that the server understands the content type of the request entity, 
          and the syntax of the request entity is correct, but it was unable to process 
          the contained instructions.
      """
      #EOED 
      self.write({'message': 'ID missing.'})
      raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
  def delete(self, id=None):
    """
      Description end-point
      ---
      tags:
        - Players
      summary: 
          Delete single player by ID.
      description: 
          This HTTP method is used to delete a single player by ID.
      operationId: deletePlayer
      parameters:
        - name: id
          in: path
          description: ID of player to delete.
          required: true
          schema:
            type: integer
            format: int64      
      responses:
          "200":
              description: 
                  Specific player successfully deleted.
          "422":
              description: 
                  Wrong ID.
    """
    #EOD  
    if id:
      if int(id) < len(players):
          del players[int(id)]
          self.write("Player with id: " + id + " is delted.")
      else:
          """
              The HyperText Transfer Protocol (HTTP) 422 Unprocessable Entity response status code 
              indicates that the server understands the content type of the request entity, 
              and the syntax of the request entity is correct, but it was unable to process 
              the contained instructions.
          """
          #EOED  
          self.write({'message': 'ID out of range.'})
          raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
    else:
      """
          The HyperText Transfer Protocol (HTTP) 422 Unprocessable Entity response status code 
          indicates that the server understands the content type of the request entity, 
          and the syntax of the request entity is correct, but it was unable to process 
          the contained instructions.
      """
      #EOED 
      self.write({'message': 'ID missing.'})
      raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
