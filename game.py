import pygame

# Load images
player_image = pygame.image.load("images/player.png")
player_image = pygame.transform.scale(player_image, (50, 50))
player_image.set_colorkey((255,255,255))

grass_img = pygame.image.load("images/grass.png")
dirt_img = pygame.image.load("images/dirt.png")
stone_img = pygame.image.load("images/stone.png")
enemy_image = pygame.image.load("images/player.png")
sky_img = pygame.image.load("images/sky.png")
enemy_image = pygame.transform.scale(enemy_image, (32, 32))
enemy_image.set_colorkey((105,106,106))

TILE_SIZE = 32

# Tilemap
tilemap = [
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "x.........................................................x",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
]

# Function to create solid tiles (stone "x" blocks)
def get_solid_tiles():
    solid_tiles = []
    for row_index, row in enumerate(tilemap):
        for col_index, tile in enumerate(row):
            if tile == "x":  # Only make collision for stone blocks
                solid_tiles.append(pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    return solid_tiles

class Player:
    def __init__(self, x, y):
        self.image = player_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = 2
        self.jump_power = -8
        self.gravity = 1
        self.y_velocity = 0
        self.grounded = False



    # Your movement code here...

    def move(self, keys, solid_tiles):
        dx = 0
        dy = self.y_velocity

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.velocity
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.grounded:
            self.jump()

        # Apply gravity
        self.y_velocity += self.gravity
        self.y_velocity = min(self.y_velocity, 10)

        # Collision check (horizontal)
        self.rect.x += dx
        for tile in solid_tiles:
            if self.rect.colliderect(tile):
                if dx > 0:  # Moving right
                    self.rect.right = tile.left
                if dx < 0:  # Moving left
                    self.rect.left = tile.right

        # Collision check (vertical)
        self.rect.y += dy
        self.grounded = False
        for tile in solid_tiles:
            if self.rect.colliderect(tile):
                if dy > 0:  # Falling down
                    self.rect.bottom = tile.top
                    self.y_velocity = 0
                    self.grounded = True
                if dy < 0:  # Jumping up
                    self.rect.top = tile.bottom
                    self.y_velocity = 0

    def jump(self):
        self.y_velocity = self.jump_power

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height

    def update(self, player):
        self.offset_x = max(0, min(player.rect.x - self.width // 2, (len(tilemap[0]) * TILE_SIZE) - self.width))
        self.offset_y = max(0, min(player.rect.y - self.height // 2, (len(tilemap) * TILE_SIZE) - self.height))


# Draw tilemap
def draw_tilemap(screen, camera):
    start_col = camera.offset_x // TILE_SIZE
    end_col = (camera.offset_x + camera.width) // TILE_SIZE + 1
    start_row = camera.offset_y // TILE_SIZE
    end_row = (camera.offset_y + camera.height) // TILE_SIZE + 1

    for row_index in range(start_row, min(end_row, len(tilemap))):
        for col_index in range(start_col, min(end_col, len(tilemap[row_index]))):
            x = col_index * TILE_SIZE - camera.offset_x
            y = row_index * TILE_SIZE - camera.offset_y
            tile = tilemap[row_index][col_index]

            if tile == "x":
                screen.blit(stone_img, (x, y))
            elif tile == ".":
                screen.blit(sky_img, (x, y))

# Main Game Loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    player = Player(100, 100)
    camera = Camera(800, 600)
    solid_tiles = get_solid_tiles()

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.move(keys, solid_tiles)
        camera.update(player)

        draw_tilemap(screen, camera)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

