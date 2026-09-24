"""
Snake Game
----------
An object-oriented implementation of the classic Snake game using pygame.
Features: collision detection, score tracking, and real-time gameplay.
"""

import random
import sys
import pygame

CELL_SIZE = 20
GRID_WIDTH = 24
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

BG_COLOR = (24, 24, 20)
GRID_COLOR = (40, 40, 34)
SNAKE_COLOR = (95, 158, 86)
SNAKE_HEAD_COLOR = (140, 191, 123)
FOOD_COLOR = (176, 94, 42)
TEXT_COLOR = (240, 235, 225)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    """Represents the player-controlled snake: position, movement, and growth."""

    def __init__(self, start_pos):
        self.body = [start_pos, (start_pos[0] - 1, start_pos[1]), (start_pos[0] - 2, start_pos[1])]
        self.direction = RIGHT
        self.grow_pending = False

    def set_direction(self, new_direction):
        # Prevent reversing directly into itself.
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if self.grow_pending:
            self.grow_pending = False
        else:
            self.body.pop()

    def grow(self):
        self.grow_pending = True

    def head(self):
        return self.body[0]

    def collides_with_self(self):
        return self.head() in self.body[1:]

    def collides_with_wall(self):
        x, y = self.head()
        return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT

    def occupies(self, cell):
        return cell in self.body

    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rect.inflate(-2, -2), border_radius=4)


class Food:
    """Represents the food the snake eats to grow and score points."""

    def __init__(self, snake):
        self.position = self._random_position(snake)

    def _random_position(self, snake):
        while True:
            cell = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if not snake.occupies(cell):
                return cell

    def respawn(self, snake):
        self.position = self._random_position(snake)

    def draw(self, surface):
        x, y = self.position
        center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(surface, FOOD_COLOR, center, CELL_SIZE // 2 - 2)


class Game:
    """Owns the game loop, scoring, and overall game state."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.reset()

    def reset(self):
        self.snake = Snake((GRID_WIDTH // 2, GRID_HEIGHT // 2))
        self.food = Food(self.snake)
        self.score = 0
        self.game_over = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.snake.set_direction(UP)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.snake.set_direction(DOWN)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.snake.set_direction(LEFT)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.snake.set_direction(RIGHT)
                elif event.key == pygame.K_r and self.game_over:
                    self.reset()

    def update(self):
        if self.game_over:
            return

        self.snake.move()

        if self.snake.collides_with_wall() or self.snake.collides_with_self():
            self.game_over = True
            return

        if self.snake.head() == self.food.position:
            self.snake.grow()
            self.food.respawn(self.snake)
            self.score += 1

    def draw(self):
        self.screen.fill(BG_COLOR)
        self._draw_grid()
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        self._draw_score()
        if self.game_over:
            self._draw_game_over()
        pygame.display.flip()

    def _draw_grid(self):
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    def _draw_score(self):
        text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(text, (8, 6))

    def _draw_game_over(self):
        message = self.font.render(
            f"Game over — score {self.score} — press R to restart", True, TEXT_COLOR
        )
        rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.draw.rect(self.screen, BG_COLOR, rect.inflate(20, 20))
        self.screen.blit(message, rect)

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
