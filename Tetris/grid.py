import pygame
from colors import Colors


class Grid:
    def __init__(self):
        self.nr_of_rows = 20
        self.nr_of_columns = 10
        self.cell_size = 30
        self.grid = [
            [0 for j in range(self.nr_of_columns)] for i in range(self.nr_of_rows)
        ]  # umple lista cu zero-uri
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.nr_of_rows):
            for column in range(self.nr_of_columns):
                print(self.grid[row][column], end=" ")
            print()

    def draw(self, screen):
        for row in range(self.nr_of_rows):
            for column in range(self.nr_of_columns):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(
                    column * self.cell_size + 1,
                    row * self.cell_size + 1,
                    self.cell_size - 1,
                    self.cell_size - 1,
                )
                pygame.draw.rect(
                    screen,
                    self.colors[cell_value],
                    cell_rect
                )
