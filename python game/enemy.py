import pygame
import os
from config import ASSETS_DIR
from bullet import Bullet

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "enemy.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.cooldown = 300
        self.health = 100
        self.bullets = []
        self.can_shoot = False

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            self.bullets.append(Bullet(self.rect.centerx, self.rect.bottom, "down"))
            self.cooldown = 300

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)
            bullet.speed = 5