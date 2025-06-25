import pygame
import os
from config import ASSETS_DIR, WIDTH, HEIGHT
from bullet import Bullet

class Player:
    def __init__(self):
        self.image_normal = pygame.image.load(os.path.join(ASSETS_DIR, "player.png")).convert_alpha()
        self.image_shield = pygame.image.load(os.path.join(ASSETS_DIR, "player_shield.png")).convert_alpha()
        self.image_triple = pygame.image.load(os.path.join(ASSETS_DIR, "triple_bonus.png")).convert_alpha()
        self.image_normal = pygame.transform.scale(self.image_normal, (50, 50))
        self.image_shield = pygame.transform.scale(self.image_shield, (50, 50))
        self.image_triple = pygame.transform.scale(self.image_triple, (50, 50))
        self.image = self.image_normal
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT-30))
        self.speed = 7 
        self.speed_boost = 0 
        self.speed_boost_timer = 0
        self.shield = 0
        self.max_shield = 100
        self.triple = 0
        self.bullets = [] 
        self.double_damage = 0
        self.health = 100
        self.max_health = 100 
    
    def get_speed(self): 
        return self.speed + self.speed_boost 

    def move(self, direction): 
        move_speed = self.get_speed()
        if direction == "left":
            self.rect.x -= move_speed
        elif direction == "right":
            self.rect.x += move_speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x)) 
    
    def apply_speed_boost(self, boost=5, duration=600): 
        self.speed_boost = boost 
        self.speed_boost_timer = duration 
    
    def apply(self, player): 
        if self.type == "shield": 
            player.shield = min(player.max_shield, player.shield + 25) 
        elif self.type == "triple_bonus": 
            player.triple = 300 
        elif self.type == "health": 
            player.health = min(player.max_health, player.health + 25) 
        elif self.type == "speed_up": 
            player.apply_speed_boost(boost=5,duration=600) 
        elif self.type == "double_damage": 
            player.double_damage = 300

    def update(self):
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if not b.off_screen()]
        if self.shield > 0:
            self.image = self.image_shield
        elif self.triple > 0:
            self.image = self.image_triple
        else:
            self.image = self.image_normal
        if self.shield < 0:
            self.shield = 0
        if self.triple < 0:
            self.triple = 0 
        if self.speed_boost_timer > 0: 
            self.speed_boost_timer -= 1 
            if self.speed_boost_timer == 0: 
                self.speed_boost = 0 
            if self.double_damage > 0: 
                self.double_damage -= 1  

    def has_double_damage(self): 
        return self.double_damage > 0
    
    def shoot(self):
        if self.triple > 0:
            self.bullets.append(Bullet(self.rect.centerx, self.rect.top, "up", triple=True))
            self.bullets.append(Bullet(self.rect.centerx - 20, self.rect.top, "up", triple=True))
            self.bullets.append(Bullet(self.rect.centerx + 20, self.rect.top, "up", triple=True))
        else:
            self.bullets.append(Bullet(self.rect.centerx, self.rect.top, "up", triple=False))
        if len(self.bullets) > 10:
            self.bullets = self.bullets[-10:]
        self.rect = self.image.get_rect(midbottom=(self.rect.centerx, self.rect.bottom))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)