import pygame

# Initialize Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Load player sprite
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (50, 50))

class Player:
    def __init__(self, x, y):
        self.image = player_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = 5
        self.jump_power = -15
        self.gravity = 1
        self.y_velocity = 0
        self.grounded = False

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_SPACE] and self.grounded:
            self.jump()

    def jump(self):
        self.y_velocity = self.jump_power
        self.grounded = False

    def apply_gravity(self, platforms):
        """Applies gravity and checks for collisions with platforms."""
        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity
        self.grounded = False

        for platform in platforms:  # Ensure platforms is a list!
            if self.rect.colliderect(platform.rect) and self.y_velocity > 0:
                self.rect.bottom = platform.rect.top
                self.y_velocity = 0
                self.grounded = True

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Platform:
    """Class to define platforms."""
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)

def lvl1():
    player = Player(100, 500)  # Create player

    # Ensure platforms is a **list of Platform objects**
    platforms = [
        Platform(0, 550, 800, 50),  # Ground
        Platform(200, 450, 100, 20),
        Platform(400, 350, 150, 20),
        Platform(600, 250, 100, 20)
    ]

    running = True
    while running:
        screen.fill((255, 255, 255))  # White background
        keys = pygame.key.get_pressed()

        player.move(keys)
        player.apply_gravity(platforms)  # ✅ Pass the correct platforms list
        player.draw(screen)

        for platform in platforms:
            platform.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

lvl1()
