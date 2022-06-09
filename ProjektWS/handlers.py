from tornado.websocket import WebSocketHandler, WebSocketClosedError
from snake_game_manager import SnakeGameManager, InvalidGameIDError
from tornado.web import RequestHandler
from logg_config import logger
import struct


# Get frontend handler
class RenderHandler(RequestHandler):
    # Get render index html
    def get(self):
        self.render("snake_game.html")
# Decode action from int code
def _decode_my_action(short_action):
    # Python - no switch case 
    if(short_action == 3): # 11
        return "move"
    elif(short_action == 1): # 01
        return "join"
    elif(short_action == 0): # 00
        return "new"
    elif(short_action == 2): # 10
        return "resume"
    else: return "err"
# Websocket communication handler
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
        # Unpack action and decode it
        unpacked_msg = struct.unpack_from(">h",message,0)
        action = _decode_my_action(unpacked_msg[0])
        logger.debug("Got new message with action: '" + action + "'.")
        # What action to perform
        if action == "move":
            data_payload = struct.unpack_from(">hh",message,0)
            move_index = data_payload[1]
            logger.debug("Received move index: '" + str(move_index) + "'.")
            # op_move msg code is 2 and next arg is op move index
            op_move_msg = struct.pack(">hh",2,move_index)
            self.send_msg_to_op(op_payload=op_move_msg)
            return #TODO: move impl
        elif action ==  "new":
            # Create a new game and send msg
            self.game_id = self.game_manager.new_game(self)
            # NOTE: msg from server starting with 0 means wait
            # for opponent, and sends id of game as next arg
            wait_action = struct.pack(">hh",0,self.game_id)
            self.send_msg(payload=wait_action)
        elif action == "join":
            # Trying to get the game id
            try:
                data_payload = struct.unpack_from(">hh",message,0)
                game_id = data_payload[1]
                self.game_manager.join_game(game_id, self)
            except InvalidGameIDError:
                # Bad Id
                logger.error("Bad game id: '" + game_id + "'.")
            else:
                # Joining to the game.
                self.game_id = game_id
                # Start both players
                # 1 -> start game, True->player A, False->player B
                start_action_a = struct.pack(">h?",1,True)
                start_action_b = struct.pack(">h?",1,False)
                self.send_msg(payload=start_action_a)
                self.send_msg_to_op(op_payload=start_action_b)
        elif action == "resume":
            return # TODO: resume
        elif action == "err":
            return #err TODO:
        else: return #big error xd
    
    # Log info about origin
    def check_origin(self, origin):
        logger.info("Origin: " + origin)
        return True
    # Send msg to opponent    
    def send_msg_to_op(self, op_payload):
        # Check if got game id
        if not self.game_id:
            logger.error("Missing game id. in fun 'send_msg_to_op'")
            return
        try:
            # Get opponent handler
            op_handler = self.game_manager.get_op_handler(self.game_id, self)
        except InvalidGameIDError:
            logger.error("Inalid game id: " + self.game_id + ". Cannot send msg.")
        else:
            if op_handler:
                op_handler.send_msg(payload=op_payload)
    # Send msg to client
    def send_msg(self, payload):
        try:
            self.write_message(message= payload, binary= True)
        except WebSocketClosedError:
            logger.warning("WebSocketClosedError", "Could Not send Message.")
            # Send error info to another player 
            # NOTE: 4 means error happend - close websocket connection
            err_action = struct.pack(">h",4)
            self.send_msg_to_op(op_payload=err_action)
            # Close connection
            self.close()

# Routes
routes = [
    ("/", RenderHandler),
    ("/ws", WSHandler, dict(game_manager=SnakeGameManager())),
]