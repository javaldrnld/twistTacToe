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
        print("Drawing figures. Game state:")
        print(self.game.board)
        for row in range(constants.BOARD_ROWS):
            for col in range(constants.BOARD_COLUMNS):
                print(f"Drawing circle at {row}, {col}")
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
                    print(f"Drawing X at {row}, {col}")
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
                    # start_x = col * self.cell_size + 200
                    # start_y = row * self.cell_size + 200
                    # end_x = (col + 1) * self.cell_size - 200
                    # end_y = (row + 1) * self.cell_size - 200
                    # pygame.draw.line(screen, constants.CROSS_COLOR, (start_x, start_y), (end_x, end_y), constants.CROSS_WIDTH)
                    # pygame.draw.line(screen, constants.CROSS_COLOR, (start_x, end_y), (end_x, start_y), constants.CROSS_WIDTH)
    
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
        player = 1 if self.game.check_win(1) else 2
        
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