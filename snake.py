import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Font for score
font = pygame.font.SysFont("Arial", 24)

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

def game_over():
    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(2000)

def reset_game():
    return [(100, 100)], (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                         random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE), 0

def main():
    snake, food, score = reset_game()
    direction = (CELL_SIZE, 0)
    running = True
    game_over_flag = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        if not game_over_flag:
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

            # Check for wall collision
            if (new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT):
                game_over_flag = True
                continue

            # Check for self collision
            if new_head in snake:
                game_over_flag = True
                continue

            snake = [new_head] + snake

            # Check for food collision
            if abs(new_head[0] - food[0]) < CELL_SIZE and abs(new_head[1] - food[1]) < CELL_SIZE:
                score += 1
                food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                        random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
            else:
                snake.pop()

        screen.fill(BLACK)
        draw_score(score)
        draw_snake(snake)
        draw_food(food)

        if game_over_flag:
            game_over()
        else:
            pygame.display.flip()
            clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
