import pygame, sys
from grid import Grid
from blocks import *

DARK_BLUE = (44, 44, 127)


screen = pygame.display.set_mode((300, 600))
clock = pygame.Clock()

game_grid = Grid()
game_grid.print_grid()

block = LBlock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Draw
    screen.fill(DARK_BLUE)
    game_grid.draw(screen)
    block.draw(screen)

    pygame.display.update()
    clock.tick(60)
