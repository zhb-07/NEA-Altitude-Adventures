import pygame
import random
import math
import main

player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (20, 20))
player_image.set_colorkey((163,73,164))
grass_img = pygame.image.load("grass.png")
wall_img = pygame.image.load("stone.png")
enemy_image = pygame.image.load("player.png")
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
enemy_image.set_colorkey((105,106,106))
TILE_SIZE = 20

tilemap = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def draw_tilemap():
    for row_index, row in enumerate(tilemap):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if tile == 0:
                main.screen.blit(grass_img, (x, y))  # Draw grass
            elif tile == 1:
                main.screen.blit(wall_img, (x, y))  # Draw wall

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
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.velocity
        if keys[pygame.K_SPACE] and self.grounded or keys[pygame.K_w] and self.grounded or keys[pygame.K_UP] and self.grounded:
            self.jump()

    def jump(self):
        self.y_velocity = self.jump_power
        self.grounded = False

    def apply_gravity(self, platforms):
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
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class Enemy:
    def __init__(self, x, y, health, speed):
        self.image = enemy_image
        self.x = x
        self.y = y
        self.health = health
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, 50, 50)  # Enemy hitbox

    @classmethod
    def spawn_random(cls, player_x, player_y):
        """Spawn enemy at a random position away from the player."""
        spawn_distance = 300  # Minimum distance from player
        screen_width, screen_height = 800, 600  # Adjust based on your game

        # Randomly choose spawn side (left, right, top, bottom)
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x = random.randint(0, screen_width // 2 - spawn_distance)
            y = random.randint(0, screen_height)
        elif side == "right":
            x = random.randint(screen_width // 2 + spawn_distance, screen_width)
            y = random.randint(0, screen_height)
        elif side == "top":
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height // 2 - spawn_distance)
        else:  # bottom
            x = random.randint(0, screen_width)
            y = random.randint(screen_height // 2 + spawn_distance, screen_height)

        return cls(x, y, health=100, damage=10, speed=random.randint(2, 5))

    def move_towards_player(self, player_x, player_y):
        """Move enemy towards the player smoothly."""
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

        # Update enemy hitbox position
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft )

