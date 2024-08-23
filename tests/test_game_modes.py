import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import time
import random
from src.board import Board
from src import constants
from src.game import Game
from src.ai import AI

def simulate_click(x, y):
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (x, y), 'button': 1}))
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (x, y), 'button': 1}))

def simulate_key_press(key):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': key}))
    pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': key}))

def test_game_mode(mode):
    pygame.init()
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    clock = pygame.time.Clock()

    game = Game(ai_first=True)
    board = Board(constants.WIDTH, constants.HEIGHT, game)
    ai = AI(game)

    running = True
    game_over = False
    game_started = False
    vs_ai = False

    ai_level = 0

    # Start the game
    time.sleep(1)
    if mode == "pvp":
        simulate_click(constants.WIDTH // 2, constants.HEIGHT // 2 - 50)
    elif mode == "ai_random":
        simulate_click(constants.WIDTH // 2, constants.HEIGHT // 2 + 50)
        ai_level = 0
        vs_ai = True
    elif mode == "ai_minimax":
        simulate_click(constants.WIDTH // 2, constants.HEIGHT // 2 + 150)
        ai_level = 1
        vs_ai = True

    game_started = True

    # Play the game
    moves = 0
    while running and moves < 9:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            x = col * board.cell_size + board.cell_size // 2
            y = row * board.cell_size + board.cell_size // 2
            simulate_click(x, y)

            game_state = game.handle_move(row, col)
            if game_state != "continue":
                game_over = True
                print(f"Game over: {game_state}")
                break

            moves += 1

            if vs_ai and game.current_player == 2 and game.gamemode == 'ai':
                ai_move = ai.eval(game)
                if ai_move:
                    row, col = ai_move
                    game_state = game.handle_move(row, col)
                    if game_state != "continue":
                        game_over = True
                        print(f"Game over: {game_state}")
                        break
                    moves += 1

        screen.fill(constants.BACKGROUND_COLOR)
        board.draw(screen)
        board.draw_figures(screen)
        if game_over:
            board.draw_win_line(screen)
            #board.display_restart_message(screen)

        pygame.display.update()
        clock.tick(60)

    # End the game
    time.sleep(2)
    simulate_key_press(pygame.K_r)
    time.sleep(1)

    pygame.quit()

if __name__ == "__main__":
    print("Testing Player vs Player mode")
    test_game_mode("pvp")
    time.sleep(2)

    print("Testing Player vs AI (Random) mode")
    test_game_mode("ai_random")
    time.sleep(2)

    print("Testing Player vs AI (Minimax) mode")
    test_game_mode("ai_minimax")