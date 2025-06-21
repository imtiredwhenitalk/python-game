import pygame
import os
from config import ASSETS_DIR
from bullet import Bullet

class Boss:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "boss.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 1500
        self.cooldown = 0
        self.bullets = []

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def can_shoot(self):
        return self.cooldown == 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.can_shoot():
            self.cooldown = 300
            self.bullets.append(Bullet(self.rect.centerx, self.rect.bottom, "down"))
        for bullet in self.bullets:
            bullet.update()
            bullet.draw(screen)

    def check_collision(self, bullet):
        if self.rect.colliderect(bullet.rect):
            self.health -= 10
            return True
        return False