
from logg_config import logger
from snake import Snake
class InvalidGameError(Exception):
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
            logger.error("No game with given id.")
            raise InvalidGameError
    # Gets next game id
    def get_next_game_id(self):
        # If more than 999 games reset id counter
        if self.next_game_id > 999:
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
        #Snake  TODO: 
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
            logger.error("No game with given id.")
            raise InvalidGameError
    # End game 
    def end_game(self, game_id):
        if game_id in self.games:
            del self.games[game_id]
        else:
            logger.warn("Game id is not in games list" + game_id)
    # Get opponent Handler TODO:
    def get_opponent_handler(self, game_id, handler):
        game = self.get_game(game_id)
        if handler == game.get("player_a_handler"):
            return game.get("player_b_handler")
        elif handler == game.get("player_b_handler"):
            return game.get("player_a_handler")
        else:
            logger.error("No game with given id.")
            raise InvalidGameError
    # Record move in game instance TODO:
    def move(self, game_id, move, handler):
        game = self.get_game(game_id)
        if handler == game.get("player_a_handler"):
            game["snake"].player_move(move)
        elif handler == game.get("player_b_handler"):
            game["snake"].player_move(move)
    # Abort game TODO:
    def abort_game(self, game_id):
        game = self.get_game(game_id)
        snake = game["snake"]
        snake.abort_game()
    # Is game ended TODO:
    def has_game_ended(self, game_id):
        return False
    # Get game result TODO:
    def get_game_result(self, game_id, handler):
        pass