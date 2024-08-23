"""Module for managing the game logic of a Tic-Tac-Toe game."""

from typing import Optional, List, Tuple
from . import constants
import numpy as np


class Game:
    """ Game Logic """

    def __init__(self, ai_first = True) -> None:
        """Instance of Game Logic

        Args:
            ai_first (bool, optional): AI First to Move. Defaults to True.
        """

        self.board = np.zeros((constants.BOARD_ROWS, constants.BOARD_COLUMNS))
        self.ai_first = ai_first
        self.current_player = 2 if ai_first else 1
        self.gamemode = 'ai' 
        self.empty_squares = self.board
        self.marked_squares = 0

    def reset(self):
        """ Reset the game every time it end"""
        self.board = np.zeros((constants.BOARD_ROWS, constants.BOARD_COLUMNS))
        self.marked_squares = 0
        self.ai_first = not self.ai_first
        self.current_player = 2 if self.ai_first else 1


    def final_state(self) -> Optional[int]:
        """
        Determine the final state of the game.

        Returns:


        Returns:
            Optional[int]: 0 for draw, 1 for player 1 win, 2 for player 2 win, None for ongoing match
        """
        for player in [1, 2]:
            if self._check_win(player):
                return player
        
        if self.is_board_full():
            return 0
        
        return None # On going match

    ##### vs player
    def handle_move(self, row: int, col: int) -> str:
        """Return if the last move played is winning move, draw move or ongoing
        match.

        Args:
            row (int): Row of array
            col (int): Column of array

        Returns:
            str: Text whether it is draw, win, or continue
        """
        if self._space_is_available(row, col):
            self._mark_move(row, col, self.current_player)
            state = self.final_state()
            if state is not None:  
                return "draw" if state == 0 else f"player_{state}_win"
            self._switch_player()
        return "continue"

    def _rotate_board(self) -> None:
        """ Rotate the board every turn"""
        self.board = np.rot90(self.board, k=1)

    def _space_is_available(self, row: int, column: int) -> bool:
        """Check if space is available"""
        return self.board[row][column] == 0

    def is_board_full(self) -> bool:
        """Use the count function to count if there's still 0"""
        return np.count_nonzero(self.board) == self.board.size
    
    def _mark_move(self, row: int, column: int, player: int) -> None:
        """Mark a move in a board

        Args:
            row (int): Row where the user want to place
            column (int): Column wher the user want to place
            player (int): Player 1 for user or 2 for AI/player 2
        """
        self.board[row][column] = player
        self.marked_squares += 1
        self._rotate_board()

    
    def get_empty_squares(self):
        """Get a list of empty squares in the board"""
        empty_sqrs = []
        for row in range(constants.BOARD_ROWS):
            for col in range(constants.BOARD_COLUMNS):
                if self._space_is_available(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def get_current_player_symbol(self):
        return 'O' if self.current_player == 1 else 'X'


    def _check_win(self, player: int) -> bool:
        """
        Check if the player has won the game.

        Args:
            player (int): Player to check for win (1 or 2)

        Returns:
            bool: True if the player has won the game, False otherwise
        """
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
    
    def restart(self) -> None:
        """Restart the game."""
        self.board = np.zeros((constants.BOARD_ROWS, constants.BOARD_COLUMNS))
        self.current_player = 1

    def _switch_player(self) -> None:
        """Switch the current player."""
        self.current_player = 3 - self.current_player

    def change_mode(self) -> None:
        """Toggle the game mode between player vs player and player vs AI."""
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def is_over(self) -> bool:
        """Check if the game is over."""
        return self.final_state(show=True) != 0 or self.is_board_full()
    
    ### vs ai
    def handle_ai_move(self, ai) -> str:
        """
        Handle an AI Move

        Args:
            ai: The AI object making the move.

        Returns:
            str: Game state after the AI move.
        """
        ai_move = ai.eval(self)
        if ai_move is not None:
            row, col = ai_move
            if self._space_is_available(row, col):
                self._mark_move(row, col, self.current_player) 
                if self._check_win(self.current_player):
                    return "ai_win"
                elif self.is_board_full():
                    return "draw"
                self._switch_player()
            return "continue"
        return "no_moves"