"""
Module for managing the game board in a Tic-Tac-Toe game using Pygame.

This module contains the Board class which handles drawing the game board,
game pieces, and various UI elements.
"""
from . import constants
import pygame

class Board:
    """
    Represents the game board and handles its visual representation.

    Attributes:
        width (int): Width of the game window.
        height (int): Height of the game window.
        cell_size (int): Size of each cell in the game grid.
        game: Reference to the main game object.
        font (pygame.font.Font): Font for regular text.
        large_font (pygame.font.Font): Font for large text.
    """

    def __init__(self, width, height, game) -> None:
        """
        Initialize the Board object.

        Args:
            width (int): Width of the game window.
            height (int): Height of the game window.
            game: Reference to the main game object.
        """
        self.width = width
        self.height = height
        self.cell_size = min(width, height) // 3  # To ensure all the cell size is same
        self.game = game

        pygame.font.init()
        self.font = pygame.font.SysFont("comincsans", 36)
        self.large_font = pygame.font.Font(None, 72)

    def draw(self, screen) -> None:
        """Draw the game grid on the screen."""
        # Start 1 since we will multiply by cell_size
        for i in range(1, 3):
            # calculate the horizontal line
            # Start Position for a 600x600 board is (0, 200) -> (600, 200)
            pygame.draw.line(
                screen,
                constants.BORDER_LINE,
                (0, i * self.cell_size),
                (self.width, i * self.cell_size),
            )

            # Calculate vertical line
            # Start Position (200, 0) -> (200, 600)
            pygame.draw.line(
                screen,
                constants.BORDER_LINE,
                (self.cell_size * i, 0),
                (self.cell_size * i, self.height),
            )

    def draw_figures(self, screen) -> None:
        """Draw the game pieces (X and 0) on the screen."""
        for row in range(constants.BOARD_ROWS):
            for col in range(constants.BOARD_COLUMNS):
                center_x = int(col * self.cell_size + self.cell_size // 2)
                center_y = int(row * self.cell_size + self.cell_size // 2)
                if self.game.board[row][col] == 1:
                    self._draw_circle(screen, center_x, center_y)
                elif self.game.board[row][col] == 2:
                    self._draw_cross(screen, center_x, center_y)

    def _draw_circle(self, screen, center_x: int, center_y: int) -> None:
        """Draw a circle (O) at the specified position."""
        pygame.draw.circle(
            screen,
            constants.CIRCLE_COLOR,
            (center_x, center_y),
            self.cell_size // 3,
            constants.CIRCLE_WIDTH,
        )

    def _draw_cross(self, screen, center_x: int, center_y: int) -> None:
        """Draw a cross (X) at the specified position."""
        offset = self.cell_size // 4
        pygame.draw.line(
            screen,
            constants.CROSS_COLOR,
            (center_x - offset, center_y - offset),
            (center_x + offset, center_y + offset),
            constants.CROSS_WIDTH,
        )
        pygame.draw.line(
            screen,
            constants.CROSS_COLOR,
            (center_x - offset, center_y + offset),
            (center_x + offset, center_y - offset),
            constants.CROSS_WIDTH,
        )
    
    def draw_win_line(self, screen) -> None:
        """Draw the winning line on the screen."""
        state = self.game.final_state()
        if state == 0:
            return
        
        player = state
        for col in range(constants.BOARD_COLUMNS):
            if all(self.game.board[row][col] == player for row in range(constants.BOARD_ROWS)):
                self._draw_vertical_win(screen, col, player)
                return
            
        for row in range(constants.BOARD_ROWS):
            if all(self.game.board[row][col] == player for col in range(constants.BOARD_COLUMNS)):
                self._draw_horizontal_win(screen, row, player)
                return
            
        if all(self.game.board[i][i] == player for i in range(3)):
            # Since nag flip yung y-axis, we need to flip the diagonal
            self._draw_diagonal_win_dsc(screen, player)
            return
        
        if all(self.game.board[i][2-i] == player for i in range(3)):
            # Same dito, since nag flip yung y-axis, we need to flip the diagonal
            self._draw_diagonal_win_asc(screen, player)
            return

    def _draw_vertical_win(self, screen, col: int, player: int) -> None:
        """Draw a vertical winning line on the screen."""
        pos_x = col * self.cell_size + self.cell_size // 2
        color = self._get_player_color(player)
        pygame.draw.line(screen, color, (pos_x, 10), (pos_x, self.height - 10), 15)

    def _draw_horizontal_win(self, screen, row: int, player: int) -> None:
        """Draw a horizontal winning line."""
        pos_y = row * self.cell_size + self.cell_size // 2
        color = self._get_player_color(player)
        pygame.draw.line(screen, color, (10, pos_y), (self.width - 10, pos_y), 15)
    
    def _draw_diagonal_win_asc(self, screen, player: int) -> None:
        """Draw an ascending diagonal winning line."""
        color = self._get_player_color(player)
        pygame.draw.line(screen, color, (10, self.height - 10), (self.width - 10, 10), 15)

    def _draw_diagonal_win_dsc(self, screen, player: int) -> None:
        """Draw a descending diagonal winning line."""
        color = self._get_player_color(player)
        pygame.draw.line(screen, color, (10, 10), (self.width - 10, self.height - 10), 15)

    @staticmethod
    def _get_player_color(player: int):
        """Get the color for the specified player."""
        return constants.CIRCLE_COLOR if player == 1 else constants.CROSS_COLOR

    # def display_restart_message(self, screen) -> None:
        # """Display the restart message on the screen."""
        # text = self.font.render("Press R to restart", True, constants.BORDER_LINE)
        # screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))

    def restart(self, screen) -> None:
        """Restart the game and clear the screen."""
        self.game.restart()
        screen.fill(constants.BACKGROUND_COLOR)
        self.draw(screen)
        pygame.display.update()

    def draw_selection_screen(self, screen):
        """Draw the game mode selection screen."""
        screen.fill(constants.BACKGROUND_COLOR)
        font = pygame.font.Font(None, 36)

        options = [
            "1. Player vs Player",
            "2. Player vs AI (Random)",
            "3. Player vs AI (Minimax)"
        ]

        option_rects = []
        for i, option in enumerate(options):
            text = font.render(option, True, constants.BORDER_LINE)
            rect = text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + i * 100 - 50))
            screen.blit(text, rect)
            option_rects.append(rect)

        return option_rects

    def draw_winner_announcement(self, screen, winner):
        """Draw the winner announcement on the screen."""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        screen.blit(overlay, (0, 0))

        text = "It's a Draw!" if winner == "draw" else f"Player {winner} Wins!"
        text_surface = self.large_font.render(text, True, constants.WINNER_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(text_surface, text_rect)

        restart_text = self.font.render("Press R to restart", True, constants.BORDER_LINE)
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        screen.blit(restart_text, restart_rect)

    def draw_turn_indicator(self, screen, current_player_symbol):
        """Draw the current player's turn indicator."""
        turn_text = f" Turn: {current_player_symbol}"
        text_surface = self.font.render(turn_text, True, constants.BORDER_LINE)
        text_rect = text_surface.get_rect(center=(self.width // 2, 50))
        screen.blit(text_surface, text_rect)

    