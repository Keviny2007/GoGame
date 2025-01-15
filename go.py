import pygame as pg
import numpy as np
from pygame_widgets.button import Button

GRID_NUM = 19
WINDOW_SIZE = (1080, 720) #1080, 720
BOARD_LEN = min(WINDOW_SIZE) * 0.8
OFFSET = ((WINDOW_SIZE[0]-BOARD_LEN)/2, (WINDOW_SIZE[1]-BOARD_LEN)/2) # gaps on the edge
GRID_LEN = BOARD_LEN / (GRID_NUM-1)
STONE_RADIUS = GRID_LEN * 0.5
X_CORDS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']


class GoGame:
    def __init__(self):
        pg.init()
        self.gameboard = np.zeros((19, 19), dtype=int) # -1 black, 1 white, 0 empty
        self.cur_stone_color = [0, 0, 0]
        self.blackgroups: list[list[(float, float)]] = []
        self.whitegroups: list[list[(float, float)]] = []
        self.window = pg.display.set_mode(WINDOW_SIZE)
        self.board = None # visual surface
        self.just_eaten = []
        self.recent_move = None
        self.display_board()
        self.save_button = Button(
            self.window, 50, 100, 100, 50, text='Undo',
            fontSize=30, margin=20,
            inactiveColour=(147, 153, 152),
            pressedColour=(147, 153, 152), radius=20,
            onClick=self.undo
        )
        self.load_button = Button(
            self.window, 50, 325, 100, 50, text='Pass',
            fontSize=30, margin=20,
            inactiveColour=(147, 153, 152),
            pressedColour=(147, 153, 152), radius=20,
            onClick=self.player_pass
        )
        self.replay_button = Button(
            self.window, 50, 550, 100, 50, text='Resign',
            fontSize=30, margin=20,
            inactiveColour=(147, 153, 152),
            pressedColour=(147, 153, 152), radius=20,
            onClick=self.resign
        )

    def undo(self):
        return
    
    def player_pass(self):
        return
    
    def resign(self):
        return

    def get_board(self):
        return self.board
    
    def get_window(self):
        return self.window
    
    def get_cur_stone_color(self):
        return self.cur_stone_color

    def display_board(self):
        '''draw a background'''
        board = pg.Surface(WINDOW_SIZE)
        area = (OFFSET[0] - GRID_LEN, OFFSET[1] - GRID_LEN, 2*GRID_LEN + BOARD_LEN, 2*GRID_LEN + BOARD_LEN)
        board.fill(color=(125, 125, 125))
        board.fill(color=(242, 194, 111), rect=area)

        font = pg.font.SysFont('chalkduster.ttf', 20)
        
        '''draw board padding'''
        pg.draw.line(board, color=(0, 0, 0), start_pos=(OFFSET[0] - GRID_LEN, BOARD_LEN + OFFSET[1] + GRID_LEN), end_pos=(OFFSET[0] - GRID_LEN, OFFSET[1] - GRID_LEN))
        pg.draw.line(board, color=(0, 0, 0), start_pos=(OFFSET[0] + BOARD_LEN + GRID_LEN, BOARD_LEN + OFFSET[1] + GRID_LEN), end_pos=(OFFSET[0] + BOARD_LEN + GRID_LEN, OFFSET[1] - GRID_LEN))
        pg.draw.line(board, color=(0, 0, 0), start_pos=(OFFSET[0] - GRID_LEN, BOARD_LEN + OFFSET[1] + GRID_LEN), end_pos=(OFFSET[0] + BOARD_LEN + GRID_LEN, BOARD_LEN + OFFSET[1] + GRID_LEN))
        pg.draw.line(board, color=(0, 0, 0), start_pos=(OFFSET[0] - GRID_LEN, OFFSET[1] - GRID_LEN), end_pos=(OFFSET[0] + BOARD_LEN + GRID_LEN, OFFSET[1] - GRID_LEN))

        '''draw coordinates'''
        space = 0
        for cord in X_CORDS:
            text = font.render(cord, True, (0,0,0))
            board.blit(text, (OFFSET[0] + space - 6, BOARD_LEN+OFFSET[1] + STONE_RADIUS))
            board.blit(text, (OFFSET[0] + space - 6, OFFSET[1] - 2*STONE_RADIUS))
            space += GRID_LEN
        
        space = 0
        for i in range(19):
            text = font.render(str(i+1), True, (0,0,0))
            board.blit(text, ((OFFSET[0] - 2*STONE_RADIUS), BOARD_LEN+OFFSET[1] - 8 - space))
            board.blit(text, ((BOARD_LEN + OFFSET[0] + STONE_RADIUS), BOARD_LEN+OFFSET[1] - 8 - space))
            space += GRID_LEN

        '''draw lines to form grids'''
        #vertical
        for grid_x_idx in range(GRID_NUM):
            pg.draw.line(
                board,
                color=(0, 0, 0),
                start_pos=(grid_x_idx * GRID_LEN+OFFSET[0], OFFSET[1]),
                end_pos=(grid_x_idx * GRID_LEN+OFFSET[0], BOARD_LEN+OFFSET[1])
            )
        #horizontal
        for grid_x_idx in range(GRID_NUM):
            pg.draw.line(
                board,
                color=(0, 0, 0),
                start_pos=(OFFSET[0], grid_x_idx * GRID_LEN+OFFSET[1]),
                end_pos=(BOARD_LEN+OFFSET[0], grid_x_idx * GRID_LEN+OFFSET[1])
            )
        
        '''draw star points'''
        y = OFFSET[1] + GRID_LEN * 3
        x = OFFSET[0] + GRID_LEN * 3
        for i in range(3):
            for j in range(3):
                pg.draw.circle(board, (0, 0, 0), (x+i*6*GRID_LEN, y+j*6*GRID_LEN), 4)
                
        # draw blackgroups whitegroups
        for group in self.blackgroups:
            for move in group:
                stone = (
                    OFFSET[0] + GRID_LEN*move[0],
                    OFFSET[1] + GRID_LEN*move[1]
                )
                pg.draw.circle(board, (0, 0, 0), stone, STONE_RADIUS)
        for group in self.whitegroups:
            for move in group:
                stone = (
                    OFFSET[0]+move[0]*GRID_LEN,
                    OFFSET[1]+move[1]*GRID_LEN
                )
                pg.draw.circle(board, (255, 255, 255), stone, STONE_RADIUS)

        # mark most recent move
        if self.recent_move:
            stone = (
                OFFSET[0]+self.recent_move[0]*GRID_LEN,
                OFFSET[1]+self.recent_move[1]*GRID_LEN
            ) 
            if self.cur_stone_color[0] == 0: # mark on white stone
                pg.draw.circle(board, (0, 0, 0), stone, 0.6*STONE_RADIUS)
                pg.draw.circle(board, (255, 255, 255), stone, 0.4*STONE_RADIUS)
            else: # mark on black stone
                pg.draw.circle(board, (255, 255, 255), stone, 0.6*STONE_RADIUS)
                pg.draw.circle(board, (0, 0, 0), stone, 0.4*STONE_RADIUS)

        '''draw background to the screen'''
        self.window.blit(board, (0, 0))
        self.board = board

    '''get legal moves'''
    '''FIX LOGIC HERE, INCORPORATE SHINKAI LOGIC INTO NEW INTERNAL REPRESENTATION'''
    def legal_moves(self) -> list[tuple[int]]:
        res = []
        for i in range(len(self.gameboard)):
            for j in range(len(self.gameboard[0])):
                move = (i, j)
                # check if there's already a stone (occupied)
                if self.occupied(move):
                    continue
                # check if just eaten (ko)
                if len(self.just_eaten)==1 and move in self.just_eaten: 
                    continue
                res.append(move)
        return res                

    '''returns the next state'''        
    def next_state(self, move: tuple[int]):
        '''draw a stone based on player's mouse position'''
        # update
        # self.blackgroups
        # self.whitegroups
        if move in self.legal_moves():
            self.recent_move = move
        else:
            return

        # append into stone groups
        if self.cur_stone_color[0] == 0:
            # black
            tmp = [x.copy() for x in self.blackgroups]
            # if current postion is neighbor of some existing group
            merged_group = [move]
            for group in self.blackgroups[::-1]:
                for stone in group:
                    candidates = [
                        (stone[0], stone[1]+1),
                        (stone[0], stone[1]-1),
                        (stone[0]+1, stone[1]),
                        (stone[0]-1, stone[1]),
                    ]
                    if move in candidates:
                        # new stone is neighbor of current group
                        self.blackgroups.remove(group) # take out since it will be updated
                        merged_group += group
                        break

            self.blackgroups.append(merged_group) # # previous group was updated
            if self.eating_whitegroups(): 
                pass
            elif self.black_suicide(): 
                self.blackgroups=tmp 
                return

        else:
            # white
            # if current postion is neighbor of some existing group
            merged_group = [move]
            tmp = [x.copy() for x in self.whitegroups]
            for group in self.whitegroups[::-1]:

                for stone in group:
                    candidates = [
                        (stone[0], stone[1]+1),
                        (stone[0], stone[1]-1),
                        (stone[0]+1, stone[1]),
                        (stone[0]-1, stone[1]),
                    ]
                    if move in candidates:
                        # new stone is neighbor of current group
                        self.whitegroups.remove(group) # take out since it will be updated
                        merged_group += group
                        break

            self.whitegroups.append(merged_group) # previous group was updated
            if self.eating_blackgroups(): 
                pass
            elif self.white_suicide(): 
                self.whitegroups=tmp
                return
        self.cur_stone_color = [255-x for x in self.cur_stone_color]
        

    def eating_whitegroups(self) -> bool:
        self.just_eaten = []
        length = len(self.whitegroups)
        have_eaten = False
        for idx, group in enumerate(self.whitegroups[::-1]):
            idx = length-1-idx
            # white group
            can_eat_cur_group = True
            for stone in group:
                if not can_eat_cur_group: 
                    break
                candidates = [
                    (stone[0], stone[1]+1),
                    (stone[0], stone[1]-1),
                    (stone[0]+1, stone[1]),
                    (stone[0]-1, stone[1]),
                ]

                # check if candidates are in bounds
                for candidate in candidates[::-1]:
                    for cord in candidate:
                        if cord not in range(19):
                            candidates.remove(candidate)

                # check if candidates are occupied
                for candidate in candidates:
                    if not self.occupied(candidate):  # if a neighbor doesn't have a stone, group can't be eaten
                        can_eat_cur_group = False
                        break
            if can_eat_cur_group:
                self.just_eaten += self.whitegroups.pop(idx)  # list addtion
                have_eaten = True
        
        return have_eaten

    def eating_blackgroups(self) -> bool:
        self.just_eaten = []
        length = len(self.blackgroups)
        have_eaten = False
        for idx, group in enumerate(self.blackgroups[::-1]):
            idx = length-1-idx
            # black group
            can_eat_cur_group = True
            for stone in group:
                if not can_eat_cur_group:
                    break
                candidates = [
                    (stone[0], stone[1]+1),
                    (stone[0], stone[1]-1),
                    (stone[0]+1, stone[1]),
                    (stone[0]-1, stone[1]),
                ]

                for candidate in candidates[::-1]:
                    for cord in candidate:
                        if cord not in range(19):
                            candidates.remove(candidate)

                # check if candidates are occupied
                for candidate in candidates:
                    if not self.occupied(candidate):  # if a neighbor doesn't have a stone, group can't be eaten
                        can_eat_cur_group = False
                        break
            if can_eat_cur_group:
                self.just_eaten += self.blackgroups.pop(idx)
                have_eaten = True
        
        return have_eaten

    def black_suicide(self) -> bool:
        length = len(self.blackgroups)
        have_eaten = False
        for idx, group in enumerate(self.blackgroups[::-1]):
            idx = length-1-idx
            # black group
            can_eat_cur_group = True
            for stone in group:
                if not can_eat_cur_group:
                    break
                candidates = [
                    (stone[0], stone[1]+1),
                    (stone[0], stone[1]-1),
                    (stone[0]+1, stone[1]),
                    (stone[0]-1, stone[1]),
                ]

                for candidate in candidates[::-1]:
                    for cord in candidate:
                        if cord not in range(19):
                            candidates.remove(candidate)

                # check if candidates are occupied
                for candidate in candidates:
                    if not self.occupied(candidate):  # if a neighbor doesn't have a stone, group can't be eaten
                        can_eat_cur_group = False
                        break
            if can_eat_cur_group:
                return True

        return have_eaten

    def white_suicide(self) -> bool:
        length = len(self.whitegroups)
        have_eaten = False
        for idx, group in enumerate(self.whitegroups[::-1]):
            idx = length-1-idx
            # white group
            can_eat_cur_group = True
            for stone in group:
                if not can_eat_cur_group:
                    break
                candidates = [
                    (stone[0], stone[1]+1),
                    (stone[0], stone[1]-1),
                    (stone[0]+1, stone[1]),
                    (stone[0]-1, stone[1]),
                ]

                for candidate in candidates[::-1]:
                    for cord in candidate:
                        if cord not in range(19):
                            candidates.remove(candidate)

                # check if candidates are occupied
                for candidate in candidates:
                    if not self.occupied(candidate):  # if a neighbor doesn't have a stone, group can't be eaten
                        can_eat_cur_group = False
                        break
            if can_eat_cur_group:
                return True
        
        return have_eaten

    def occupied(self, stone) -> bool:
        for group in self.whitegroups:
            for pos_ in group:
                if pos_ == stone:
                    return True
        for group in self.blackgroups:
            for pos_ in group:
                if pos_ == stone:
                    return True
        return False



