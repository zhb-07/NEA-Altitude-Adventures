import pygame

class Player:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.velocity = 5
        self.jump_power = -15
        self.gravity = 1
        self.y_velocity = 0
        self.grounded = False

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.velocity
        if keys[pygame.K_d]:
            self.rect.x += self.velocity
        if keys[pygame.K_SPACE] and self.grounded or keys[pygame.K_w] and self.grounded:
            self.jump()

    def jump(self):
        self.y_velocity = self.jump_power
        self.grounded = False

    def apply_gravity(self, ground_level):
        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity

        # Stop falling when hitting the ground
        if self.rect.y >= ground_level:
            self.rect.y = ground_level
            self.y_velocity = 0
            self.grounded = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

