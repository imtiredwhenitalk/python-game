import pygame
import os
from config import ASSETS_DIR
from bullet import Bullet

WIDTH = 800
HEIGHT = 600

class Boss:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "boss.png")).convert_alpha()
        self.rect = self.image.get_rect(x=x, y=y, width=100, height=60)
        self.health = 1500 
        self.shield = 300
        self.bullets = [] 
        self.direction = 1 
        self.last_powerup_hp = self.health
        self.cooldown = 0 

    def update(self): 
        self.rect.x += 3 * self.direction  
        if self.rect.right >= WIDTH or self.rect.left <= 0: 
            self.direction *= -1 
        
        if self.cooldown > 0: 
            self.cooldown -= 1 
        else: 
            self.shoot() 
            self.cooldown = 60  

    def shoot(self):
        cx, cy = self.rect.centerx, self.rect.bottom 
        self.bullets.append(Bullet(cx, cy, "down")) 
        self.bullets.append(Bullet(cx - 20, cy, "down_left")) 
        self.bullets.append(Bullet(cx + 20, cy, "down_right"))  
    
    def take_damage(self, amount): 
        if self.shield > 0: 
            absorbed = min(self.shield, amount) 
            self.shield -= absorbed 
            amount -= absorbed 
        self.health -= amount

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.update()
            bullet.draw(screen)

    def check_collision(self, bullet):
        if self.rect.colliderect(bullet.rect):
            self.health -= 10
            return True
        return False