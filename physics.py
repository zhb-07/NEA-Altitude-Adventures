import pygame
import config

grass_img = pygame.image.load("images/grass.png")
dirt_img = pygame.image.load("images/dirt.png")
stone_img = pygame.image.load("images/stone.png")
sky_img = pygame.image.load("images/sky.png")

screen = config.screen
screen_width = config.screen_width
screen_height = config.screen_height
player_image = config.playerimg
player_image.set_colorkey((255, 255, 255))
player_image = pygame.transform.scale(player_image, (50,50))

spike_group = pygame.sprite.Group()
en_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

print(config.playerimg)

tile_size = 50
game_over = False

tilemap = [ #                                    30 x 16
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "x............................x",
    "x................0......0....x",
    "x...............xxxx.xxxxxxxxx",
    "x..........xxx...............x",
    "x.......x....................x",
    "x............................x",
    "x..0.........................x",
    "x..xxx......x0...e...........x",
    "x............xxxxxxxxx...x...x",
    "x............................x",
    "x.........................0.xx",
    "x.......xx...xx...xxxxxxxxxxxx",
    "x.....xxxx^^^xx^^^xxxxxxxxxxxx",
    "x....xxxxxxxxxxxxxxxxxxxxxxxxx",
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

                elif tile == "^":
                    spike = Spikes(collumn_count * tile_size, row_count * tile_size)
                    spike_group.add(spike)

                elif tile == "e":
                    en = Enemy(collumn_count * tile_size, row_count * tile_size - 5)
                    en_group.add(en)

                elif tile == "0":
                    coin = Coins(collumn_count * tile_size + 25, row_count * tile_size)
                    coin_group.add(coin)

                collumn_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])

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
                self.y_vel = -10
                self.jumped = True
            else:
                self.jumped = False

            if key[pygame.K_a]:
                dx = dx - 3

            if key[pygame.K_d]:
                dx = dx + 3

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

            if pygame.sprite.spritecollide(self, en_group, False):
                game_over = True

            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = True



            self.rect.x = self.rect.x + dx
            self.rect.y = self.rect.y + dy

            screen.blit(self.image, self.rect)
            return game_over

class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("images/spikes.png")
        image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("images/coin.png")
        image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(image, (25,25))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)


class Enemy (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.move = 0

    def update(self):
        self.rect.x = self.rect.x + self.direction
        self.move = self.move + 1
        if abs(self.move) > 50:
            self.direction = self.direction * -1
            self.move = self.move * -1
world = World(tilemap, screen)
player = Player(100, screen_height - 130, screen)