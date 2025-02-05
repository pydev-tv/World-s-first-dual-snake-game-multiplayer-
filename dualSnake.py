import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20


# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_GRAY = (30, 30, 30)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Player Snake Game")
clock = pygame.time.Clock()

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake Class
class Snake:
    def __init__(self, start_pos, start_direction, color):
        self.body = [start_pos]
        self.direction = start_direction
        self.growing = False
        self.color = color

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Wrap around screen
        new_head = (new_head[0] % (WIDTH // CELL_SIZE), new_head[1] % (HEIGHT // CELL_SIZE))

        if new_head in self.body:
            return False  # Game over condition

        self.body.insert(0, new_head)
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False
        return True

    def grow(self):
        self.growing = True

    def change_direction(self, new_direction):
        if (self.direction[0] + new_direction[0], self.direction[1] + new_direction[1]) != (0, 0):
            self.direction = new_direction

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            if i == 0:  # Head
                pygame.draw.circle(screen, self.color, (segment[0] * CELL_SIZE + CELL_SIZE // 2, segment[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
                pygame.draw.circle(screen, WHITE, (segment[0] * CELL_SIZE + CELL_SIZE // 3, segment[1] * CELL_SIZE + CELL_SIZE // 3), 3)
                pygame.draw.circle(screen, WHITE, (segment[0] * CELL_SIZE + 2 * CELL_SIZE // 3, segment[1] * CELL_SIZE + CELL_SIZE // 3), 3)
            else:  # Body
                pygame.draw.rect(screen, self.color, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Food Class
class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.position = (random.randint(0, WIDTH // CELL_SIZE - 1), random.randint(0, HEIGHT // CELL_SIZE - 1))

# Draw Grid
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (0, y), (WIDTH, y))

# Draw Score
def draw_score(score1, score2):
    font = pygame.font.SysFont('Segoe UI', 36)
    score_text1 = font.render(f"Score: {score1}", True, GREEN)
    screen.blit(score_text1, (10, 10))
    score_text2 = font.render(f"Score: {score2}", True, BLUE)
    screen.blit(score_text2, (WIDTH - score_text2.get_width() - 10, 10))

# Game Over
def game_over():
    font = pygame.font.SysFont('Segoe UI', 60)
    text = font.render("GAME OVER", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
    pygame.display.flip()
    pygame.time.delay(3000)  # Show "Game Over" for 3 seconds

# Game Loop
def game_loop(level):
    if level == 1:
        FPS = 8  # Easy
    elif level == 2:
        FPS = 12  # Medium
    else:
        FPS = 16  # Hard

    snake1 = Snake((5, 5), RIGHT, GREEN)  # Snake 1 (WASD)
    snake2 = Snake((15, 5), RIGHT, BLUE)  # Snake 2 (Arrow keys)
    food = Food()
    score1 = 0
    score2 = 0
    running = True

    while running:
        screen.fill(BLACK)
        draw_grid()

        # Draw score labels
        draw_score(score1, score2)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snake1.change_direction(UP)
                elif event.key == pygame.K_s:
                    snake1.change_direction(DOWN)
                elif event.key == pygame.K_a:
                    snake1.change_direction(LEFT)
                elif event.key == pygame.K_d:
                    snake1.change_direction(RIGHT)
                elif event.key == pygame.K_UP:
                    snake2.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake2.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake2.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake2.change_direction(RIGHT)

        # Snake movements
        if not snake1.move():
            game_over()  # Snake 1 dies
            return  # End the game and return to the menu
        if not snake2.move():
            game_over()  # Snake 2 dies
            return  # End the game and return to the menu

        # Check if either snake eats the food
        if snake1.body[0] == food.position:
            snake1.grow()
            food.respawn()
            score1 += 1  # Snake 1 scores
        if snake2.body[0] == food.position:
            snake2.grow()
            food.respawn()
            score2 += 1  # Snake 2 scores

        # Check if the two snakes collide with each other
        if snake1.body[0] in snake2.body or snake2.body[0] in snake1.body:
            game_over()  # Game over if snakes collide with each other
            return  # End the game and return to the menu

        # Draw both snakes
        snake1.draw(screen)
        snake2.draw(screen)

        # Draw the food
        pygame.draw.circle(screen, RED, (food.position[0] * CELL_SIZE + CELL_SIZE // 2, food.position[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Display Initial Label
def display_label():
    screen.fill(BLACK)
    font = pygame.font.SysFont('Segoe UI', 60)
    text = font.render("Snake Mania by Ahsan Nasir", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))

    pygame.display.flip()
    pygame.time.delay(3000)  # Show the label for 3 seconds

# Draw Level Selection
def draw_level_selection():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    text = font.render("Choose a Level", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

    easy_text = font.render("1. Easy", True, WHITE)
    medium_text = font.render("2. Medium", True, WHITE)
    hard_text = font.render("3. Hard", True, WHITE)
    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2))
    screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2 + 60))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 120))

    pygame.display.flip()
    waiting = True
    level = 1
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = 1  # Easy
                    waiting = False
                elif event.key == pygame.K_2:
                    level = 2  # Medium
                    waiting = False
                elif event.key == pygame.K_3:
                    level = 3  # Hard
                    waiting = False
    return level

if __name__ == "__main__":
    display_label()
    level = draw_level_selection()  # Get player choice of level
    game_loop(level)  # Start the game
