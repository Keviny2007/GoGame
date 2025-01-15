import pygame as pg
import pygame_widgets
from go import OFFSET, GRID_LEN, STONE_RADIUS, BOARD_LEN
from go import GoGame
from gobot import GoBot

'''game loop'''
def run_game():
    gobot = GoBot()
    gogame = GoGame()
    while 1:
        events = pg.event.get()
        for event in events:

            if event.type == pg.QUIT:
                # player quit game
                return

            if event.type == pg.MOUSEBUTTONDOWN:
                # place a stone
                mouse_pos = pg.mouse.get_pos()
                pos_ = (
                    round((mouse_pos[0]-OFFSET[0]) / GRID_LEN),
                    round((mouse_pos[1]-OFFSET[1]) / GRID_LEN)
                )
                gogame.next_state(pos_)
                if gogame.get_cur_stone_color()[0] == 255:
                    gogame.next_state(gobot.next_move())
                gogame.display_board()

        gogame.get_window().blit(gogame.get_board(), (0, 0))
        if OFFSET[0] - STONE_RADIUS <= pg.mouse.get_pos()[0] <= BOARD_LEN + OFFSET[0] + STONE_RADIUS and OFFSET[1] - STONE_RADIUS <= pg.mouse.get_pos()[1] <= BOARD_LEN + OFFSET[1] + STONE_RADIUS:
            pg.draw.circle(gogame.get_window(), gogame.get_cur_stone_color(),
                            pg.mouse.get_pos(), STONE_RADIUS)
        pygame_widgets.update(events)
        pg.display.update()

if __name__ == "__main__":
    run_game()
    
    