import numpy as np
from . import constants

class Game:
    def __init__(self) -> None:
        self.board = np.zeros((constants.BOARD_ROWS, constants.BOARD_COLUMNS))
        # [[" " for _ in range(3)] for _ in range(3)]

    # Game function
    def insert_move(self, row: int, column: int, player: int) -> None:
        """Mark a square on the board with the player move, it can be string but need to tweak the np and change to ordinary list"""
        self.board[row][column] = player

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
        self.board[row][column] = player