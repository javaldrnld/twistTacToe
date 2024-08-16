from . import constants

import numpy as np
import pygame

class Game:
    def __init__(self) -> None:
        self.board = np.zeros((constants.BOARD_ROWS, constants.BOARD_COLUMNS))
        # [[" " for _ in range(3)] for _ in range(3)]
        self.empty_squares = self.board
        self.marked_squares = 0
        self.current_player = 1
        self.gamemode = 'ai' #ai

    # Game function

    def final_state(self):
        """
            @return 0 -> No win yet
            @return 1 -> Player 1 wins
            @return 2 -> Player 2 wins
        """
        if self.check_win(1):
            return 1
        
        if self.check_win(2):
            return 2
        
        if self.is_board_full():
            return 0
        
        return 0 # Subject to change 0 for both no win yet and draw

    # empty_sqr
    def space_is_available(self, row: int, column: int) -> bool:
        """Check if space is available"""
        return self.board[row][column] == 0

    # is_full
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
    
    # Mark_sqr
    def mark_move(self, row: int, column: int, player) -> None:
        # print(f"Marking move: Row {row}, Col {column}, Player {player}")
        self.board[row][column] = player
        self.marked_squares += 1
        # print("Updated board:")
        # print(self.board)

    # LEt's see kung same lang ba sila nung is_board_full or nope
    # def is_full(self) -> None:
        # return self.marked_squares == 9

    # is_empty
    def is_empty(self):
        return self.marked_squares == 0
    
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
    
    def reset(self):
        self.__init__()

    ##### vs player
    def handle_play_move(self, row, col):
        if self.space_is_available(row, col):
            self.mark_move(row, col, self.current_player)
            if self.check_win(self.current_player):
                print(f"Player {self.current_player} wins!")
                return "player_win" 
            elif self.is_board_full():
                print("It's a draw")
                return "draw"
            else:
                self.switch_player()
        return "continue"
    
    ### vs a    
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