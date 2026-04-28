import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Звёздные войны")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,150,255)

clock = pygame.time.Clock()
FPS = 60

# --- ЗАГРУЗКА ---
ship_frames = [
    pygame.transform.scale(pygame.image.load("ship.png"), (50,50)),
    pygame.transform.scale(pygame.image.load("ship2.png"), (50,50))
]

asteroid_img = pygame.transform.scale(pygame.image.load("asteroid.png"), (50,50))
background = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH,HEIGHT))

explosion_sound = pygame.mixer.Sound("explosion.wav")

# --- РЕКОРД ---
def load_high_score():
    if not os.path.exists("high_score.txt"):
        return 0
    return int(open("high_score.txt").read())

def save_high_score(score):
    open("high_score.txt","w").write(str(score))

# --- ТЕКСТ ---
def draw_text(text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x,y))
    screen.blit(surf, rect)

# --- ИГРОК ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = ship_frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-70))
        self.speed = 6

        self.animation_timer = 0
        self.shield = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        # --- АНИМАЦИЯ ---
        self.animation_timer += 1
        if self.animation_timer > 10:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.animation_timer = 0

        # --- ЩИТ ---
        if self.shield > 0:
            self.shield -= 1

# --- АСТЕРОИД ---
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, speed_mult=1):
        super().__init__()
        self.image = asteroid_img
        self.rect = self.image.get_rect()
        self.speed_mult = speed_mult
        self.reset()

    def reset(self):
        self.rect.x = random.randint(0, WIDTH-50)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3,6) * self.speed_mult

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset()

# --- БОНУС ---
class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["shield","slow"])
        self.image = pygame.Surface((30,30))
        self.image.fill(BLUE if self.type=="shield" else RED)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, WIDTH-30)
        self.rect.y = random.randint(-100, -40)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

# --- GAME OVER ---
def game_over(score):
    while True:
        screen.fill(BLACK)
        draw_text("GAME OVER", 60, WIDTH//2, 200, RED)
        draw_text(f"Счёт: {score}", 40, WIDTH//2, 300)
        draw_text("Нажми R чтобы заново", 30, WIDTH//2, 400)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return

# --- ИГРА ---
def game(mode):
    player = Player()
    sprites = pygame.sprite.Group(player)
    asteroids = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()

    difficulty = 1
    speed_mult = 1

    for _ in range(5):
        a = Asteroid(speed_mult)
        asteroids.add(a)
        sprites.add(a)

    score = 0
    high_score = load_high_score()
    slow_timer = 0

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- ВЫЖИВАНИЕ ---
        if mode == "survival":
            speed_mult = 1 + score / 500

        # --- СПАВН БОНУСОВ ---
        if random.randint(1,200) == 1:
            b = Bonus()
            bonuses.add(b)
            sprites.add(b)

        sprites.update()

        # --- СТОЛКНОВЕНИЕ ---
        if pygame.sprite.spritecollide(player, asteroids, False):
            if player.shield > 0:
                player.shield = 0
            else:
                explosion_sound.play()
                if score > high_score:
                    save_high_score(score)
                game_over(score)
                return

        # --- БОНУСЫ ---
        hits = pygame.sprite.spritecollide(player, bonuses, True)
        for b in hits:
            if b.type == "shield":
                player.shield = 300
            elif b.type == "slow":
                slow_timer = 300

        # --- ЗАМЕДЛЕНИЕ ---
        if slow_timer > 0:
            slow_timer -= 1
            for a in asteroids:
                a.rect.y += 1  # замедление

        # --- ОТРИСОВКА ---
        screen.blit(background, (0,0))
        sprites.draw(screen)

        if player.shield > 0:
            pygame.draw.circle(screen, BLUE, player.rect.center, 35, 2)

        draw_text(f"Счёт: {score}", 30, WIDTH//2, 20)
        draw_text(f"Рекорд: {high_score}", 30, WIDTH//2, 50)

        pygame.display.flip()
        score += 1

# --- МЕНЮ ---
def menu():
    options = ["Обычный", "Выживание"]
    selected = 0

    while True:
        screen.fill(BLACK)

        draw_text("SPACE GAME", 60, WIDTH//2, 150)

        for i, option in enumerate(options):
            color = RED if i==selected else WHITE
            draw_text(option, 40, WIDTH//2, 300+i*60, color)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected-1)%2
                if event.key == pygame.K_DOWN:
                    selected = (selected+1)%2
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        game("normal")
                    else:
                        game("survival")

menu()