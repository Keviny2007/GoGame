import pygame as pg
import copy
import utils
import pprint

from pygame_widgets.button import Button
from go import GoGame

class GameGUI:
    def __init__(self, game):
        pg.init()
        self.game = game
        self.window = pg.display.set_mode(utils.WINDOW_SIZE)
        self.buttons = self.create_buttons()
        self.board_surface = None        
        self.display_board(game.state)

    def create_buttons(self):
        return [
            Button(
            self.window, 50, 100, 100, 50, text='Undo',
            fontSize=30, margin=20,
            inactiveColour=(147, 153, 152),
            pressedColour=(147, 153, 152), radius=20,
            onClick=self.game.undo
        ),
            Button(
            self.window, 50, 325, 100, 50, text='Pass',
            fontSize=30, margin=20,
            inactiveColour=(147, 153, 152),
            pressedColour=(147, 153, 152), radius=20,
            onClick=self.game.player_pass
        ),
            Button(
            self.window, 50, 550, 100, 50, text='Resign',
            fontSize=30, margin=20,
            inactiveColour=(147, 153, 152),
            pressedColour=(147, 153, 152), radius=20,
            onClick=self.game.resign
        )
        ]

    def display_board(self, state):
        """
        Draw everything:
        - Wooden background
        - Grid lines
        - Coordinates
        - Stones from gameboard
        - Mark the most recent move
        """
        board = pg.Surface(utils.WINDOW_SIZE)
        
        # Background color
        area = (utils.OFFSET[0] - utils.GRID_LEN, utils.OFFSET[1] - utils.GRID_LEN,
                2*utils.GRID_LEN + utils.BOARD_LEN, 2*utils.GRID_LEN + utils.BOARD_LEN)
        board.fill(color=(125, 125, 125))  # dark grey background
        board.fill(color=(242, 194, 111), rect=area)  # "wooden" color for board
        
        # Draw board boundary lines
        pg.draw.rect(board, (0, 0, 0), area, width=2)
        
        font = pg.font.SysFont('chalkduster.ttf', 20)
        
        # Draw coordinate labels (A-S, 1-19)
        # Horizontal (X) labels
        space = 0
        for cord in utils.X_CORDS:
            text = font.render(cord, True, (0,0,0))
            board.blit(text, (utils.OFFSET[0] + space - 6, utils.BOARD_LEN+utils.OFFSET[1] + utils.STONE_RADIUS))
            board.blit(text, (utils.OFFSET[0] + space - 6, utils.OFFSET[1] - 2*utils.STONE_RADIUS))
            space += utils.GRID_LEN
        
        # Vertical (Y) labels
        space = 0
        for i in range(utils.GRID_NUM):
            text = font.render(str(i+1), True, (0,0,0))
            board.blit(text, (utils.OFFSET[0] - 2*utils.STONE_RADIUS,
                              utils.BOARD_LEN+utils.OFFSET[1] - 8 - space))
            board.blit(text, (utils.BOARD_LEN + utils.OFFSET[0] + utils.STONE_RADIUS,
                              utils.BOARD_LEN+utils.OFFSET[1] - 8 - space))
            space += utils.GRID_LEN
        
        # Draw grid lines
        for i in range(utils.GRID_NUM):
            # vertical line
            start_x = utils.OFFSET[0] + i * utils.GRID_LEN
            pg.draw.line(board, (0,0,0),
                         (start_x, utils.OFFSET[1]),
                         (start_x, utils.OFFSET[1] + utils.BOARD_LEN))
            
            # horizontal line
            start_y = utils.OFFSET[1] + i * utils.GRID_LEN
            pg.draw.line(board, (0,0,0),
                         (utils.OFFSET[0], start_y),
                         (utils.OFFSET[0] + utils.BOARD_LEN, start_y))
        
        # Draw star points (3x3, 3x9, 3x15, etc.)
        star_offsets = [3, 9, 15] if utils.GRID_NUM == 19 else []
        for sx in star_offsets:
            for sy in star_offsets:
                px = utils.OFFSET[0] + sx * utils.GRID_LEN
                py = utils.OFFSET[1] + sy * utils.GRID_LEN
                pg.draw.circle(board, (0,0,0), (px, py), 4)
        
        # Draw stones from self.gameboard
        for row in range(utils.GRID_NUM):
            for col in range(utils.GRID_NUM):
                if state.board[row, col] == -1:  # black
                    px = utils.OFFSET[0] + col * utils.GRID_LEN
                    py = utils.OFFSET[1] + row * utils.GRID_LEN
                    pg.draw.circle(board, (0, 0, 0), (px, py), utils.STONE_RADIUS)
                elif state.board[row, col] == 1:  # white
                    px = utils.OFFSET[0] + col * utils.GRID_LEN
                    py = utils.OFFSET[1] + row * utils.GRID_LEN
                    pg.draw.circle(board, (255, 255, 255), (px, py), utils.STONE_RADIUS)

        # Display Captures
        cap_font = pg.font.SysFont('chalkduster.ttf', 30)
        b_cap = cap_font.render("Black Captures: %d" % (state.captures['black']), True, (0,0,0))
        w_cap = cap_font.render("White Captures: %d" % (state.captures['white']), True, (0,0,0))
        board.blit(b_cap, (0.82*utils.WINDOW_SIZE[0], 0.4*utils.WINDOW_SIZE[1]))
        board.blit(w_cap, (0.82*utils.WINDOW_SIZE[0], 0.5*utils.WINDOW_SIZE[1]))

        # Mark most recent move 
        if state.recent_move:
            stone = (
                utils.OFFSET[0] + state.recent_move[1] * utils.GRID_LEN,  # col index
                utils.OFFSET[1] + state.recent_move[0] * utils.GRID_LEN   # row index
            )
            if state.cur_player == -1:  # Mark on white stone
                pg.draw.circle(board, (0, 0, 0), stone, 0.6 * utils.STONE_RADIUS)
                pg.draw.circle(board, (255, 255, 255), stone, 0.4 * utils.STONE_RADIUS)
            else:  # Mark on black stone
                pg.draw.circle(board, (255, 255, 255), stone, 0.6 * utils.STONE_RADIUS)
                pg.draw.circle(board, (0, 0, 0), stone, 0.4 * utils.STONE_RADIUS)
        
        # Blit to the main window
        self.window.blit(board, (0, 0))
        pg.display.update()
        
        self.board_surface = board

    def run(self):
        """
        Main loop (simplified). In your actual code, you'd probably integrate
        this with event handling for Pygame. 
        """
        running = True
        clock = pg.time.Clock()
        
        while running:
            clock.tick(30)
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    running = False
                
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # Translate click position into board row/col
                    mx, my = pg.mouse.get_pos()
                    col = round((mx - utils.OFFSET[0]) / utils.GRID_LEN)
                    row = round((my - utils.OFFSET[1]) / utils.GRID_LEN)
                    
                    if 0 <= row < utils.GRID_NUM and 0 <= col < utils.GRID_NUM:
                        new_state = self.game.next_state(self.game.state, (row, col))
                        if new_state:
                            self.game.state = new_state
                            self.game.history.append(copy.deepcopy(new_state.board))
                            # print('='*150)
                            # pprint.pprint(self.game.history)
                            self.display_board(self.game.state)
            # Update the button states
            """self.undo_button.listen(events)
            self.undo_button.draw()
            
            self.pass_button.listen(events)
            self.pass_button.draw()
            
            self.resign_button.listen(events)
            self.resign_button.draw()"""
            self.window.blit(self.board_surface, (0, 0))

            mx, my = pg.mouse.get_pos()
            if utils.OFFSET[0] - utils.STONE_RADIUS <= mx <= utils.BOARD_LEN + utils.OFFSET[0] + utils.STONE_RADIUS and utils.OFFSET[1] - utils.STONE_RADIUS <= my <= utils.BOARD_LEN + utils.OFFSET[1] + utils.STONE_RADIUS:
                # Round to snap the cursor stone into place
                col = round((mx - utils.OFFSET[0]) / utils.GRID_LEN)
                row = round((my - utils.OFFSET[1]) / utils.GRID_LEN)
                if 0 <= row < utils.GRID_NUM and 0 <= col < utils.GRID_NUM and self.game.state.board[row, col] == 0:
                    color = (0, 0, 0) if self.game.state.cur_player == -1 else (255, 255, 255)
                    px = utils.OFFSET[0] + col * utils.GRID_LEN
                    py = utils.OFFSET[1] + row * utils.GRID_LEN
                    pg.draw.circle(self.window, color, (px, py), utils.STONE_RADIUS)

            pg.display.flip()
        
        pg.quit()