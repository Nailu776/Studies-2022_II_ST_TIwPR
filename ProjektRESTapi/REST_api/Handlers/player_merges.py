from .errorHandler import BaseHandler, errData
from http import HTTPStatus
from tornado.web            import HTTPError
import DataBase
import json


# Schemas for Swagger
import Schemas.PlayerMergesSchemas

# Players_Merges Handler 
# ~/player_merges
class PlayerMergesH(BaseHandler):
    def post(self):
        """
        Description end-point
        ---
        tags:
            - Merges
        summary: 
            Create a new merge.
        description: 
            This HTTP method is used to create a new merge.
        operationId: addMerge      
        requestBody: 
            description: New merge attributes.
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/PlayerMergesSchema'
            required: true
        responses:
            '201':
                description: Players are merged successfully.
            '400':
                description: Expected correct 4 fulfilled 
                    JSON elements in request body.
            '500':
                description: Something unexpected happened.
        """
        #EODescription end-point

        try:
            # Decode request data
            request_data = json.loads(self.request.body.decode("utf-8"))
        except:
            errData['Cause'] = 'Check if request body is correct.'
            raise HTTPError(HTTPStatus.BAD_REQUEST)
        else:
            if len(request_data) != 4:
                errData['Cause'] = 'Request body require 4 elements.'
                raise HTTPError(HTTPStatus.BAD_REQUEST)
            else:
                # NOTE Check if got 4 arguments 
                # TODO Find out better method date, nick_first, nick_secound and nick_finall
                try:
                    if request_data['date']:
                        pass
                    if request_data['nick_first']:
                        pass
                    if request_data['nick_secound']:
                        pass 
                    if request_data['nick_final']:
                        pass 
                except:
                    errData['Cause'] = 'Check if request body is correct.'
                    raise HTTPError(HTTPStatus.BAD_REQUEST)
                else:
                    # Check if date is not empty
                    if not request_data['date']:
                        errData['Cause'] = 'Date is empty.'
                        raise HTTPError(HTTPStatus.BAD_REQUEST)

                    # Check if first nick exists
                    DataBase.db.cursor.execute(DataBase.queries.get_player_query, 
                    [request_data['nick_first']])
                    f_nick = DataBase.db.cursor.fetchone()
                    if not f_nick:
                        errData['Cause'] = 'First nick is wrong.'
                        raise HTTPError(HTTPStatus.BAD_REQUEST)

                    # Check if secound nick exists
                    DataBase.db.cursor.execute(DataBase.queries.get_player_query, 
                    [request_data['nick_secound']])
                    s_nick = DataBase.db.cursor.fetchone()
                    if not s_nick:
                        errData['Cause'] = 'Secound nick is wrong.'
                        raise HTTPError(HTTPStatus.BAD_REQUEST)

                    # Check if final nick is not empty
                    if not request_data['nick_final']:
                        errData['Cause'] = 'Final nick is empty.'
                        raise HTTPError(HTTPStatus.BAD_REQUEST)

                    # Check if final nick isn't first nick
                    if request_data['nick_final'] != request_data['nick_first']:
                        # Check if there is player with final nick 
                        DataBase.db.cursor.execute(
                            DataBase.queries.get_player_query,
                            [request_data['nick_final']])
                        dbRecord = DataBase.db.cursor.fetchone()
                        if dbRecord is not None:
                            errData['Cause'] = 'Final nick is not unique.'
                            raise HTTPError(HTTPStatus.BAD_REQUEST)
                    else:
                        # NOTE uncomment this code below (and next 'Note' code) 
                        # to ensure final nick must be unique so can't be equal to first nick 
                        # errData['Cause'] = 'Final nick is not unique.'
                        # raise HTTPError(HTTPStatus.BAD_REQUEST)
                        pass

                    # Create merge request
                    query_req = [ 
                        # MERGE REQUEST
                        request_data['date'],
                        request_data['nick_first'],
                        request_data['nick_secound'],
                        request_data['nick_final']
                    ]
                    query_data = [
                        #  UPDATE NICK
                        request_data['nick_final'],
                        #  SELECT RECORD
                        request_data['nick_first'],
                        request_data['nick_secound'],
                        #  SELECT NO_MSG_RECEIVED
                        request_data['nick_first'],
                        request_data['nick_secound'],
                        #  SELECT NO_MSG_SENDED
                        request_data['nick_first'],
                        request_data['nick_secound'],
                        # WHERE NICK = ?
                        request_data['nick_first']
                    ]
                    query_del = [
                        # DELETE NICK = ?
                        request_data['nick_secound']
                    ]
                    DataBase.db.cursor.execute(
                        DataBase.queries.execute_merge,
                        query_data)
                    DataBase.db.cursor.execute(
                        DataBase.queries.update_sended_mess,
                        [
                        request_data['nick_final'],
                        request_data['nick_secound']
                        ])
                    DataBase.db.cursor.execute(
                        DataBase.queries.update_received_mess,
                        [
                        request_data['nick_final'],
                        request_data['nick_secound']
                        ])
                    DataBase.db.cursor.execute(
                        DataBase.queries.delete_player_query,
                        query_del)
                    DataBase.db.cursor.execute(
                        DataBase.queries.create_merge_req,
                        query_req)
                    DataBase.db.conn.commit()

                    # Check if players are merged succesfully
                    # First nick can exist as final nick 
                    # NOTE Uncomment this code below if first nick shouldn't exist after merge
                    # DataBase.db.cursor.execute(
                    #     DataBase.queries.get_player_query, [request_data['nick_first']])
                    # if DataBase.db.cursor.fetchone() is not None:
                    #     errData['Cause'] = 'First nick still exists.'
                    #     raise HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR)
                    DataBase.db.cursor.execute(
                        DataBase.queries.get_player_query, [request_data['nick_secound']])
                    if DataBase.db.cursor.fetchone() is not None:
                        errData['Cause'] = 'Secound nick still exists.'
                        raise HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR)  
                    DataBase.db.cursor.execute(
                        DataBase.queries.get_player_query, [request_data['nick_final']])
                    if DataBase.db.cursor.fetchone() is None:
                        errData['Cause'] = 'Final nick does not exist.'
                        raise HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR)  

                    response = {}
                    response['Response'] = 'New merge done.'
                    response['New nick'] = request_data['nick_final']     
                    self.set_status(HTTPStatus.CREATED)
                    self.write(response)
    def get(self):
        """
        Description end-point
        ---
        tags:
            - Merges
        summary: 
            Get player merges.
        description: 
            This HTTP method is used to get all past merges.
        operationId: getMerges
        parameters:
            -   name: If-None-Match
                in: header
                required: false
                description: Used to check if we have an up-to-date list of merges.
                schema:
                    type: string
                    # NOTE default value is usefull for debuging
                    # default: '"ETag"'
        responses:
            "200":
                description: 
                    Merges list successfully geted.
            "304":
                description: 
                    Merges list not changed.
            "404":
                description:
                    Merges not found. Perhaps Database is empty.
        """
        #EODescription end-point

        DataBase.db.cursor.execute(
            DataBase.queries.get_all_merges)
        dbRecord = DataBase.db.cursor.fetchall()
        if dbRecord:
            response = {}
            response['Response'] = 'Merges list successfully geted.'
            mergesTab = []
            for records in dbRecord:
                mergesTab.append(buildMergesJSON_db(records))
            response['Merges'] = mergesTab
            self.write(response)
            # 304 if not modified
            self.check_modified_resp()
        else: 
            # Db is empty.   
            errData['Cause'] = 'Merges not found.'
            # 404 Error Code
            raise HTTPError(HTTPStatus.NOT_FOUND) 

# Players_Merges Details Handler 
# ~/player_merges/{pm_id}
class PlayerMergesDetailsH(BaseHandler):
    def get(self, pm_id):
        """
        Description end-point
        ---
        tags:
            - Merges
        summary: 
            Get specific merge (specified by id).
        description: 
            This HTTP method is used to get specific merge by id.
        operationId: getMerge
        parameters:
            -   name: pm_id
                in: path
                description: Id of merge.
                schema:
                    type: string
        responses:
            "200":
                description: 
                    Merge info successfully geted.
            "400":
                description:
                    Perhaps ID of merge is missing.
            "404":
                description:
                    Wrong ID. Merge info not found.
        """
        #EODescription end-point  

        if pm_id:
            DataBase.db.cursor.execute(
                DataBase.queries.get_merge_by_id, [pm_id])
            dbRecord = DataBase.db.cursor.fetchone()
            if dbRecord:
                response = {}
                response['Response'] = 'Merge info successfully geted.'
                response['Merge'] = buildMergesJSON_db(dbRecord)
                self.write(response)
            else: 
                # Id is wrong err.   
                errData['Cause'] = 'ID is wrong. Merge not found.'
                # 404 Error Code
                raise HTTPError(HTTPStatus.NOT_FOUND) 
        else: 
            # ID is missing err.
            errData['Cause'] = 'Check for missing ID of merge.'
            # 400 Error Code
            raise HTTPError(HTTPStatus.BAD_REQUEST) 

# Build JSON merge from db record
def buildMergesJSON_db(dbRecord):
    merge_json = {}
    merge_json['ID'] = dbRecord[0]
    merge_json['DATE'] = dbRecord[1]
    merge_json['NICK_FIRST'] = dbRecord[2]
    merge_json['NICK_SECOUND'] = dbRecord[3]
    merge_json['NICK_FINALL'] = dbRecord[4]
    return merge_json