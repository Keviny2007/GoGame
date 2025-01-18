import copy
import pprint

class GameState:
    def __init__(self, status, board, cur_player, captures: dict, recent_move):
        self.status = status
        self.board = board
        self.cur_player = cur_player
        self.captures = captures
        self.recent_move = recent_move

    def clone(self):
        return GameState(
            status=self.status,
            board=copy.deepcopy(self.board),
            cur_player=self.cur_player,
            captures=copy.deepcopy(self.captures)
        )
