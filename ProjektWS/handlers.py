from tornado.web import RequestHandler
import tornado.websocket
from logg_config import logger

class RenderHandler(RequestHandler):
    # Get render index html
    def get(self):
        self.render("index.html")

class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        logger.info("Open new game.")

    def on_close(self):
        logger.info("Connection closed.")

    def on_message(self, message):
        logger.info("Got message.")
        self.write_message(message + " OK")

    def check_origin(self, origin):
        logger.info("ORIGIN: " + origin)
        return True

routes = [
    ("/", RenderHandler),
    ("/ws", WSHandler),
]