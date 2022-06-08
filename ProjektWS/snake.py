from logg_config import logger
# Invalid moves 
class InvalidMoveError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
# Game rules and maintaining state of game
class Snake(object):
    def __init__(self):
        self.game_result = ""
    def reset_game(self):
        self.game_result = ""
    def get_game_result(self):
        return self.game_result
    def set_game_result(self, value):
        self.game_result = value
    def has_ended(self):
        pass
    def abort_game(self):
        pass
    def player_move(self):
        pass