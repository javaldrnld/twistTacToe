from src.board import Board
from src import constants
from src.game import Game

import pygame
import sys


pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
screen.fill(constants.BACKGROUND_COLOR)
clock = pygame.time.Clock()

# Game Instance (logic)
game = Game()

# Board Instance
board = Board(constants.WIDTH, constants.HEIGHT)

# Add title
pygame.display.set_caption("Ultimate TIC-TAC-TOE")

# To run the window, use the loop
while True:
    # pygame.QUIT event means the user clicked X to close the window.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Render 
        board.draw(screen)
        pygame.display.update()