import pygame
import random
import sys
# Initialize Pygame
pygame.init()
# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
    def get_head_position(self):
        return self.positions[0]
    def update(self):
        current = self.get_head_position()
        x, y = self.direction
        new = ((current[0] + x) % GRID_WIDTH, (current[1] + y) % GRID_HEIGHT)
        if new in self.positions[2:]:
            return False
        self.positions.insert(0, new)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True
    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1),
                        random.randint(0, GRID_HEIGHT - 1))
def main():
    snake = Snake()
    food = Food()
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
        # Update snake
        if not snake.update():
            snake.reset()
            food.randomize_position()
            score = 0
            continue
        # Check if snake ate food
        if snake.get_head_position() == food.position:
            snake.grow = True
            food.randomize_position()
            score += 1
        # Draw
        screen.fill(BLACK)
        # Draw snake
        for position in snake.positions:
            rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE,
                             GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(screen, GREEN, rect)
        # Draw food
        rect = pygame.Rect(food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE,
                          GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(screen, RED, rect)
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(10)  # Control game speed
if __name__ == '__main__':
    main()