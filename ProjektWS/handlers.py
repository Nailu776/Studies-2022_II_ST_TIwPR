from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from logg_config import logger
import json
from snake_game_manager import SnakeGameManager, InvalidGameError

class RenderHandler(RequestHandler):
    # Get render index html
    def get(self):
        self.render("snake_game.html")

class WSHandler(WebSocketHandler):
    # WebSocketHandler init
    def initialize(self, game_manager, *args, **kwargs):
        self.game_manager = game_manager
        self.game_id = None
        super().initialize(*args, **kwargs)
    # Open connection
    def open(self):
        logger.info("Connected to snake server.")
    # On connection close
    def on_close(self):
        logger.info("Connection closed.")
    # On message receive
    def on_message(self, message):
        logger.info("Got message.")
        data = json.loads(message)
        action = data.get("action", "")
        # What action to perform
        if action ==  "new":
            # Create a new game and send msg
            self.game_id = self.game_manager.new_game(self)
            self.send_msg(action="wait for enemy", game_id=self.game_id)
        elif action == "join":
            # Trying to get the game id
            try:
                game_id = int(data.get("game_id"))
                self.game_manager.join_game(game_id, self)
            except:
                # Bad Id
                logger.error("Bad game ID.")
            else:
                # Joining to the game.
                self.game_id = game_id
                # Start both players
                self.send_msg(action="start_player_b")
                self.send_msg_to_opponent(action="start_player_a")
    # Log info about origin
    def check_origin(self, origin):
        logger.info("ORIGIN: " + origin)
        return True
    # Send msg to opponent    
    def send_msg_to_opponent(self, action, **data):
        if not self.game_id:
            logger.error("No game id.")
            return
        try:
            opponent_handler = self.game_manager.get_opponent_handler(self.game_id, self)
        except InvalidGameError:
            logger.error("Inalid game id: "+self.game_id+". Cannot send msg: "+ data)
        else:
            if opponent_handler:
                opponent_handler.send_msg(action, **data)
    def send_msg(self, action, **data):
        message = {
            "action": action,
            "data": data
        }
        try:
            self.write_message(json.dumps(message))
        except WebSocketClosedError:
            logger.warning("WebSocketClosedError", "Could Not send Message: " + json.dumps(message))
            # Send error info to another player 
            self.send_msg_to_opponent(action="WebSocketClosedError")
            # Close connection
            self.close()

routes = [
    ("/", RenderHandler),
    ("/ws", WSHandler, dict(game_manager=SnakeGameManager())),
]