import random
from . import game
from typing import Optional
import copy

class AI:
    def __init__(self, game, level: Optional[int] = 1, player: Optional[int] = 2) -> None:
        self.game = game
        self.level = level
        self.player = player

    # Random Function move
    def random_choice(self, game):
        empty_cells = game.get_empty_squares()
        if empty_cells:
            move = random.choice(empty_cells)
            print(f"Random choice selected: {move}")  # Add this line
            return move
        print("No empty cells available")  # Add this line
        return None

    def minimax(self, game, maximizing_player: bool):
        # Terminal Case
        case = game.final_state()

        # Player 1 case
        if case == 1:
            return 1, None
        
        # Player 2 case
        if case == 2:
            return -1, None # AI -> Minimize
        
        elif game.is_board_full():
            return 0, None
        

        ### ALGORITHM
        if maximizing_player:
            max_eval = float("-inf")
            best_move = None
            empty_cells = game.get_empty_squares()

            for (row, col) in empty_cells:
                game_copy = copy.deepcopy(game)
                game_copy.mark_move(row, col, self.player)
                eval = self.minimax(game_copy, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing_player: # AI CODE
            min_eval = float("inf")
            best_move = None
            empty_cells = game.get_empty_squares()

            for (row, col) in empty_cells:
                game_copy = copy.deepcopy(game)
                game_copy.mark_move(row, col, self.player)
                eval = self.minimax(game_copy, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


    def eval(self, game):
        if self.level == 0:
            # Random choice
            eval = 'random'
            move = self.random_choice(game)
        else:
            # minimax algo choice
            eval, move = self.minimax(game, False) # False: AI -> Minimize 
        print(f" AI Eval: {eval}, Move: {move}")
        return move
    