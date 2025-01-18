import numpy as np
import utils
import pprint

from gamestate import GameState

class GoGame:
    def __init__(self):
        initial_board = np.zeros((utils.GRID_NUM, utils.GRID_NUM), dtype=int) # -1 for black, +1 for white, 0 for empty
        initial_state = GameState('Ongoing', initial_board, -1, {'black': 0, 'white': 0}, None)
        self.state = initial_state
        self.history = [] # queue of states

    def undo(self):
        """Undo the most recent move, if possible."""
        if self.history:
            self.history.pop()
            self.state = self.history[-1]

    def player_pass(self):
        print("Player passed.")
        # Simply switch the current color
        self.next_state(self.state, 'pass')

    def resign(self):
        print("Player resigned.")
        # You could handle end-of-game logic here
        self.next_state(self.state, 'resign')

    def get_neighbors(self, r, c):
        """Helper to get valid neighbors within the board."""
        neighbors = []
        for (nr, nc) in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]:
            if 0 <= nr < utils.GRID_NUM and 0 <= nc < utils.GRID_NUM:
                neighbors.append((nr, nc))
        return neighbors

    def find_group_and_liberties(self, state, row, col):
        """
        BFS (or DFS) to find:
         - all stones in the connected group containing (row, col)
         - the set of empty neighbor points (liberties) for that group
        """
        color = state.board[row, col]
        if color == 0:
            return [], set()  # empty space, no group
        
        visited = set()
        to_visit = [(row, col)]
        group_stones = []
        liberties = set()
        
        while to_visit:
            r, c = to_visit.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            group_stones.append((r, c))
            
            for (nr, nc) in self.get_neighbors(r, c):
                if state.board[nr, nc] == color:
                    to_visit.append((nr, nc))
                elif state.board[nr, nc] == 0:
                    liberties.add((nr, nc))
        
        return group_stones, liberties

    def next_state(self, state, move):
        """
        Attempt to place a stone of the current color at (row, col).
        If it's a valid move (not suicide unless it captures),
        update the board, handle captures, switch player, etc.
        """
        (row, col) = move
        
        if state.board[row, col] != 0:
            return None # not a valid move
        
        old_board = state.board.copy()
        
        # Place the stone tentatively
        state.board[row, col] = state.cur_player
        
        captured_anything = False
        
        # Check adjacent groups of the opponent color
        opponent_color = -state.cur_player
        neighbors = self.get_neighbors(row, col)
        opp_groups_to_remove = []
        for (nr, nc) in neighbors:
            if state.board[nr, nc] == opponent_color:
                group_stones, liberties = self.find_group_and_liberties(state, nr, nc)
                if len(liberties) == 0:
                    # This group is captured
                    opp_groups_to_remove.append(group_stones)
        
        # Remove captured groups
        for grp in opp_groups_to_remove:
            captured_anything = True
            for (r, c) in grp:
                state.board[r, c] = 0  # remove from board
        
        # Check if newly placed stone’s group has liberties
        my_group, my_liberties = self.find_group_and_liberties(state, row, col)
        if len(my_liberties) == 0 and not captured_anything:
            # Suicide move
            # Revert to old board
            state.board = old_board
            return None
        
        # Check if board state is the same as before (ko violation):
        if any(np.array_equal(state.board, prev_board) for prev_board in self.history):
            state.board = old_board
            return None

        # Otherwise, move is valid
        b_captures = state.captures['black'] # white's dead stones
        w_captures = state.captures['white'] # black's dead stones
        print(opp_groups_to_remove)
        if len(opp_groups_to_remove) >= 1:
            if state.cur_player == 1:
                w_captures += len(opp_groups_to_remove[0])
            else:
                b_captures += len(opp_groups_to_remove[0])
        next_player = -state.cur_player

        return GameState('Ongoing', state.board.copy(), next_player, {'black': b_captures, 'white': w_captures}, (row, col))
