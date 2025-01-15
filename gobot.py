import random
from go import GoGame

class GoBot:
    def __init__(self):
        return
    
    def next_move(self) -> tuple:
        gogame = GoGame()
        valid_move = False
        while not valid_move:
            x = random.randint(0, 18)
            y = random.randint(0, 18)
            move = (x, y)
            valid_move = move in gogame.legal_moves()
        return move