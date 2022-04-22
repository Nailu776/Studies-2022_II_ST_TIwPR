from tornado.web            import Application
from tornado.ioloop         import IOLoop
from tornado                import options 
from tornado_swagger.setup  import setup_swagger

class Application(Application):
    _routes = [

        ]
    def __init__(self):
        settings = {
            "debug": True,
            "autoreload": True
            }
        setup_swagger(
            self._routes, 
            swagger_url="/REST_doc"
            )
        super(Application, self).__init__(self._routes, **settings)


if __name__ == "__main__":
    options.define("port", default="8000", help="Port to listen on")
    options.parse_command_line()
    app = Application()
    app.listen(port=8000)
    IOLoop.current().start()