import pygame
import os
import sys
from config import WIDTH, HEIGHT, ASSETS_DIR
from game import Game

if not os.path.exists(ASSETS_DIR):
    print("Error: Assets directory not found!")
    sys.exit(1)
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Перший проект")
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)
if not pygame.mixer.get_init():
    print("Error: Pygame mixer not initialized!")
    sys.exit(1)

music_path = os.path.join(ASSETS_DIR, "backgroundmusic.mp3")
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
else:
    print("Warning: background music file not found!")

if not pygame.font.get_init():
    print("Error: Pygame font not initialized!")
    sys.exit(1)
background_path = os.path.join(ASSETS_DIR, "background.png")
if not os.path.exists(background_path):
    print("Error: Background image not found!")
    sys.exit(1)
background = pygame.image.load(background_path).convert() 

game = Game(screen, background)
game.show_menu()  # Додаємо це перед run
game.run() 
pygame.quit() 