import pygame, os

class Projectile:
    def __init__(self, x, y, speed_x, speed_y, is_monster=False):
        base = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites")
        img_path = os.path.join(base, "fireball.png")
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.x, self.y = x, y
        self.speed_x, self.speed_y = speed_x, speed_y
        self.is_monster = is_monster
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
