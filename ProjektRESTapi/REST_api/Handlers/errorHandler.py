from http import HTTPStatus
import http.client
from tornado.web            import RequestHandler, ErrorHandler
import json
errData = {}
errData['Cause'] = 'Nickname is missing or wrong.' 
"""
    The HyperText Transfer Protocol (HTTP) 422 Unprocessable Entity response status code 
    indicates that the server understands the content type of the request entity, 
    and the syntax of the request entity is correct, but it was unable to process 
    the contained instructions.
"""
#EOErrDesc  
class BaseHandler(RequestHandler):
    def write_error(self, status, **kwargs):
        self.write("HTTP error code: {} {}\n".format(str(status),
                http.client.responses[status]))  
        self.write("Cause: " + errData['Cause'])
        # self.write(json.dumps(errData,
        #                  skipkeys = True,
        #                  allow_nan = True,
        #                  indent = 1))

class ErrorHandler(ErrorHandler, BaseHandler):
    pass
