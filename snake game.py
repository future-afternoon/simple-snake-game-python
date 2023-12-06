
import pygame
import sys
import random
global SNAKE_SPEED

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
SNAKE_SIZE = 20
SNAKE_SPEED = 15  # Initial snake speed
SNAKE_ACCELERATION = 1  # Increase in speed after each point

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = RED

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        current = self.get_head_position()
        x, y = self.direction
        new = (((current[0] + (x * GRID_SIZE)) % WIDTH), (current[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], SNAKE_SIZE, SNAKE_SIZE))


# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = WHITE
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], SNAKE_SIZE, SNAKE_SIZE))


# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Main function
def main():
    global SNAKE_SPEED  # Add this line to declare SNAKE_SPEED as a global variable
    # Initialize game
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    font = pygame.font.SysFont(None, 36)
    score = 0
    highest_score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    snake.direction = RIGHT

        snake.update()
        if snake.get_head_position() == food.position:
            score += 1
            snake.length += 1
            if score > highest_score:
                highest_score = score
            SNAKE_SPEED += SNAKE_ACCELERATION
            food.randomize_position()

        surface.fill(BLACK)
        snake.render(surface)
        food.render(surface)

        # Draw dashboard
        score_text = font.render(f"Score: {score}", True, WHITE)
        highest_score_text = font.render(f"Highest Score: {highest_score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        surface.blit(highest_score_text, (10, 40))

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()
