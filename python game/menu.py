import pygame
import os
import sys
from config import WIDTH, HEIGHT, ASSETS_DIR
from game import Game

def show_menu(self):
    pygame.mouse.set_visible(True)
    menu_font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 36)
    options = ["Easy", "Normal", "Hard"]
    selected = 0
    music_on = True
    running = True

    while running:
        self.screen.fill((20, 20, 40))
        title = menu_font.render("SPACE GAME", True, (255, 255, 0))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        for i, opt in enumerate(options):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            text = small_font.render(opt, True, color)
            self.screen.blit(text, (WIDTH // 2 - 60, 200 + i * 60))

        music_text = small_font.render(f"Music: {'On' if music_on else 'Off'}", True, (255, 255, 255))
        self.screen.blit(music_text, (WIDTH // 2 - 60, 400))

        cursor_y = 200 + selected * 60
        pygame.draw.polygon(self.screen, (255, 255, 0), [
            (WIDTH // 2 - 80, cursor_y + 10),
            (WIDTH // 2 - 70, cursor_y),
            (WIDTH // 2 - 70, cursor_y + 20)
        ])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    # Встановлюємо складність
                    if selected == 0:
                        self.difficulty = "easy"
                    elif selected == 1:
                        self.difficulty = "normal"
                    else:
                        self.difficulty = "hard"
                    running = False
                if event.key == pygame.K_m:
                    music_on = not music_on
                    if music_on:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
        # Додаємо підтримку кліку мишкою по опціям
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            for i in range(len(options)):
                rect = pygame.Rect(WIDTH // 2 - 60, 200 + i * 60, 120, 40)
                if rect.collidepoint(mx, my):
                    selected = i
                    if selected == 0:
                        self.difficulty = "easy"
                    elif selected == 1:
                        self.difficulty = "normal"
                    else:
                        self.difficulty = "hard"
                    running = False
            # Клік по Music
            music_rect = pygame.Rect(WIDTH // 2 - 60, 400, 120, 40)
            if music_rect.collidepoint(mx, my):
                music_on = not music_on
                if music_on:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
        pygame.time.wait(120)