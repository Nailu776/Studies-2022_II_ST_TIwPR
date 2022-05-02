from .errorHandler import BaseHandler, errData
from http import HTTPStatus
from tornado.web            import HTTPError
import DataBase
from asyncio.windows_events import NULL
from typing import   Optional
import hashlib
import Schemas.HistoriesSchemas
import json
# Build JSON History from db record
def buildHistoryJSON_db(dbRecord):
    history_json = {}
    history_json['ID'] = dbRecord[0]
    history_json['DATE'] = dbRecord[1]
    history_json['G_NAME'] = dbRecord[2]
    # NOTE parsing string into json array
    history_json['PLAYERS_TAB'] = json.loads(dbRecord[3])
    return history_json
class HistoriesH(BaseHandler):
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
    def post(self):
        """
        Description end-point
        ---
        tags:
            - Histories
        summary: 
            Create a new game history.
        description: 
            This HTTP method is used to create a new game history.
        operationId: addMessage      
        requestBody: 
            description: New message attributes.
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/HistoriesSchema'
            required: true
        responses:
            '200':
                description: New game history added.
            '417':
                description: Expected 3 fulfilled JSON elements in request body.
            '500':
                description: Something unexpected happened and new History does not exist.
        """
        # EODescription end-point

        try:
            # Decode request data
            request_data = json.loads(self.request.body.decode("utf-8"))
        except:
            errData['Cause'] = 'Check if request body is correct.'
            raise HTTPError(HTTPStatus.EXPECTATION_FAILED)
        else:
            if len(request_data) != 3:
                errData['Cause'] = 'Request body require 3 elements.'
                raise HTTPError(HTTPStatus.EXPECTATION_FAILED)
            else:
                # NOTE Check if got 3 arguments
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
                    raise HTTPError(HTTPStatus.EXPECTATION_FAILED)
                else:
                    # Check if date is not empty
                    if not request_data['date']:
                        errData['Cause'] = 'Date is empty.'
                        raise HTTPError(HTTPStatus.EXPECTATION_FAILED)

                    # Check if g_name is not empty
                    if not request_data['g_name']:
                        errData['Cause'] = 'Game name is empty.'
                        raise HTTPError(HTTPStatus.EXPECTATION_FAILED)

                    # Check if players_tab is not empty
                    if not request_data['players_tab']:
                        errData['Cause'] = 'Players tab is empty.'
                        raise HTTPError(HTTPStatus.EXPECTATION_FAILED)

                    # Check if there is game with given name
                    DataBase.db.cursor.execute(
                        DataBase.queries.get_history_with_name,
                        [request_data['g_name']])
                    dbRecord = DataBase.db.cursor.fetchone()
                    if dbRecord is not None:
                        errData['Cause'] = 'Game name is not unique.'
                        raise HTTPError(HTTPStatus.EXPECTATION_FAILED)

                    # Add new game history
                    # NOTE CREATE STRING FROM ARRAY OF {PLAYER, POINTS}
                    converterTab = {}
                    converterTab['players_tab'] = request_data['players_tab']
                    stringTab = json.dumps(converterTab)
                    DataBase.db.cursor.execute(
                        DataBase.queries.add_history_query,
                        [request_data['date'],
                        request_data['g_name'],
                        stringTab])
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
                        self.write(response)
                    else:
                        errData['Cause'] = 'New history was not added.'
                        raise HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR)
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

        DataBase.db.cursor.execute(
            DataBase.queries.get_all_histories)
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

class HistoriesDetailsH(BaseHandler):
    def get(self, g_name):
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
            -   name: g_name
                in: path
                description: Unique name of game.
                schema:
                    type: string
        responses:
            "200":
                description: 
                    History successfully geted.
            "417":
                description:
                    Something is missing. Check name of game.
            "404":
                description:
                    Wrong name. Game not found.
        """
        #EODescription end-point  
        if g_name:
            DataBase.db.cursor.execute(
                DataBase.queries.get_history_with_name, [g_name])
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
            # 422 Error Code
            raise HTTPError(HTTPStatus.EXPECTATION_FAILED) 