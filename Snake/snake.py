import pygame, sys, random
from pygame.math import Vector2

pygame.init()

score_font = pygame.Font(None, 40)

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

# creare grid
cell_size = 25  # marime blocuri din grid
nr_of_cells = 30  # nr blocuri de pe axa x si de pe axa y

OFFSET = 75


class Food:
    def __init__(self, snake_body):
        self.pos = self.generate_random_pos(snake_body)  # positie mancare

    def draw(self):
        # definire positie si marime mancare
        food_rect = pygame.Rect(
            OFFSET + self.pos.x * cell_size,
            OFFSET + self.pos.y * cell_size,
            cell_size,
            cell_size,
        )
        pygame.draw.rect(screen, DARK_GREEN, food_rect, 0, 15)

    def generate_random_cell(self):
        x = random.randint(0, nr_of_cells - 1)
        y = random.randint(0, nr_of_cells - 1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        is_on_top_of_snake = False
        # asigura ca mancarea nu se genereaza pe sarpe
        while True:
            position = self.generate_random_cell()
            for segment in snake_body:
                if position == segment:
                    is_on_top_of_snake = True
            if is_on_top_of_snake == False:
                return position


class Snake:
    def __init__(self):
        # pozitie initiala sarpe, dimensiune 3 segmente
        self.body = [
            Vector2(6, 6),  # primul item din lista este capul sarpelui
            Vector2(5, 6),
            Vector2(4, 6),  # ultimul este coada
        ]
        self.direction = Vector2(1, 0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = pygame.Rect(
                OFFSET + segment.x * cell_size,
                OFFSET + segment.y * cell_size,
                cell_size,
                cell_size,
            )
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 2)

    # sarpele se misca prin adaugarea unui segment in fata capului si stergerea ultimului segment (coada)
    def update(self):
        # adauga segment nou in directia introdusa (capul sarpelui)
        self.body.insert(0, self.body[0] + self.direction)
        # daca snake nu a mancat, nu fa nimic
        if self.add_segment == True:
            self.add_segment = False
        else:
            # sterge ultimul segment din lista (coada sarpelui), pentru a-i pastra marimea constanta
            self.body = self.body[:-1]

    def reset(self):
        self.body = [
            Vector2(6, 6),
            Vector2(5, 6),
            Vector2(4, 6),
        ]
        self.direction = Vector2(1, 0)
        self.add_segment = False


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        self.highscore = 0

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_for_collision_with_food()
            self.check_for_collision_with_edges()
            self.check_for_collision_with_body()
            if self.score > self.highscore:
                self.highscore = self.score

    def check_for_collision_with_food(self):
        if self.snake.body[0] == self.food.pos:  # capul sarpelui atinge mancarea
            self.food.pos = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1  # incrementeaza scor

    def check_for_collision_with_body(self):
        headless_body = self.snake.body[1:]
        for segment in headless_body:
            if self.snake.body[0] == segment:
                self.game_over()

    def check_for_collision_with_edges(self):
        if self.snake.body[0].x == -1 or self.snake.body[0].x == nr_of_cells:
            self.game_over()
        if self.snake.body[0].y == -1 or self.snake.body[0].y == nr_of_cells:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.pos = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0


# game window
screen = pygame.display.set_mode(
    (cell_size * nr_of_cells + 2 * OFFSET, cell_size * nr_of_cells + 2 * OFFSET)
)

clock = pygame.time.Clock()
game = Game()

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

while True:
    # Event checking
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":  # pauza joc pana cand primeste input
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)

    # Drawing
    screen.fill(GREEN)  # background color
    pygame.draw.rect(
        screen,
        DARK_GREEN,
        (
            OFFSET - 5,
            OFFSET - 5,
            nr_of_cells * cell_size + 10,
            nr_of_cells * cell_size + 10,
        ),
        5,
    )
    game.draw()
    score_surface = score_font.render(str(game.score), True, DARK_GREEN)
    highscore_surface = score_font.render(
        "Highscore: " + str(game.highscore), True, DARK_GREEN
    )
    screen.blit(score_surface, (OFFSET - 5, OFFSET + cell_size * nr_of_cells + 10))
    screen.blit(
        highscore_surface,
        (
            OFFSET - 5 + cell_size * nr_of_cells - 160,
            OFFSET + cell_size * nr_of_cells + 10,
        ),
    )
    pygame.display.update()
    clock.tick(60)  # set fps
