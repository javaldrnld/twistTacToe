import random
from . import game
from typing import Optional
import copy
import numpy as np

class AI:
    def __init__(self, game, level: Optional[int] = 1, player: Optional[int] = 2) -> None:
        self.game = game
        self.level = level
        self.player = player
        self.opponent = 1 if player == 2 else 2

    # Random Function move
    def random_choice(self, game):
        empty_cells = game.get_empty_squares()
        if empty_cells:
            move = random.choice(empty_cells)
            print(f"Random choice selected: {move}")  # Add this line
            return move
        print("No empty cells available")  
        return None

    def minimax(self, game, depth: int, alpha: float, beta: float, maximizing_player: bool):
        # Terminal Case
        case = game.final_state()

        if case == self.player:
            return 10 - depth, None
        elif case == self.opponent:
            return depth - 10, None
        elif game.is_board_full():
            return 0, None

        ### ALGORITHM
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None

            for (row, col) in game.get_empty_squares():
                game_copy = copy.deepcopy(game)
                game_copy.mark_move(row, col, self.player)
                eval, _ = self.minimax(game_copy, depth + 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        else: # AI CODE
            min_eval = float('inf')
            best_move = None

            for (row, col) in game.get_empty_squares():
                game_copy = copy.deepcopy(game)
                game_copy.mark_move(row, col, self.opponent)
                eval, _ = self.minimax(game_copy, depth + 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def eval(self, game):
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
    