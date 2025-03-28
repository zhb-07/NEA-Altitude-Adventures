import pygame
from pygame.examples.cursors import image
from pygame.sprite import Sprite

from config import screen_height
from config import screen

player_image = pygame.image.load("images/player.png")
player_image.set_colorkey((255, 255, 255))

grass_img = pygame.image.load("images/grass.png")
spikes_img = pygame.image.load("images/spikes.png")
dirt_img = pygame.image.load("images/dirt.png")
stone_img = pygame.image.load("images/stone.png")
enemy_image = pygame.image.load("images/player.png")
sky_img = pygame.image.load("images/sky.png")

tile_size = 50
game_over = False

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
    "x.....xx.....................x",
    "x....x..//...................x",
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

                elif tile == "/":
                    spike = Spikes(collumn_count * tile_size, row_count * tile_size)
                    spike_group.add(spike)

                collumn_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Player:
    def __init__(self, x, y, screen):
        self.screen = screen
        self.screen_height = screen_height
        self.image = pygame.transform.scale(player_image, (40,80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.y_vel = 0
        self.jumped = False

    def update(self, screen, game_over):
        self.screen = screen

        dx = 0
        dy = 0
        if game_over == False:
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

            for tile in world.tile_list:

                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width , self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width , self.height):
                    if self.y_vel < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.y_vel = 0
                    elif self.y_vel >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.y_vel = 0

            if pygame.sprite.spritecollide(self,spike_group, False):
                game_over = True

            self.rect.x = self.rect.x + dx
            self.rect.y = self.rect.y + dy

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0

            screen.blit(self.image, self.rect)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

            return game_over

class Spikes(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite,Sprite.__init__(self)
        self.image = pygame.transform.scale(spikes_img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


spike_group = pygame.sprite.Group()
world = World(tilemap, screen)
player = Player(100, screen_height - 130, screen)