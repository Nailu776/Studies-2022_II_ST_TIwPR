import this                 #__Easter Egg__: The Zen of Python, by Tim Peters 
from tornado.web            import Application, RequestHandler, url, ErrorHandler, HTTPError
from tornado.ioloop         import IOLoop
from tornado                import options 
from tornado_swagger.setup  import setup_swagger
from Handlers.players import PlayersH
from Handlers.players import PlayersDetailsH
#from Handlers.test_players import PlayersDetailsH
from DataBase import db
import signal
import sys

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    try:
        db.conn.commit()
        db.conn.close()
    except:
        print('Database is perhaps already closed.')
    finally:
        print('End of program.')
    sys.exit(0)


class Application(Application):
    _routes = [
        url("/players", PlayersH, name= "Players Handler"),
        url(r"/players/([^/]+)?", PlayersDetailsH, name= "Players Details Handler"),  
        ]
    def __init__(self):
        settings = {
            "debug": True,
            "autoreload": True,
            "default_handler_class": ErrorHandler,
            'default_handler_args': dict(status_code=404)
            }
        setup_swagger(
            self._routes, 
            swagger_url="/RESTdoc"
            )
        super(Application, self).__init__(self._routes, **settings)

if __name__ == "__main__":
    options.define("port", default="8000", help="Port to listen on")
    options.parse_command_line()
    db.init() # Init Database
    app = Application()
    app.listen(port=8000)
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to end loop')
    IOLoop.current().start()