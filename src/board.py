from . import constants

import pygame

#__all__ = [Board]
# I use class to maintain my code in an organize way and to find the bug easily.
class Board:
    
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.cell_size = min(width, height) // 3 # To ensure all the cell size is same
        #self.grid =

    def draw(self, screen) -> None:

        # Start 1 since we will multiply by cell_size
        for i in range(1, 3): 
            # calculate the horizontal line
            # Start Position for a 600x600 board is (0, 200) -> (600, 200)
            pygame.draw.line(screen, constants.BORDER_LINE, (0, i * self.cell_size), (self.width, i * self.cell_size))
            
            # Calculate vertical line
            # Start Position (200, 0) -> (200, 600)
            pygame.draw.line(screen, constants.BORDER_LINE, (self.cell_size * i, 0), (self.cell_size * i, self.width))
            