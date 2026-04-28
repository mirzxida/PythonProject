import pygame
import random
import sys
import os

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Звёздные войны: Бегство от астероидов")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60
clock = pygame.time.Clock()


ship_img = pygame.image.load("ship.png")
asteroid_img = pygame.image.load("asteroid.png")
background_img = pygame.image.load("background.png")

ship_img = pygame.transform.scale(ship_img, (50, 50))
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))


stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(100)]

def draw_stars():
    for star in stars:
        star[1] += 1
        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, WHITE, star, 2)


def draw_text(text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


def load_high_score():
    if not os.path.exists("high_score.txt"):
        return 0
    with open("high_score.txt", "r") as file:
        return int(file.read())

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ship_img
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-60))
        self.speed = 6

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_img
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset()


def game(difficulty):
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    asteroids = pygame.sprite.Group()

    for _ in range(5 * difficulty):
        a = Asteroid()
        asteroids.add(a)
        all_sprites.add(a)

    score = 0
    high_score = load_high_score()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update()


        if pygame.sprite.spritecollide(player, asteroids, False):
            if score > high_score:
                save_high_score(score)
            return


        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)

        draw_text(f"Счёт: {score}", 30, WIDTH//2, 20)
        draw_text(f"Рекорд: {high_score}", 30, WIDTH//2, 50)

        pygame.display.flip()

        score += 1

def menu():
    options = ["Лёгкий", "Средний", "Сложный"]
    selected = 0

    while True:
        screen.fill(BLACK)
        draw_stars()

        draw_text("Звёздные войны", 60, WIDTH//2, 120)
        draw_text("Бегство от астероидов", 40, WIDTH//2, 180)

        for i, option in enumerate(options):
            color = RED if i == selected else WHITE
            draw_text(option, 40, WIDTH//2, 300 + i*60, color)

        draw_text("↑ ↓ для выбора, Enter для старта", 20, WIDTH//2, HEIGHT-50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 3
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                if event.key == pygame.K_RETURN:
                    game(selected + 1)

menu()