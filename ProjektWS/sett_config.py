import os
from tornado.options import options, define
from handlers import routes

# Some defines 
APP_DIR = os.path.dirname(os.path.realpath(__file__))   
define("debug", default=True, help="Debug settings")
define("port", default=8888, help="Port to run the server on")
define("autoreload", default=True, help="Autoreload")
define("static_path", default=APP_DIR, help="Path to static stuff")
# Application settings 
settings = {
    "handlers": routes,
    "debug": options.debug,
    "autoreload": options.autoreload,
    # path to js
    "static_path": options.static_path,
}