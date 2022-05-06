from .errorHandler import BaseHandler, errData
from http import HTTPStatus
from tornado.web            import HTTPError
import DataBase
import json


# Schemas for Swagger
import Schemas.HistoriesSchemas

# Histories Handler 
# ~/histories 
class HistoriesH(BaseHandler):
    def post(self):
        """
        Description end-point
        ---
        tags:
            - Histories
        summary: 
            Create a new game history exactly once by POST-PUT method.
        description: >
            This HTTP method is used to create a new game history 
            exactly once by POST-PUT method.
        operationId: addHistory
        responses:
            '200':
                description: PUT history on location in response.
        """
        # EODescription end-point
        DataBase.db.cursor.execute(
            DataBase.queries.poe_post_dummy_history_query)
        dbRecord = DataBase.db.cursor.lastrowid
        DataBase.db.conn.commit()
        response = {}
        response['Response'] = 'PUT history on location in response header.'
        response['Location'] = dbRecord
        self.write(response)
        self.add_header('Location', dbRecord)
    def get(self):
        """
        Description end-point
        ---
        tags:
            - Histories
        summary: 
            Get game histories.
        description: 
            This HTTP method is used to get all histories of past games.
        operationId: getHistories
        parameters:
            -   name: If-None-Match
                in: header
                required: false
                description: Used to check if we have an up-to-date history.
                schema:
                    type: string
                    # NOTE default value is usefull for debuging
                    # default: '"ETag"' 
            -   name: limit
                in: query
                required: false
                description: Limit the number of histories to get.
                schema:
                    type: integer
                    format: int64
            -   name: page
                in: query
                required: false
                description: Number of page of histories to get.
                schema:
                    type: integer
                    format: int64
        responses:
            "200":
                description: 
                    Histories successfully geted.
            "304":
                description: 
                    Histories not changed.
            "404":
                description:
                    Histories not found. Perhaps Database is empty.
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
        DataBase.db.cursor.execute(
            DataBase.queries.get_all_histories, get_query_data)
        dbRecord = DataBase.db.cursor.fetchall()
        if dbRecord:
            response = {}
            response['Response'] = 'Histories successfully geted.'
            historiesTab = []
            for records in dbRecord:
                historiesTab.append(buildHistoryJSON_db(records))
            response['Histories'] = historiesTab
            self.write(response)
            self.check_modified_resp()
        else: 
            # Db is empty.   
            errData['Cause'] = 'Histories not found.'
            # 404 Error Code
            raise HTTPError(HTTPStatus.NOT_FOUND) 

# Histories Details Handler 
# ~/histories/{g_id} 
class HistoriesDetailsH(BaseHandler):
    def get(self, g_id):
        """
        Description end-point
        ---
        tags:
            - Histories
        summary: 
            Get specific history (specified by game name).
        description: 
            This HTTP method is used to get specific history by game name.
        operationId: getHistory
        parameters:
            -   name: g_id
                in: path
                description: Unique name of game.
                schema:
                    type: string
        responses:
            "200":
                description: 
                    History successfully geted.
            "400":
                description:
                    Something is missing. Check name of game.
            "404":
                description:
                    Wrong name. Game not found.
        """
        #EODescription end-point  
        if g_id:
            DataBase.db.cursor.execute(
                DataBase.queries.get_history_with_name, [g_id])
            dbRecord = DataBase.db.cursor.fetchone()
            if dbRecord:
                response = {}
                response['Response'] = 'History successfully geted.'
                response['History'] = buildHistoryJSON_db(dbRecord)
                self.write(response)
            else: 
                # Name is wrong err.   
                errData['Cause'] = 'History of this game is not found. Check name.'
                # 404 Error Code
                raise HTTPError(HTTPStatus.NOT_FOUND) 
        else: 
            # Name is missing err.
            errData['Cause'] = 'Check for missing name of game.'
            # 400 Error Code
            raise HTTPError(HTTPStatus.BAD_REQUEST) 
    def put(self, g_id):
        """
        Description end-point
        ---
        tags:
            - Histories
        summary: 
            Create a new game history exactly once by POST-PUT method.
        description: >
            This HTTP method is used to create a new game history 
            exactly once by POST-PUT method.
        operationId: addHistory123   
        parameters:
            -   name: g_id
                in: path
                required: false
                description: Limit the number of players to get.
                required: true
                schema:
                    type: integer
                    format: int64
        requestBody: 
            description: New history attributes.
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/HistoriesSchema'
            required: true
        responses:
            '200':
                description: New game history added.
            '400':
                description: Expected 3 fulfilled JSON elements in request body.
            '500':
                description: Something unexpected happened and new History does not exist.
        """
        # EODescription end-point 
        try:
            h_id = int(g_id)
            DataBase.db.cursor.execute(
                DataBase.queries.get_history_with_id, [h_id])
            dbRecord = DataBase.db.cursor.fetchone()
            if dbRecord is None:
                # It should be DummyHistory
                errData['Cause'] = 'Check if Location is correct.'
                raise HTTPError(HTTPStatus.BAD_REQUEST)
            else:
                if dbRecord[3] != "DummyHistory":
                    errData['Cause'] = 'Check if Location is correct.'
                    raise HTTPError(HTTPStatus.BAD_REQUEST)
        except:
            errData['Cause'] = 'Check if Location is correct.'
            raise HTTPError(HTTPStatus.BAD_REQUEST)

        try:
            # Decode request data
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
                # date, g_name and players_tab
                try:
                    if request_data['date']:
                        pass
                    if request_data['g_name']:
                        pass
                    if request_data['players_tab']:
                        pass 
                except:
                    errData['Cause'] = 'Check if request body is correct.'
                    raise HTTPError(HTTPStatus.BAD_REQUEST)
                else:
                    # Check if date is not empty
                    if not request_data['date']:
                        errData['Cause'] = 'Date is empty.'
                        raise HTTPError(HTTPStatus.BAD_REQUEST)

                    # Check if g_name is not empty
                    if not request_data['g_name']:
                        errData['Cause'] = 'Game name is empty.'
                        raise HTTPError(HTTPStatus.BAD_REQUEST)

                    # Check if players_tab is not empty
                    if not request_data['players_tab']:
                        errData['Cause'] = 'Players tab is empty.'
                        raise HTTPError(HTTPStatus.BAD_REQUEST)

                    # Check if there is game with given name
                    DataBase.db.cursor.execute(
                        DataBase.queries.get_history_with_name,
                        [request_data['g_name']])
                    dbRecord = DataBase.db.cursor.fetchone()
                    if dbRecord is not None:
                        errData['Cause'] = 'Game name is not unique.'
                        raise HTTPError(HTTPStatus.BAD_REQUEST)

                    # Add new game history
                    # NOTE CREATE STRING FROM ARRAY OF {PLAYER, POINTS}
                    converterTab = {}
                    converterTab['players_tab'] = request_data['players_tab']
                    stringTab = json.dumps(converterTab)
                    DataBase.db.cursor.execute(
                        DataBase.queries.poe_put_history_query,
                        [request_data['date'],
                        request_data['g_name'],
                        stringTab, h_id])
                    DataBase.db.conn.commit()

                    # Get added history
                    DataBase.db.cursor.execute(
                        DataBase.queries.get_history_with_name,
                        [request_data['g_name']])
                    dbRecord = DataBase.db.cursor.fetchone()
                    
                    if dbRecord:
                        # Write response
                        response = {}
                        response['Response'] = 'New history added.'
                        response['Game History'] = buildHistoryJSON_db(dbRecord) 
                        self.set_status(HTTPStatus.CREATED) 
                        self.write(response)
                    else:
                        errData['Cause'] = 'New history was not added.'
                        raise HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR)

# Build JSON History from db record
def buildHistoryJSON_db(dbRecord):
    history_json = {}
    history_json['ID'] = dbRecord[0]
    history_json['DATE'] = dbRecord[1]
    history_json['G_NAME'] = dbRecord[2]
    # NOTE parsing string into json array
    history_json['PLAYERS_TAB'] = json.loads(dbRecord[3])
    return history_json