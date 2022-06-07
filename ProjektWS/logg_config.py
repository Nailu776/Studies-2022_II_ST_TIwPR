import logging

# Logger settings
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
FORMAT = '[ %(levelname)s\t%(asctime)s %(name)s ] %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
