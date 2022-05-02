from http import HTTPStatus
import http.client
from tornado.web            import HTTPError
import json
from .errorHandler import BaseHandler, errData
import DataBase
import Schemas.MessageSchemas
import hashlib
from asyncio.windows_events import NULL
from typing import   Optional
# Build JSON message from db record
def buildMessageJSON_db(dbRecord):
    message_json = {}
    message_json['ID'] = dbRecord[0]
    message_json['SENDER_NICK'] = dbRecord[1]
    message_json['RECEIVER_NICK'] = dbRecord[2]
    message_json['TEXT_MESSAGE'] = dbRecord[3]
    return message_json
# Messages Handler 
# ~/messages 
class MessagesH(BaseHandler):
    def post(self):
        """
        Description end-point
        ---
        tags:
            - Messages
        summary: 
            Create a new message.
        description: 
            This HTTP method is used to create a new message.
        operationId: addMessage      
        requestBody: 
            description: New message attributes.
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/MessagePostSchema'
            required: true
        responses:
            '200':
                description: New message sended.
            '417':
                description: Expected 3 fulfilled JSON arguments in request body.
            '500':
                description: Something unexpected happend.
        """
        #EODescription end-point

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
                # text_message, sender_nick and receiver_nick
                try:
                    if request_data['text_message']:
                        pass
                    if request_data['sender_nick']:
                        pass
                    if request_data['receiver_nick']:
                        pass 
                except:
                    errData['Cause'] = 'Check if request body is correct.'
                    raise HTTPError(HTTPStatus.EXPECTATION_FAILED)
                else:
                    # Check if message is not empty
                    if not request_data['text_message']:
                        errData['Cause'] = 'Message is empty.'
                        raise HTTPError(HTTPStatus.EXPECTATION_FAILED)

                    # Check if sender exists
                    DataBase.db.cursor.execute(DataBase.queries.get_player_query, 
                    [request_data['sender_nick']])
                    s_nick = DataBase.db.cursor.fetchone()
                    if not s_nick:
                        errData['Cause'] = 'Sender nick is wrong.'
                        raise HTTPError(HTTPStatus.EXPECTATION_FAILED)

                    # Check if receiver exists
                    DataBase.db.cursor.execute(DataBase.queries.get_player_query, 
                    [request_data['receiver_nick']])
                    r_nick = DataBase.db.cursor.fetchone()
                    if not r_nick:
                        errData['Cause'] = 'Receiver nick is wrong.'
                        raise HTTPError(HTTPStatus.EXPECTATION_FAILED)

                    # Check if there is a similar message
                    DataBase.db.cursor.execute(
                        DataBase.queries.get_message_query,
                        [request_data['sender_nick'],
                        request_data['receiver_nick'],
                        request_data['text_message']])
                    dbRecord = DataBase.db.cursor.fetchall()
                    noSimilarMsg = len(dbRecord)

                    # Add new message
                    DataBase.db.cursor.execute(
                        DataBase.queries.add_message_query,
                        [request_data['sender_nick'],
                        request_data['receiver_nick'],
                        request_data['text_message']])
                    DataBase.db.conn.commit()

                    # Check if message is added
                    DataBase.db.cursor.execute(
                        DataBase.queries.get_message_query,
                        [request_data['sender_nick'],
                        request_data['receiver_nick'],
                        request_data['text_message']])
                    dbRecord = DataBase.db.cursor.fetchall()
                    noAddedMsg = len(dbRecord) - noSimilarMsg
                    
                    # Write response
                    response = {}
                    if noAddedMsg == 1:
                        response['Response'] = 'New message added.'
                        # Update numbers recived / sended msgs
                        DataBase.db.cursor.execute(
                            DataBase.queries.inc_message_sended_query,
                            [request_data['sender_nick']])
                        DataBase.db.cursor.execute(
                            DataBase.queries.inc_message_received_query,
                            [request_data['receiver_nick']])
                        DataBase.db.conn.commit()    
                    elif noAddedMsg == 0:
                        response['Response'] = 'Message was not added.' 

                    messagesFetched = []
                    for records in dbRecord:
                        messagesFetched.append(buildMessageJSON_db(records))
                    response['Message'] = messagesFetched     
                    self.write(response)


# MessagesGetterH Handler 
# ~/messages/{u_send},{u_receiv}
class MessagesGetterH(BaseHandler):
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
    def get(self, sender_nick, receiver_nick):
        """
        Description end-point
        ---
        tags:
            - Messages
        summary: 
            Get messages sended by sender and received by receiver nick.
        description: 
            This HTTP method is used to get messages by nicks of
            sender and receiver player.
        operationId: getMessages
        parameters:
            -   name: sender_nick
                in: path
                description: Nick of player that sended messages.
                required: true
                schema:
                    type: string
            -   name: receiver_nick
                in: path
                description: Nick of player that received messages.
                required: true
                schema:
                    type: string
            -   name: If-None-Match
                in: header
                required: false
                description: Used to check if we have an up-to-date message.
                schema:
                    type: string
                    #TODO comment that default after debugging
                    # default: '"ETag"'
        responses:
            "200":
                description: 
                    Messages successfully geted.
            "304":
                description: 
                    Messages have not been modified since the last get.
            "422":
                description: Missing or wrong nick/nicks.
        """
        #EODescription end-point
              
        if sender_nick and receiver_nick:
            DataBase.db.cursor.execute(DataBase.queries.get_messages_query, 
            [sender_nick, receiver_nick])
            dbRecord = DataBase.db.cursor.fetchall()
            if dbRecord:
                response = {}
                response['Response'] = 'Messages successfully geted.'
                messagesFetched = []
                for records in dbRecord:
                    messagesFetched.append(buildMessageJSON_db(records))
                response['Messages'] = messagesFetched
                self.write(response)
                self.check_modified_resp()
            else: 
                # Nick is wrong err.   
                errData['Cause'] = 'Check nicks to correct.'
                # 422 Error Code
                raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) 
        else: 
            # Nick is missing err.
            errData['Cause'] = 'Check for missing nicks.'
            # 422 Error Code
            raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) 


def getMessageFromDatabaseById(id):
  DataBase.db.cursor.execute(DataBase.queries.get_message_byID_query, [id])
  return DataBase.db.cursor.fetchone()
def checkMessageDeleted(id):
  if getMessageFromDatabaseById(id):
    # If message exists raise error
    errData['Cause'] = 'Server did not delete message successfully. Message still exists.'
    raise HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR)
# Messages Handler 
# ~/messages 
class MessagesDetailsH(BaseHandler):
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
    def delete(self, sender_nick, receiver_nick, id):
        """
        Description end-point
        ---
        tags:
            - Messages
        summary: 
            Delete single message by id (and sender's nick and receiver's nick ).
        description: 
            This HTTP method is used to delete a single message by id.
        operationId: deleteMessage
        parameters:
            -   name: sender_nick
                in: path
                description: Nick of sender player.
                required: true
                schema:
                    type: string 
            -   name: receiver_nick
                in: path
                description: Nick of receiver player.
                required: true
                schema:
                    type: string 
            -   name: id
                in: path
                description: Id of message to delete.
                required: true
                schema:
                    type: integer
                    format: int64
            -   name: If-Match
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
                    Specific Message successfully deleted.
            "422":
                description: Missing nick.
            "404":
                description: Message not found.
            "412":
                description: Precondition Failed. Entity changed.
            "428":
                description: Precondition Required. Etag is missing.
            "500":
                description: 
                    Server did not delete message successfully.  
                    Message still exists.
        """
        #EODescription end-point    

        if sender_nick and receiver_nick and id:
            dbRecord = getMessageFromDatabaseById(id)
            if dbRecord:
                # Check precondition.
                response = {}
                response['Response'] = 'Specific message successfully geted.'
                response['Message'] = buildMessageJSON_db(dbRecord)
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
                    DataBase.db.cursor.execute(DataBase.queries.delete_message_query, [id])
                    DataBase.db.conn.commit()
                    checkMessageDeleted(id)
                    self._headers['Content-Type'] = "text/html; charset=utf-8"
                    self.write("Message with id: " + id + " is successfully delted.")
                    return
            else:  
                # Nick is wrong err.  
                errData['Cause'] = 'Message not found.'
                # 404 Error Code
                raise HTTPError(HTTPStatus.NOT_FOUND) 
        # Nick is missing err.
        else:
            errData['Cause'] = 'Nicks or Id is missing.'
            # 422 Error Code
            raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) 
    def patch(self, sender_nick, receiver_nick, id):
        """
        Description end-point
        ---
        tags:
            - Messages
        summary: 
            Update (PATCH) the specific details of a single message by id.
        description: 
            This HTTP method is used to update (PATCH) the specific details 
            of a single message by id.
        operationId: patchMessage
        parameters:
            -   name: sender_nick
                in: path
                description: Nick of sender player.
                required: true
                schema:
                    type: string 
            -   name: receiver_nick
                in: path
                description: Nick of receiver player.
                required: true
                schema:
                    type: string 
            -   name: id
                in: path
                description: Id of message to delete.
                required: true
                schema:
                    type: integer
                    format: int64
            -   name: If-Match
                in: header
                required: false
                description: Used to prevent lost-update-problem.
                schema:
                    type: string
                    #TODO comment that default after debugging
                    default: '"ETag"' 
        requestBody:
            description: Update a specific message.
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/MessagePostSchema'
        responses:
            "200":
                description: 
                    Specific message successfully updated (patched).
            "422":
                description: Nicks or message is missing.
            "404":
                description: Id is wrong. Message not found.
            "412":
                description: Precondition Failed. Entity changed.
            "428":
                description: Precondition Required. Etag is missing.
        """
        #EODescription end-point
         
        if sender_nick and receiver_nick and id:
            dbRecord = getMessageFromDatabaseById(id)
            if dbRecord:
                # Check precondition.
                response = {}
                response['Response'] = 'Specific message successfully geted.'
                response['Message'] = buildMessageJSON_db(dbRecord)
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
                    # sender_nick update
                    if 'sender_nick' in json_data:
                        query_data = (json_data['sender_nick'], id)
                        DataBase.db.cursor.execute(
                        DataBase.queries.patch_msg_sender_nick_query, query_data)
                        data['Message sender_nick updated'] = json_data['sender_nick']
                        indents += 1
                    # receiver_nick update
                    if 'receiver_nick' in json_data:
                        query_data = (json_data['receiver_nick'], id)
                        DataBase.db.cursor.execute(
                        DataBase.queries.patch_msg_receiver_nick_query, query_data)
                        data['Message receiver_nick updated'] = json_data['receiver_nick']
                        indents += 1
                    # text_message update
                    if 'text_message' in json_data:
                        query_data = (json_data['text_message'], id)
                        DataBase.db.cursor.execute(
                        DataBase.queries.patch_msg_text_message_query, query_data)
                        data['Message text_message updated'] = json_data['text_message']
                        indents += 1
                    if indents == 0:
                        data['Changes '] = 'Nothing'
                        indents += 1
                    else:
                        DataBase.db.conn.commit()
                        # Calculate new etag 
                        dbRecord = getMessageFromDatabaseById(id)
                        response = {}
                        response['Response'] = 'Specific message successfully geted.'
                        response['Message'] = buildMessageJSON_db(dbRecord)
                        self.write(response)
                        self.set_my_etag_header()
                        # Vanish response
                        self._write_buffer = []
                    self.write(json.dumps(data, sort_keys=True, indent=indents))
                    return
            # Nick is wrong err.  
            else:  
                errData['Cause'] = 'Message not found.'
                raise HTTPError(HTTPStatus.NOT_FOUND) # 422 Error Code
        # Nick is missing err.
        else:
            errData['Cause'] = 'Nicks or message is missing.'
            raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) # 422 Error Code
    def put(self, sender_nick, receiver_nick, id):
        """
        Description end-point
        ---
        tags:
            - Messages
        summary: 
            Update (PUT) single message details by id.
        description: 
            This HTTP method is used to update (PUT) the details 
            of a single message by id.
        operationId: putMessage
        parameters:
            -   name: sender_nick
                in: path
                description: Nick of sender player.
                required: true
                schema:
                    type: string 
            -   name: receiver_nick
                in: path
                description: Nick of receiver player.
                required: true
                schema:
                    type: string 
            -   name: id
                in: path
                description: Id of message to delete.
                required: true
                schema:
                    type: integer
                    format: int64
            -   name: If-Match
                in: header
                required: false
                description: Used to prevent lost-update-problem.
                schema:
                    type: string
                    #TODO comment that default after debugging
                    default: '"ETag"'  
        requestBody:
            description: Update a specific message.
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/MessagePostSchema'
        responses:
            "200":
                description: 
                    Specific message successfully updated (patched).
            "422":
                description: Something is missing (Id or nicks).
            "404":
                description: Message not found. Id is wrong.
            "412":
                description: Precondition Failed. Entity changed.
            "417":
                description: Something in request body is wrong.
            "428":
                description: Precondition Required. Etag is missing.
        """
        #EODescription end-point    

        if sender_nick and receiver_nick and id:
            dbRecord = getMessageFromDatabaseById(id)
            if dbRecord:
                # Check precondition.
                response = {}
                response['Response'] = 'Specific message successfully geted.'
                response['Message'] = buildMessageJSON_db(dbRecord)
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
                    # Decode request data
                    request_data = json.loads(self.request.body.decode("utf-8"))
                    if len(request_data) != 3:
                        errData['Cause'] = 'Request body require 3 elements.'
                        raise HTTPError(HTTPStatus.EXPECTATION_FAILED)
                    else:
                        #TODO Check if got 3 arguments = text_message, sender_nick and receiver_nick
                        try:
                            if request_data['text_message']:
                                pass
                            if request_data['sender_nick']:
                                pass
                            if request_data['receiver_nick']:
                                pass 
                        except:
                            errData['Cause'] = 'Check if request body is correct.'
                            raise HTTPError(HTTPStatus.EXPECTATION_FAILED)
                        else:
                            # Check if message is not empty
                            if not request_data['text_message']:
                                errData['Cause'] = 'Message is empty.'
                                raise HTTPError(HTTPStatus.EXPECTATION_FAILED)

                            # Check if sender exists
                            DataBase.db.cursor.execute(DataBase.queries.get_player_query, 
                            [request_data['sender_nick']])
                            s_nick = DataBase.db.cursor.fetchone()
                            if not s_nick:
                                errData['Cause'] = 'Sender nick is wrong.'
                                raise HTTPError(HTTPStatus.EXPECTATION_FAILED)

                            # Check if receiver exists
                            DataBase.db.cursor.execute(DataBase.queries.get_player_query, 
                            [request_data['receiver_nick']])
                            r_nick = DataBase.db.cursor.fetchone()
                            if not r_nick:
                                errData['Cause'] = 'Receiver nick is wrong.'
                                raise HTTPError(HTTPStatus.EXPECTATION_FAILED)

                            # UPDATE message 
                            query_data = (request_data['sender_nick'],
                                request_data['receiver_nick'], request_data['text_message'], id)
                            DataBase.db.cursor.execute(
                                DataBase.queries.put_msg_query, query_data)
                            DataBase.db.conn.commit()
                            # Calculate new etag 
                            dbRecord = getMessageFromDatabaseById(id)
                            data = {}
                            data['Message before update'] = response['Message']
                            response['Message'] = buildMessageJSON_db(dbRecord)
                            self.write(response)
                            self.set_my_etag_header()
                            # Vanish response
                            self._write_buffer = []
                            data['Message after update'] = response['Message']
                            self.write(json.dumps(data, sort_keys=True, indent=2))
                            return 
            else: 
                # Id is wrong err.  
                errData['Cause'] = 'Message not found. Id is wrong.'
                # 404 Error Code
                raise HTTPError(HTTPStatus.NOT_FOUND) 
        else:
            # Nick or id is missing err.
            errData['Cause'] = 'Something is missing (Id or nicks).'
            # 422 Error Code
            raise HTTPError(HTTPStatus.UNPROCESSABLE_ENTITY) 