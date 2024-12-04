import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()
FPS = 30

# Grid and cell size
CELL_SIZE = 25
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Directions
DIRECTIONS = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}


class PacMan:
    def __init__(self):
        self.x = 1  # Initial x position in grid
        self.y = 1  # Initial y position in grid
        self.direction = "RIGHT"  # Initial direction
        self.size = CELL_SIZE - 5  # Pac-Man size

    def move(self, maze):
        dx, dy = DIRECTIONS[self.direction]
        new_x, new_y = self.x + dx, self.y + dy

        # Check for walls
        if maze[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self):
        pygame.draw.circle(
            screen,
            YELLOW,
            (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2),
            self.size // 2,
        )


class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice(list(DIRECTIONS.keys()))

    def move(self, maze):
        if random.randint(0, 10) > 8:  # Change direction occasionally
            self.direction = random.choice(list(DIRECTIONS.keys()))

        dx, dy = DIRECTIONS[self.direction]
        new_x, new_y = self.x + dx, self.y + dy

        # Check for walls
        if maze[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2),
            CELL_SIZE // 2,
        )


def create_maze():
    maze = [
        [1 if x == 0 or y == 0 or x == COLS - 1 or y == ROWS - 1 else 0 for x in range(COLS)]
        for y in range(ROWS)
    ]

    # Add some random walls
    for _ in range(50):
        x, y = random.randint(1, COLS - 2), random.randint(1, ROWS - 2)
        maze[y][x] = 1

    return maze


def draw_maze(maze):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:  # Wall
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )


def main():
    maze = create_maze()
    pacman = PacMan()
    ghosts = [Ghost(COLS - 2, ROWS - 2, RED), Ghost(2, ROWS - 2, WHITE)]
    pellets = [(x, y) for y in range(ROWS) for x in range(COLS) if maze[y][x] == 0]

    running = True
    score = 0

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.direction = "UP"
                elif event.key == pygame.K_DOWN:
                    pacman.direction = "DOWN"
                elif event.key == pygame.K_LEFT:
                    pacman.direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    pacman.direction = "RIGHT"

        # Move Pac-Man
        pacman.move(maze)

        # Check for pellet collection
        if (pacman.x, pacman.y) in pellets:
            pellets.remove((pacman.x, pacman.y))
            score += 1

        # Move ghosts
        for ghost in ghosts:
            ghost.move(maze)
            if ghost.x == pacman.x and ghost.y == pacman.y:
                running = False  # Game over

        # Draw everything
        draw_maze(maze)
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()

        # Draw pellets
        for pellet in pellets:
            pygame.draw.circle(
                screen,
                WHITE,
                (pellet[0] * CELL_SIZE + CELL_SIZE // 2, pellet[1] * CELL_SIZE + CELL_SIZE // 2),
                5,
            )

        # Draw score
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

main()
