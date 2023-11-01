import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
GRID_SIZE = 25
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

SHAPES_COLORS = [(0, 255, 255), (255, 255, 0), (128, 0, 128),
                 (255, 165, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0)]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Create grid
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Initialize variables
clock = pygame.time.Clock()
current_tetromino = None
current_tetromino_shape = None
current_tetromino_color = None
current_x = GRID_WIDTH // 2
current_y = 0
score = 0


def game_over_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, (255, 0, 0))  # Red "Game Over" text
    restart_text = font.render("Press 'R' to restart or 'Q' to quit", True,
                               (255, 255, 255))  # White restart/quit instructions
    screen.blit(game_over_text,
                (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height()))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    pygame.display.update()


# Function to rotate a tetromino clockwise
def rotate_tetromino(tetromino):
    # Transpose the tetromino
    rotated = [[tetromino[j][i] for j in range(len(tetromino))] for i in range(len(tetromino[0]))]
    # Reverse each row to get the clockwise rotation
    rotated = [row[::-1] for row in rotated]
    return rotated


# Functions
def draw_grid():
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen, SHAPES_COLORS[cell - 1], pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
            pygame.draw.rect(
                screen, WHITE, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)


def new_tetromino():
    global current_tetromino, current_tetromino_shape, current_tetromino_color, current_x, current_y

    current_x = GRID_WIDTH // 2
    current_y = 0

    shape = random.choice(SHAPES)
    color = random.randint(1, len(SHAPES_COLORS))

    current_tetromino_shape = shape
    current_tetromino_color = color
    current_tetromino = []

    for y, row in enumerate(shape):
        new_row = []
        for x, cell in enumerate(row):
            if cell:
                new_row.append(color)
            else:
                new_row.append(0)
        current_tetromino.append(new_row)

    if check_collision(current_tetromino, current_x, current_y):
        game_over()


def check_collision(tetromino, x, y):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col]:
                if (
                        x + col < 0
                        or x + col >= GRID_WIDTH
                        or y + row >= GRID_HEIGHT
                        or grid[y + row][x + col] != 0
                ):
                    return True
    return False


def merge_tetromino():
    global current_x, current_y, current_tetromino

    for row in range(len(current_tetromino)):
        for col in range(len(current_tetromino[row])):
            if current_tetromino[row][col]:
                grid[current_y + row][current_x + col] = current_tetromino_color

    remove_lines()

    new_tetromino()


def remove_lines():
    global grid, score
    lines_to_remove = []
    for row in range(len(grid)):
        if all(grid[row]):
            lines_to_remove.append(row)
    for row in lines_to_remove:
        del grid[row]
        grid.insert(0, [0] * GRID_WIDTH)
        score += 100


def game_over():
    global grid, score
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    score = 0


def draw_tetromino(tetromino, x, y, color):
    neon_glow_color = (0, 255, 255)  # Neon glow color (bright cyan)

    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col]:
                # Draw the neon glow effect with a slight shift and larger size
                pygame.draw.rect(
                    screen, neon_glow_color,
                    pygame.Rect((x + col) * GRID_SIZE - 3, (y + row) * GRID_SIZE - 3, GRID_SIZE + 6, GRID_SIZE + 6)
                )
                # Draw the actual piece
                pygame.draw.rect(
                    screen, color,
                    pygame.Rect((x + col) * GRID_SIZE, (y + row) * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                )


def draw_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))


# Game loop
new_tetromino()
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not check_collision(current_tetromino, current_x - 1, current_y):
                current_x -= 1
            if event.key == pygame.K_RIGHT and not check_collision(current_tetromino, current_x + 1, current_y):
                current_x += 1
            if event.key == pygame.K_DOWN and not check_collision(current_tetromino, current_x, current_y + 1):
                current_y += 1
            if event.key == pygame.K_SPACE:
                while not check_collision(current_tetromino, current_x, current_y + 1):
                    current_y += 1
            if event.key == pygame.K_UP:  # Rotate the tetromino clockwise
                rotated_tetromino = rotate_tetromino(current_tetromino)
                if not check_collision(rotated_tetromino, current_x, current_y):
                    current_tetromino = rotated_tetromino

    if not check_collision(current_tetromino, current_x, current_y + 1):
        current_y += 1
    else:
        merge_tetromino()

    draw_grid()
    draw_tetromino(current_tetromino, current_x, current_y, SHAPES_COLORS[current_tetromino_color - 1])
    draw_score()

    pygame.display.update()
    clock.tick(5)

pygame.quit()
