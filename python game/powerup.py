import pygame
import os
from config import ASSETS_DIR

class PowerUp:
    def __init__(self, x, y, type):
        self.type = type
        if self.type == "triple_bonus":
            self.image = pygame.image.load(os.path.join(ASSETS_DIR, "triple_bonus.png")).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join(ASSETS_DIR, f"{type}.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.y += 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def apply(self, player):
        if self.type == "shield":
            player.shield = min(player.max_shield, player.shield + 25)
        elif self.type == "triple_bonus":
            player.triple = 300
        elif self.type == "health":
            player.health = min(player.max_health, player.health + 25)  
        elif self.type == "speed_up": 
            player.apply_speed_boost(boost=5, duration=600)
