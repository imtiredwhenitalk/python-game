import pygame
import random
import os 
from config import WIDTH, HEIGHT, ASSETS_DIR
from player import Player
from enemy import Enemy
from boss import Boss
from powerup import PowerUp
from bullet import Bullet

class Game:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.player = Player()
        self.wave = 1
        self.max_waves = 5
        self.difficulty = "normal" 
        self.enemies = self.create_enemies_grid(self.wave)
        self.bosses = []
        self.powerups = []
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.high_score = 0
        self.load_high_score()
        self.load_assets()
        self.enemy_shoot_timer = 0
        self.shooter_queue = []

    def create_enemies_grid(self, wave):
        enemies = []
        if self.difficulty == "easy":
            base = 5
            step = 5
        elif self.difficulty == "normal":
            base = 5
            step = 10
        else:  # Сложно
            base = 10
            step = 15  
        count = base + (wave - 1) * step
        cols = min(count, 10)
        rows = (count + 9) // 10
        spacing_x = WIDTH // 10
        spacing_y = 50
        idx = 0
        for row in range(rows):
            for col in range(10):
                if idx >= count:
                    break
                x = col * spacing_x + 10
                y = 50 + row * spacing_y
                enemies.append(Enemy(x, y))
                idx += 1
        return enemies

    def run(self): 
        pygame.mouse.set_visible(True)
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
            pygame.display.set_caption(f"Перший проект - Score: {self.score} | High Score: {self.high_score}")
            if self.player.health <= 0:
                self.player.health = 0
                self.player.rect.y = HEIGHT - 30
                self.player.rect.x = WIDTH // 2
            if self.player.health > 100:
                self.player.health = 100
            if self.player.health <= 0:
                self.game_over()
            if self.score > self.high_score:
                print("Новий рекорд!")
                self.high_score = self.score
                self.save_high_score()

    def load_assets(self):
        self.player_image = pygame.image.load(os.path.join(ASSETS_DIR, "player.png")).convert_alpha()
        self.enemy_image = pygame.image.load(os.path.join(ASSETS_DIR, "enemy.png")).convert_alpha()
        self.bullet_image = pygame.image.load(os.path.join(ASSETS_DIR, "bullet.png")).convert_alpha()
        self.boss_image = pygame.image.load(os.path.join(ASSETS_DIR, "boss.png")).convert_alpha()
        self.powerup_images = {
            "shield": pygame.image.load(os.path.join(ASSETS_DIR, "shield.png")).convert_alpha(),
            "triple": pygame.image.load(os.path.join(ASSETS_DIR, "triple.png")).convert_alpha(),
            "health": pygame.image.load(os.path.join(ASSETS_DIR, "health.png")).convert_alpha(), 
            "speed_up": pygame.image.load(os.path.join(ASSETS_DIR, "speed_up.png")).convert_alpha()
        }

    def load_high_score(self):
        try:
            with open(os.path.join(ASSETS_DIR, "high_score.txt"), "r") as f:
                self.high_score = int(f.read())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

    def save_high_score(self):
        with open(os.path.join(ASSETS_DIR, "high_score.txt"), "w") as f:
            if self.score > self.high_score:
                self.high_score = self.score
            f.write(str(self.high_score))

    def game_over(self):
        pygame.quit()
        import sys
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                if event.key == pygame.K_ESCAPE:
                    self.show_menu()  # Меню

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move("left")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move("right")
        self.player.update()

        if not self.enemies and not self.bosses:
            if self.wave < self.max_waves:
                self.wave += 1
                self.enemies = self.create_enemies_grid(self.wave)
            else:
                if not self.bosses:
                    self.bosses.append(Boss(WIDTH // 2 - 50, 50))

        self.enemy_shoot_timer += 1
        if self.enemy_shoot_timer >= 300:
            alive_enemies = [e for e in self.enemies if e.health > 0]
            if len(alive_enemies) > 0:
                if not self.shooter_queue or len(self.shooter_queue) < 5:
                    random.shuffle(alive_enemies)
                    self.shooter_queue = alive_enemies.copy()
                shooters = self.shooter_queue[:5]
                self.shooter_queue = self.shooter_queue[5:]
                for enemy in self.enemies:
                    enemy.can_shoot = False
                for enemy in shooters:
                    enemy.can_shoot = True
            self.enemy_shoot_timer = 0

        for enemy in self.enemies:
            enemy.update()
            if enemy.can_shoot and enemy.cooldown == 0:
                enemy.bullets.append(Bullet(enemy.rect.centerx, enemy.rect.bottom, "down"))
                enemy.cooldown = 300
            for bullet in enemy.bullets:
                bullet.update()
            enemy.bullets = [b for b in enemy.bullets if not b.off_screen()]

        for boss in self.bosses: 
            boss.update() 
            for bullet in boss.bullets: 
                bullet.update() 
            boss.bullets = [b for b in boss.bullets if not b.off_screen()] 
            if boss.health <= boss.last_powerup_hp - 100: 
                self.powerups.append(PowerUp(boss.rect.x, boss.rect.y, random.choice(["shield", "health", "triple", "speed_up", "double_damage"]))) 
                boss.last_powerup_hp = boss.health

        for powerup in self.powerups:
            powerup.update()
        self.powerups = [p for p in self.powerups if p.rect.y < HEIGHT]

        self.check_collisions()

    def check_collisions(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if self.player.shield > 0:
                    self.player.shield = 0  
                else:
                    self.player.health -= 10
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect): 
                    damage = 20 if self.player.has_double_damage() else 10
                    enemy.health -= damage
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    if enemy.health <= 0:
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                        self.score += 100
                        rand = random.random()
                        if rand < 0.05:
                            self.powerups.append(PowerUp(enemy.rect.x, enemy.rect.y, "triple_bonus"))
                        elif rand < 0.35:
                            self.powerups.append(PowerUp(enemy.rect.x, enemy.rect.y, "shield"))
                        elif rand < 0.45:
                            self.powerups.append(PowerUp(enemy.rect.x, enemy.rect.y, "health")) 
                        elif rand < 0.50: 
                            self.powerups.append(PowerUp(enemy.rect.x, enemy.rect.y, "speed_up")) 
                        elif rand < 0.53: 
                            self.powerups.append(PowerUp(enemy.rect.x, enemy.rect.y, "double_damage"))
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                if bullet.rect.colliderect(self.player.rect):
                    if self.player.shield > 0:
                        self.player.shield = 0  
                    else:
                        self.player.health -= 10
                    if bullet in enemy.bullets:
                        enemy.bullets.remove(bullet) 

        for boss in self.bosses: 
            for bullet in self.player.bullets[:]: 
                if bullet.rect.colliderect(boss.rect):  
                    damage = 20 if self.player.has_double_damage() else 10
                    boss.take_damage(damage) 
                    if bullet in self.player.bullets: 
                        self.player.bullets.remove(bullet) 
                    if boss.health <= 0: 
                        self.bosses.remove(boss) 
                        self.score += 1000 
        
        for boss in self.bosses: 
            for bullet in boss.bullets[:]: 
                if bullet.rect.colliderect(self.player.rect): 
                    if self.player.shield > 0: 
                        self.player.shield = 0 
                    else: 
                        self.player.health -= 20 
                    boss.bullets.remove(bullet)
               

        for powerup in self.powerups[:]:
            if powerup.rect.colliderect(self.player.rect):
                powerup.apply(self.player)
                self.powerups.remove(powerup)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for boss in self.bosses:
            boss.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        self.draw_score()
        pygame.display.flip()

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        if self.player.shield > 0:
            health_text = self.font.render(
                f"Health: {self.player.health} | Shield: {self.player.shield}", True, (0, 255, 0)
            )
        else:
            health_text = self.font.render(
                f"Health: {self.player.health}", True, (0, 255, 0)
            )
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))
        self.screen.blit(health_text, (WIDTH // 2 - 100, HEIGHT - 40))

    def show_menu(self):
        pygame.mouse.set_visible(True)
        menu_font = pygame.font.Font(None, 60)
        small_font = pygame.font.Font(None, 36)
        options = ["Easy", "Normal", "Hard", "Exit"]
        selected = 1  
        music_on = True
        running = True

        while running:
            self.screen.fill((20, 20, 40))
            title = menu_font.render("SPACE GAME", True, (255, 255, 0))
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

            mouse_x, mouse_y = pygame.mouse.get_pos()
            hovered = None

            for i, opt in enumerate(options):
                rect = pygame.Rect(WIDTH // 2 - 60, 200 + i * 60, 120, 40)
                if rect.collidepoint(mouse_x, mouse_y):
                    hovered = i
                    color = (255, 255, 0)
                else:
                    color = (0, 255, 0) if i == selected else (255, 255, 255)
                text = small_font.render(opt, True, color)
                self.screen.blit(text, rect.topleft)

            music_rect = pygame.Rect(WIDTH // 2 - 60, 200 + len(options) * 60, 120, 40)
            music_color = (255, 255, 0) if music_rect.collidepoint(mouse_x, mouse_y) else (255, 255, 255)
            music_text = small_font.render(f"Music: {'On' if music_on else 'Off'}", True, music_color)
            self.screen.blit(music_text, music_rect.topleft)

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
                        if selected == 0:
                            self.difficulty = "easy"
                            running = False
                        elif selected == 1:
                            self.difficulty = "normal"
                            running = False
                        elif selected == 2:
                            self.difficulty = "hard"
                            running = False
                        elif selected == 3:  # Exit
                            pygame.quit()
                            exit()
                    if event.key == pygame.K_m:
                        music_on = not music_on
                        if music_on:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in range(len(options)):
                        rect = pygame.Rect(WIDTH // 2 - 60, 200 + i * 60, 120, 40)
                        if rect.collidepoint(mouse_x, mouse_y):
                            selected = i
                            if selected == 0:
                                self.difficulty = "easy"
                                running = False
                            elif selected == 1:
                                self.difficulty = "normal"
                                running = False
                            elif selected == 2:
                                self.difficulty = "hard"
                                running = False
                            elif selected == 3:
                                pygame.quit()
                                exit()
                    if music_rect.collidepoint(mouse_x, mouse_y):
                        music_on = not music_on
                        if music_on:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
            if hovered is not None:
                selected = hovered

            pygame.time.wait(60)