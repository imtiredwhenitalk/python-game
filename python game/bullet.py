import pygame
import os
from config import ASSETS_DIR, HEIGHT

class Bullet:
    def __init__(self, x, y, direction, triple=False, speed=15):
        if triple:
            self.image = pygame.image.load(os.path.join(ASSETS_DIR, "triple.png")).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join(ASSETS_DIR, "bullet.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = speed
        self.speed = speed
        self.direction = direction

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.y < 0 or self.rect.y > HEIGHT
