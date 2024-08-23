"""
AI module for playing a game of Tic Tac Toe.

This module contains the AI class which is responsible for making moves in the game 
using random selection or the minimax algorithm with alpha-beta pruning.

Classes:
    AI: A class to represent the AI player in the game.
"""


import random
import copy
import numpy as np

from typing import Optional, Tuple
from . import game


class AI:
    """
    AI Player for a game.

    This class implements an AI player that can make moves using either
    random selection or the minimax algorithm with alpha-beta pruning.

    Attributes:
        game: The game instance.
        level (int): The AI difficulty level (0 for random, 1+ for minimax).
        player (int): The player number for this AI (usually 2).
        opponent (int): The opponent's player number.
    """

    def __init__(self, game, level: Optional[int] = 1, player: Optional[int] = 2) -> None:
        """
        Initialize the AI player.

        Args:
            game: The game instance.
            level (int): The AI difficulty level (default is 1).
            player (int): The player number for this AI (default is 2).
        """
        self.game = game
        self.level = level
        self.player = player
        self.opponent = 1 if player == 2 else 2


    def random_choice(self, game) -> Optional[Tuple[int, int]]:
        """
        Make a random move on the game board.

        Args:
            game: The game instance.

        Returns:
            Optional[Tuple[int, int]]: A random empty cell, or None if no empty cells.
        """ 
        empty_cells = game.get_empty_squares()
        if empty_cells:
            move = random.choice(empty_cells)
            print(f"Random choice selected: {move}")  # Add this line
            return move
        print("No empty cells available")  
        return None

    def minimax(self, 
                game, 
                depth: int, 
                alpha: float, 
                beta: float, 
                maximizing_player: bool
    ) -> Tuple[int, Optional[Tuple[int, int]]]:
        """
        Implement the minimax algorithm with alpha-beta pruning.

        Args:
            game: The game instance.
            depth (int): The current depth in the game tree.
            alpha (float): The alpha value for pruning.
            beta (float): The beta value for pruning.
            maximizing_player (bool): True if maximizing, False if minimizing.

        Returns:
            Tuple[float, Optional[Tuple[int, int]]]: The evaluation value and the best move.
        """
        # Terminal Case
        case = game.final_state()

        if case == self.player:
            return 10 - depth, None
        elif case == self.opponent:
            return depth - 10, None
        elif game.is_board_full():
            return 0, None
        
        if maximizing_player:
            return self._maximize(game, depth, alpha, beta)
        else:
            return self._minimize(game, depth, alpha, beta)

    def _maximize(self, game, depth: int, alpha: float, beta: float) -> Tuple[int, Optional[Tuple[int, int]]]:
        """
        Handles the maximizing player's turn in the minimax algorithm.

        Args:
            game_copy (game.Game): A copy of the current game state.
            depth (int): The current depth in the game tree.
            alpha (float): The alpha value for alpha-beta pruning.
            beta (float): The beta value for alpha-beta pruning.

        Returns:
            Tuple[int, Optional[Tuple[int, int]]]: The best evaluation score and the best move as (row, col).
        """

        max_eval = float('-inf')
        best_move = None

        for row, col in game.get_empty_squares():
            game_copy = copy.deepcopy(game)
            game_copy._mark_move(row, col, self.player)
            eval, _ = self.minimax(game_copy, depth + 1, alpha, beta, False)

            if eval > max_eval:
                max_eval = eval
                best_move = (row, col)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return max_eval, best_move
    
    def _minimize(self, game, depth: int, alpha: float, beta: float) -> Tuple[int, Optional[Tuple[int, int]]]:
        """
        Handles the minimizing player's turn in the minimax algorithm.

        Args:
            game_copy (game.Game): A copy of the current game state.
            depth (int): The current depth in the game tree.
            alpha (float): The alpha value for alpha-beta pruning.
            beta (float): The beta value for alpha-beta pruning.

        Returns:
            Tuple[int, Optional[Tuple[int, int]]]: The best evaluation score and the best move as (row, col).
        """
                
        min_eval = float('inf')
        best_move = None

        for row, col in game.get_empty_squares():
            game_copy = copy.deepcopy(game)
            game_copy._mark_move(row, col, self.opponent)
            eval, _ = self.minimax(game_copy, depth + 1, alpha, beta, True)

            if eval < min_eval:
                min_eval = eval
                best_move = (row, col)
            beta = min(beta, eval)
            if beta <= alpha:
                break

        return min_eval, best_move

    def eval(self, game) -> Optional[Tuple[int, int]]:
        """
        Evaluate the game state and return the best move.

        Args:
            game: The game instance.

        Returns:
            Optional[Tuple[int, int]]: The best move as (row, col), or None if no move is possible.
        """ 
        if self.level == 0:
            # Random choice
            eval = "Random"
            print("Random choice selected")
            move = self.random_choice(game)
        else:
            # minimax algo choice
            print("Minimax choice selected")
            eval, move = self.minimax(game, 0, float('-inf'), float('inf'), False) # False: AI -> Minimize 
        print(f" AI Eval: {eval}, Move: {move}")
        return move
    