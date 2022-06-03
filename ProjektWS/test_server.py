import tornado.web
import tornado.websocket
import tornado.ioloop
import logging
import logging.config
from tornado.web import RequestHandler
from tornado.options import options, define
import signal
import sys
import os

def signal_handler(sig, frame):
    logger.info('You pressed Ctrl+C!')
    logger.info('End of program.')
    sys.exit(0)

class EchoGETHandler(RequestHandler):
    # Get render index html
    def get(self):
        self.render("index.html")

class EchoHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        logger.info("open")

    def on_close(self):
        logger.info("close")

    def on_message(self, message):
        logger.info("message")
        self.write_message(message + " OK")

    def check_origin(self, origin):
        logger.info("ORIGIN: " + origin)
        return True


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    options.parse_command_line()
    # Logger settings
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)
    routes = [
        ("/", EchoGETHandler),
        ("/ws", EchoHandler),
    ]
    # Some defines ( TODO: put them in another file)
    APP_DIR = os.path.dirname(os.path.realpath(__file__))   
    define("debug", default=True, help="Debug settings")
    define("port", default=8888, help="Port to run the server on")
    define("autoreload", default=True, help="Autoreload")
    define("static_path", default=APP_DIR, help="Path to static stuff")
    # Application settings (from TODO: another config-like file!)
    settings = {
        "handlers": routes,
        "debug": options.debug,
        "autoreload": options.autoreload,
        "static_path": options.static_path,
    }
    app = tornado.web.Application(**settings)
    # Start Logger and Server
    logger.info("Starting App on Port: {} with Debug Mode: {}".format(options.port, options.debug))
    app.listen(options.port)
    logger.debug("Have a nice time debuging bugs! :)")
    logger.info('Press Ctrl+C to end loop')
    tornado.ioloop.IOLoop.instance().start()