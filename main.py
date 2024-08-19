##### IMPORTS #####
from src.board import Board
from src import constants
from src.game import Game
from src.ai import AI

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
clock = pygame.time.Clock()

##### Instance of Class

game = Game(ai_first=False)
print(f"Game Mode: {game.gamemode}")

board = Board(constants.WIDTH, constants.HEIGHT, game)

ai = AI(game)
print(f"AI init with level {ai.level}")

# Add title
pygame.display.set_caption("TIC-TAC-TOE")


# Flags
running = True
game_over = False
game_started = False
vs_ai = False

ai_level = 0

#### RESET GAME
def reset_game() -> None:
    global game, board, ai, game_over, game_started, vs_ai, ai_level
    game.reset()
    board = Board(constants.WIDTH, constants.HEIGHT, game)
    ai = AI(game, ai_level) if vs_ai else None
    game_over = False
    game_started = False
    vs_ai = False
    ai_level = 0

def draw_dimmed_board(screen, board, winner_text):
    dim_surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
    dim_surface.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(dim_surface, (0, 0))
    
    font = pygame.font.Font(None, 74)
    text_surface = font.render(winner_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2))
    screen.blit(text_surface, text_rect)

##### MAIN LOOP #####

# To run the window, use the loop
while running:
    # pygame.QUIT event means the user clicked X to close the window.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()
            continue
            
        
        #### SELECTION SCREEN ####
        if not game_started:
            pvprect, pvairect, pvp_minimax_rect = board.draw_selection_screen(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvprect.collidepoint(event.pos):
                    game_started = True
                    vs_ai = False
                elif pvairect.collidepoint(event.pos):
                    game_started = True
                    vs_ai = True
                    ai_level = 0
                    ai = AI(game, ai_level)
                elif pvp_minimax_rect.collidepoint(event.pos):
                    game_started = True
                    vs_ai = True
                    ai_level = 1
                    ai = AI(game, ai_level)
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

                # Vs Player
                game_state = game.handle_move(clicked_row, clicked_col)
                if game_state != "continue":
                    game_over = True
                    if game_state == "draw":
                        print("It's a draw")
                        winner_text = "It's a draw"
                    else:
                        print(f"Player {game_state.split('_')[1]} wins!")
                        winner_text = f"Player {game_state.split('_')[1]} wins!"


                # Vs AI
                if not game_over and vs_ai and game.current_player == 2 and game.gamemode == 'ai':
                    pygame.display.update()
                    #game_state = game.handle_ai_move(ai)
                    ai_move = ai.eval(game)
                    if ai_move:
                        row, col = ai_move
                        game_state = game.handle_move(row, col)
                        if game_state != "continue":
                            game_over = True
                            if game_state == "draw":
                                print("Draw")
                                winner_text = "It's a draw"
                            elif game_state == "player_win":
                                print("Wind")
                                winner_text = f"AI ({['Random', 'Minimax'][ai_level]}) wins!"
                    #if game_state != "continue":
                        #game_over = True
                        #if game_state != "continue":
                            #game_over = True
                            #if game_state == "ai_win":
                                #print(f"AI ({['Random', 'Minimax'][ai_level]}) wins!")
                            #elif game_state == "draw":
                                #print("It's a draw")
                            #elif game_state == "no_moves":
                                #print("No more moves")
                                

                # if game_over:
                    # if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        # game.restart()
                        # board.restart(screen)
                        # game_over = False

        if game_started:
            screen.fill(constants.BACKGROUND_COLOR)
            board.draw(screen)
            board.draw_figures(screen)
            if game_over:
                board.draw_win_line(screen)
                draw_dimmed_board(screen, board, winner_text)
                board.display_restart_message(screen)
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()