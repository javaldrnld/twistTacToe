from . import constants

import numpy as np
import pygame

class Game:
    def __init__(self) -> None:
        self.board = np.zeros((constants.BOARD_ROWS, constants.BOARD_COLUMNS))
        # [[" " for _ in range(3)] for _ in range(3)]
        

    # Game function
    # def insert_move(self, row: int, column: int, player: int) -> None:
        # """Mark a square on the board with the player move, it can be string but need to tweak the np and change to ordinary list"""
        # self.board[row][column] = player

    def space_is_available(self, row: int, column: int) -> bool:
        """Check if space is available"""
        return self.board[row][column] == 0

    def is_board_full(self) -> bool:
        """Use the count function to count if there's still 0"""
        return np.count_nonzero(self.board) == self.board.size
        # Eiter way we can use loop
        """
        for row in range(3):
            for column in range(3):
                if board[row][column] == 0:
                    return False
        return True
        """

    def mark_move(self, row: int, column: int, player) -> None:
        print(f"Marking move: Row {row}, Col {column}, Player {player}")
        self.board[row][column] = player
        print("Updated board:")
        print(self.board)

# TODO: FIX THE CHECKING ALGORITM MAKE IT EFFICIENT
    ## WInning Condition Check
    # def check_win(self, player: int):
        # # Vertical Check using loop
        # for col in range(constants.BOARD_COLUMNS):
            # if self.board[0][col] == player and self.board[1][col] == player and self.board[2][col] == player:
                # #self.game.draw_vertical_win(col, player)
                # return True
            
        # # Horizontal Check
        # for row in range(constants.BOARD_ROWS):
            # if self.board[row][0] == player and self.board[row][1] == player and self.board[row][2] == player:
                # #self.draw_horizontal_win(row, player)
                # return True

        # # Ascending Diagonal Win Check
        # if self.board[2][0] == player and self.board[1][1] == player and self.board[0][2] == player:
            # #self.draw_diagonal_win_asc(player)
            # return True
        
        # # Descending Diagonal Win Check
        # if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            # #self.draw_diagonal_win_dsc(player)
            # return True

        # return False
        # ANALYZE HOW ALGO WORK
    def check_win(self, player: int) -> bool:
        # Vertical Check
        for col in range(constants.BOARD_COLUMNS):
            if all(self.board[row][col] == player for row in range(constants.BOARD_ROWS)):
                return True
        
        # Horizontal Check
        for row in range(constants.BOARD_ROWS):
            if all(self.board[row][col] == player for col in range(constants.BOARD_COLUMNS)):
                return True
        
        # Diagonal Checks
        if all(self.board[i][i] == player for i in range(3)) or \
        all(self.board[i][2-i] == player for i in range(3)):
            return True
        
        return False
