import sys
import signal
from sett_config import settings
from logg_config import logger
import tornado.web
from tornado.ioloop import IOLoop as tornIOLoop
from tornado.options import options

# End of program - sigint
def signal_handler(sig, frame):
    logger.info("You pressed Ctrl+C! End of program.")
    sys.exit(0)

if __name__ == "__main__":
    # Sigint handler
    signal.signal(signal.SIGINT, signal_handler)

    # Parse command line options if specified
    options.parse_command_line()
    
    # Apply settings
    app = tornado.web.Application(**settings)
    
    # Start Logger and Server
    logger.info("Starting App on Port: {} with Debug Mode: {}"
        .format(options.port, options.debug))
    app.listen(options.port)
    # Info before IOLoop start - how to end program
    logger.debug("Have a nice time debuging bugs! :)")
    logger.info("Press Ctrl+C to end ioloop.")
    # IOLoop start
    tornIOLoop.instance().start()