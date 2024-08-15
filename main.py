##### IMPORTS #####
from src.board import Board
from src import constants
from src.game import Game
from src.ai import AI

import pygame
import sys

###################

##### USER CHOICE PvP or AI #####
def draw_selection_screen(screen) -> int:
    screen.fill(constants.BACKGROUND_COLOR)
    font = pygame.font.Font(None, 36)

    pvp_text = font.render("1. Player vs Player", True, constants.BORDER_LINE)
    pvai_text = font.render("2. Player vs AI", True, constants.BORDER_LINE)

    pvp_rect = pvp_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 50))
    pvai_rect = pvai_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 50))

    screen.blit(pvp_text, pvp_rect)
    screen.blit(pvai_text, pvai_rect)

    return pvp_rect, pvai_rect

##### Pygame Initialization #####

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
#screen.fill(constants.BACKGROUND_COLOR)
clock = pygame.time.Clock()

##### Instance of Class

# Game Instance (logic)
game = Game()
print(f"Game Mode: {game.gamemode}")

# Board Instance
board = Board(constants.WIDTH, constants.HEIGHT, game)

ai = AI(game)
print(f"AI init with level {ai.level}")

# Add title
pygame.display.set_caption("Ultimate TIC-TAC-TOE")


# Flags
running = True
game_over = False
game_started = False
vs_ai = False

##### MAIN LOOP #####

# To run the window, use the loop
while running:
    # pygame.QUIT event means the user clicked X to close the window.
    for event in pygame.event.get():

        #### QUIT EVENT ####
        if event.type == pygame.QUIT:
            running = False

            

        #### SELECTION SCREEN ####
        if not game_started:
            pvprect, pvairect = draw_selection_screen(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvprect.collidepoint(event.pos):
                    game_started = True
                    vs_ai = False
                elif pvairect.collidepoint(event.pos):
                    game_started = True
                    vs_ai = True
        else:
            # If the mouse is clicked it will switch to
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                # How to access the coordinate to link the console board to the GUI
                # MOUSEBUTTONDOWN -> Return position
                # https://www.pygame.org/docs/ref/event.html#pygame.event.get
                mouseX, mouseY = event.pos

                # Are we gonna use conditionals to have a boundary within the board?
                # Still using the coordinate return by the MOUSEBUTTONDOWN, then use // to get the floor division
                clicked_row = int(mouseY // board.cell_size)
                clicked_col = int(mouseX // board.cell_size)
                # Why column is in X? -> Remember in pygame, x increases to the right, so we need to make it column
                # Why row is in Y? -> Same logic to x, y increases downwards making it y as row


                if game.space_is_available(clicked_row, clicked_col):
                    game.mark_move(clicked_row, clicked_col, game.current_player)
                    if game.check_win(game.current_player):
                        print(f"Player {game.current_player} wins!")
                        game_over = True
                        #board.display_restart_message(screen)
                    elif game.is_board_full():
                        print("It's draw")
                        game_over = True
                        #board.display_restart_message(screen)
                    else:
                        game.switch_player()
                        if vs_ai and game.current_player == 2 and game.gamemode == 'ai':
                            # AI move
                            pygame.display.update()
                            print("Calling AI Eval")
                            ai_move = ai.eval(game)
                            if ai_move is not None:
                                row, col = ai_move
                                if game.space_is_available(row, col):
                                    game.mark_move(row, col, game.current_player)
                                    if game.check_win(game.current_player):
                                        print("AI wins!")
                                        game_over = True
                                    elif game.is_board_full():
                                        print("It's a draw")
                                        game_over = True
                                    else:
                                        game.switch_player()
                            else:
                                print("No more Moves")
                                game_over = True
                
            if game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game.restart()
                    board.restart(screen)
                    game_over = False

        if game_started:
            screen.fill(constants.BACKGROUND_COLOR)
            board.draw(screen)
            board.draw_figures(screen)
            if game_over:
                board.draw_win_line(screen)
                board.display_restart_message(screen)
            

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()