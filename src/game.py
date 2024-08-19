########## IMPORT ##########  
from . import constants
import numpy as np
########## IMPORT ##########  


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
        """ Reset the game every time it end
        """
        self.board = np.zeros((constants.BOARD_ROWS, constants.BOARD_COLUMNS))
        self.marked_squares = 0
        self.ai_first = not self.ai_first
        self.current_player = 2 if self.ai_first else 1


    def final_state(self):
        """
            @return 0 -> No win yet
            @return 1 -> Player 1 wins
            @return 2 -> Player 2 wins
        """
        for player in [1, 2]:
            if self.check_win(player):
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
        if self.space_is_available(row, col):
            self.mark_move(row, col, self.current_player)
            state = self.final_state()
            if state is not None:  
                if state == 0:
                    return "draw"
                else:
                    return f"player_{state}_win"
            self.switch_player()
        return "continue"

    def rotate_board(self) -> None:
        """ Rotate the board every turn
        """
        self.board = np.rot90(self.board, k=1)

    def space_is_available(self, row: int, column: int) -> bool:
        """Check if space is available
        """
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
    
    def mark_move(self, row: int, column: int, player: int) -> None:
        """Mark a move in a board

        Args:
            row (int): Row where the user want to place
            column (int): Column wher the user want to place
            player (int): Player 1 for user or 2 for AI/player 2
        """
        self.board[row][column] = player
        self.marked_squares += 1
        self.rotate_board()

    # To be deleted is_empty
    # def is_empty(self):
        # return self.marked_squares == 0
    
    def get_empty_squares(self):
        empty_sqrs = []
        for row in range(constants.BOARD_ROWS):
            for col in range(constants.BOARD_COLUMNS):
                if self.space_is_available(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs


        # ANALYZE HOW ALGO WORK
        # all() -> Returns true if all element is true in given array
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
    
    def restart(self) -> None:
        self.board = np.zeros((constants.BOARD_ROWS, constants.BOARD_COLUMNS))
        self.current_player = 1

    def switch_player(self) -> None:
        self.current_player = 3 - self.current_player

    def change_mode(self) -> None:
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def is_over(self) -> bool:
        return self.final_state(show=True) != 0 or self.is_board_full()
    
    ### vs ai
    def handle_ai_move(self, ai):
        ai_move = ai.eval(self)
        if ai_move is not None:
            row, col = ai_move
            if self.space_is_available(row, col):
                self.mark_move(row, col, self.current_player) 
                if self.check_win(self.current_player):
                    return "ai_win"
                elif self.is_board_full():
                    return "draw"
                self.switch_player()
        else:
            return "no_moves"
        return "continue"