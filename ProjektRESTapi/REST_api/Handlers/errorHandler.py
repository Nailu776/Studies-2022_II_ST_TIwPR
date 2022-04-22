import http.client
from tornado.web            import RequestHandler, ErrorHandler

class BaseHandler(RequestHandler):
    def write_error(self, status, **kwargs):
        self.write("HTTP error code: {} {}\n".format(str(status),
                http.client.responses[status]))

class ErrorHandler(ErrorHandler, BaseHandler):
    pass
