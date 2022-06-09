from random import randint, random
from logg_config import logger
# Invalid moves 
class InvalidMoveError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
# Game rules and maintaining state of game
class Snake(object):
    def __init__(self):
        self.food_index = 0
        self.game_result = ""
    def get_food_index(self):
        return self.food_index
    def check_eating_food(self, board_index):
        if self.food_index == board_index:
            self.food_index = randint(0,399)
            return True
        return False
    def reset_game(self):
        self.game_result = ""
        self.food_index = randint(0,399)
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