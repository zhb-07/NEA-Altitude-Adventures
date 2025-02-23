import pygame

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 50  # Size of each tile (square)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load tile images
grass_img = pygame.image.load("grass.png")
wall_img = pygame.image.load("stone.png")

# Scale images to fit tile size
grass_img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))

# Define the tilemap (0 = Grass, 1 = Wall)
tilemap = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Function to draw the tilemap
def draw_tilemap():
    for row_index, row in enumerate(tilemap):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if tile == 0:
                screen.blit(grass_img, (x, y))  # Draw grass
            elif tile == 1:
                screen.blit(wall_img, (x, y))  # Draw wall

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen

    draw_tilemap()  # Draw the tilemap

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
