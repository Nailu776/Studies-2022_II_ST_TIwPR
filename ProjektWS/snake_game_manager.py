from logg_config import logger
from snake import Snake
class InvalidGameIDError(Exception):
    # No game with given id
    pass
    
class SnakeGameManager(object):
    # Games set and next game id
    def __init__(self):
        self.games = {}
        self.next_game_id = 0
    # Get game from games set
    def get_game(self, game_id):
        game = self.games.get(game_id)
        if game:
            return game
        else:
            # No game with given id
            raise InvalidGameIDError
    # Gets next game id
    def get_next_game_id(self):
        # If more than 254 games reset id counter
        # TODO: MAKE IT SAFE
        if self.next_game_id >= 255:
            self.next_game_id = 0
        self.next_game_id += 1
        return self.next_game_id
    # Create new game
    def new_game(self, player_a_handler):
        game_id = self.get_next_game_id()
        self.games[game_id] = {
            "player_a_handler": player_a_handler
        }
        game = self.get_game(game_id)
        #Snake game
        game["snake"] = Snake()
        return game_id
    # Join game
    def join_game(self, game_id, player_b_handler):
        game = self.get_game(game_id)
        if game.get("player_b_handler") is None:
            game["player_b_handler"] = player_b_handler
            return game_id
        else:
            # No game with given ID
            raise InvalidGameIDError
    # Resume game
    def resume_game(self, game_id, player_handler, player):
        game = self.get_game(game_id)
        if game:
            if player is True:
                game["player_a_handler"] = player_handler
            else:
                game["player_b_handler"] = player_handler
        else:
            # No game with given ID
            raise InvalidGameIDError
    # Check if move is eating food
    def check_food(self, game_id, board_index):
        game = self.get_game(game_id)
        return game["snake"].check_eating_food(board_index)
    # Get food index
    def get_food_index_on_board(self, game_id):
        game = self.get_game(game_id)
        return game["snake"].get_food_index()
    # Reset game
    def reset_game(self, game_id):
        game = self.get_game(game_id)
        game["snake"].reset_game()
    # End game 
    def end_game(self, game_id):
        if game_id in self.games:
            del self.games[game_id]
            logger.debug("Games:"+str(self.games))
        else:
            raise InvalidGameIDError
    # Get opponent Handler
    def get_op_handler(self, game_id, handler):
        game = self.get_game(game_id)
        if handler == game.get("player_a_handler"):
            return game.get("player_b_handler")
        elif handler == game.get("player_b_handler"):
            return game.get("player_a_handler")
        else:
            raise InvalidGameIDError
    # Abort game TODO:
    def abort_game(self, game_id):
        game = self.get_game(game_id)
        snake = game["snake"]
        snake.abort_game()