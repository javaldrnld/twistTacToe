from . import constants
import pygame


# __all__ = [Board]
# I use class to maintain my code in an organize way and to find the bug easily.

class Board:
    def __init__(self, width, height, game) -> None:
        self.width = width
        self.height = height
        self.cell_size = min(width, height) // 3  # To ensure all the cell size is same
        # self.grid = [["" for _ in range(3)] for _ in range(3)]
        self.game = game
        pygame.font.init()
        self.font = pygame.font.SysFont("comincsans", 36)
        self.large_font = pygame.font.Font(None, 72)

    def draw(self, screen) -> None:
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

    # Move the function to the game class for purely game logic
    # def mark_square(self, row: int, column: int, player) -> None:
    # self.grid[row][column] = player
    def draw_figures(self, screen) -> None:
        rotation_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rotation_surface.fill((0, 0, 0, 0))  # Transparent background
        for row in range(constants.BOARD_ROWS):
            for col in range(constants.BOARD_COLUMNS):
                center_x = int(col * self.cell_size + self.cell_size // 2)
                center_y = int(row * self.cell_size + self.cell_size // 2)
                if self.game.board[row][col] == 1:
                    pygame.draw.circle(
                        screen,
                        constants.CIRCLE_COLOR,
                        (center_x, center_y),
                        self.cell_size // 3,
                        constants.CIRCLE_WIDTH,
                    )
                elif self.game.board[row][col] == 2:
                    # Draw X for player 2
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
                        constants.CROSS_WIDTH
                    )
    
    # TODO: READ ANALYZE
    # Drawing for checking
    def draw_vertical_win(self, screen, col: int, player: int) -> None:
        pos_x = col * self.cell_size + self.cell_size // 2
        color = constants.CIRCLE_COLOR if player == 1 else constants.CROSS_COLOR
        pygame.draw.line(screen, color, (pos_x, 10), (pos_x, self.height - 10), 15)

    def draw_horizontal_win(self, screen, row: int, player: int) -> None:
        pos_y = row * self.cell_size + self.cell_size // 2
        color = constants.CIRCLE_COLOR if player == 1 else constants.CROSS_COLOR
        pygame.draw.line(screen, color, (10, pos_y), (self.width - 10, pos_y), 15)
    
    def draw_diagonal_win_asc(self, screen, player: int) -> None:
        color = constants.CIRCLE_COLOR if player == 1 else constants.CROSS_COLOR
        pygame.draw.line(screen, color, (10, self.height - 10), (self.width - 10, 10), 15)

    def draw_diagonal_win_dsc(self, screen, player: int) -> None:
        color = constants.CIRCLE_COLOR if player == 1 else constants.CROSS_COLOR
        pygame.draw.line(screen, color, (10, 10), (self.width - 10, self.height - 10), 15)

    # Check for all win lien
    def draw_win_line(self, screen) -> None:
        state = self.game.final_state()
        if state == 0:
            return
        
        player = state
        color = constants.CIRCLE_COLOR if player == 1 else constants.CROSS_COLOR
        
        # Check vertical wins
        for col in range(constants.BOARD_COLUMNS):
            if all(self.game.board[row][col] == player for row in range(constants.BOARD_ROWS)):
                self.draw_vertical_win(screen, col, player)
                return

        # Check horizontal wins
        for row in range(constants.BOARD_ROWS):
            if all(self.game.board[row][col] == player for col in range(constants.BOARD_COLUMNS)):
                self.draw_horizontal_win(screen, row, player)
                return

        # Check diagonal wins
        if all(self.game.board[i][i] == player for i in range(3)):
            self.draw_diagonal_win_dsc(screen, player)
            return

        if all(self.game.board[i][2-i] == player for i in range(3)):
            self.draw_diagonal_win_asc(screen, player)
            return

    def display_restart_message(self, screen) -> None:
        text = self.font.render("Press R to restart", True, constants.BORDER_LINE)
        screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))

    def restart(self, screen) -> None:
        self.game.restart()
        screen.fill(constants.BACKGROUND_COLOR)
        self.draw(screen)
        pygame.display.update()

    def draw_selection_screen(self, screen) -> None:
        screen.fill(constants.BACKGROUND_COLOR)
        font = pygame.font.Font(None, 36)

        pvp_text = font.render("1. Player vs Player", True, constants.BORDER_LINE)
        pvai_text = font.render("2. Player vs AI (Random)", True, constants.BORDER_LINE)
        pvai_minimax_text = font.render("3. Player vs AI (Minimax)", True, constants.BORDER_LINE)

        pvp_rect = pvp_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 50))
        pvai_rect = pvai_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 50))
        pvai_minimax_rect = pvai_minimax_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 150))

        screen.blit(pvp_text, pvp_rect)
        screen.blit(pvai_text, pvai_rect)
        screen.blit(pvai_minimax_text, pvai_minimax_rect)

        return pvp_rect, pvai_rect, pvai_minimax_rect
    

    def draw_winner_announcement(self, screen, winner):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        screen.blit(overlay, (0, 0))

        # Prepare the winner text
        if winner == "draw":
            text = "It's a Draw!"
        else:
            text = f"Player {winner} Wins!"
        
        text_surface = self.large_font.render(text, True, constants.WINNER_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
        
        # Draw the winner text
        screen.blit(text_surface, text_rect)

        # Draw the restart message
        restart_text = self.font.render("Press R to restart", True, constants.BORDER_LINE)
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        screen.blit(restart_text, restart_rect)