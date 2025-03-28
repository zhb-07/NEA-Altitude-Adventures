import pygame

from main import height
from main import screen

player_image = pygame.image.load("images/player.png")
player_image.set_colorkey((255, 255, 255))

grass_img = pygame.image.load("images/grass.png")
dirt_img = pygame.image.load("images/dirt.png")
stone_img = pygame.image.load("images/stone.png")
enemy_image = pygame.image.load("images/player.png")
sky_img = pygame.image.load("images/sky.png")

tile_size = 50

tilemap = [
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "x............................x",
    "x............................x",
    "x............................x",
    "x............................x",
    "x............................x",
    "x............................x",
    "x............................x",
    "x............................x",
    "x............................x",
    "x............................x",
    "x............................x",
    "x............................x",
    "x............................x",
    "x............................x",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
]


class World:
    def __init__(self, data, screen):
        self.screen = screen
        self.tile_list = []

        row_count = 0
        for row in data:
            collumn_count = 0
            for tile in row:
                if tile == "x":
                    img = pygame.transform.scale(stone_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = collumn_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                elif tile == "-":
                    img = pygame.transform.scale(sky_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = collumn_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                collumn_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])

class Player:
    def __init__(self, x, y, screen):
        self.screen = screen
        self.height = height
        self.image = pygame.transform.scale(player_image, (40,80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_vel = 0
        self.jumped = False

    def update(self,screen):
        self.screen = screen

        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_w] and self.jumped == False or  key[pygame.K_SPACE] and self.jumped == False:
            self.y_vel = -3
            self.jumped = True
        if key[pygame.K_w] == False or  key[pygame.K_SPACE] == False:
            self.jumped = False

        if key[pygame.K_a]:
            dx = dx - 1

        if key[pygame.K_d]:
            dx = dx + 1

        self.y_vel = self.y_vel + 1
        if self.y_vel > 10:
            self.y_vel = 10
        dy = dy + self.y_vel

        self.rect.x = self.rect.x + dx
        self.rect.y = self.rect.y + dy

        if self.rect.bottom > height:
            self.rect.bottom = height
            dy = 0

        screen.blit(self.image, self.rect)
