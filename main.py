from go import GoGame
from game import GameGUI

if __name__ == "__main__":
    game = GoGame()
    gui = GameGUI(game)
    gui.run()