import pygame
import sys
import random

from settings import *
from entities.player import Player
from entities.asteroid import Asteroid
from utils.storage import load, save
from systems.events import Event
from ui.hud import Hud
from ui.game_over import GameOverScreen
from systems.effects import Effects
from entities.powerups import PowerUp

class Game:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.fuel = 100
        self.hull = 100
        self.hud = Hud(screen)
        self.game_over = GameOverScreen(screen)
        self.bg_y = 0
        self.shake = 0
        self.powerups = pygame.sprite.Group()
        self.power_timer = 0
        pygame.mixer.init()
        self.sounds = {"hit": pygame.mixer.Sound("assets/sounds/hit.mp3"),
            "game_over": pygame.mixer.Sound("assets/sounds/game_over.mp3")}
        self.sounds["hit"].set_volume(0.6)
        self.sounds["game_over"].set_volume(1.0)
        self.last_hit_time = 0
        self.hit_lock = False

        self.clock = pygame.time.Clock()

        self.player = Player(assets["ship"])
        self.all_sprites = pygame.sprite.Group(self.player)
        self.asteroids = pygame.sprite.Group()
        self.events =Event()
        self.effects = Effects()

        self.score = 0
        self.save_data = load()
        self.high_score = self.save_data.get("high_score", 0)

    def _finish_run(self):
        if self.score > self.high_score:
            self.save_data["high_score"] = self.score
            save(self.save_data)
            pygame.mixer.stop()
            self.sounds["game_over"].play()
            print("GAME OVER SOUND")
            pygame.time.delay(400)
        return self.game_over.run(self.score)

    def spawn_asteroids(self, difficulty):
        for _ in range(5 * difficulty):
            a = Asteroid(self.assets["asteroid"])
            self.asteroids.add(a)
            self.all_sprites.add(a)
    def run(self, difficulty):
        self.spawn_asteroids(difficulty)
        running = True
        paused = False
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if paused:
                font = pygame.font.Font(None, 60)
                text = font.render("PAUSE", True, WHITE)
                self.screen.blit(text, (300, 250))
                pygame.display.flip()
                continue
            self.events.update()
            self.effects.update()
            self.all_sprites.update()
            self.fuel -= 0.02

            self.power_timer += 1

            if self.power_timer >= 400:
                self.power_timer = 0
                power = PowerUp()
                self.powerups.add(power)
                self.all_sprites.add(power)

            if pygame.sprite.spritecollide(self.player, self.asteroids, False):
                collisions = pygame.sprite.spritecollide(
                    self.player,
                    self.asteroids,
                    False
                )
                if collisions:
                    if not self.hit_lock:
                        self.hit_lock = True
                        self.sounds["hit"].play()
                        self.hull =0
                        if self.hull <= 0:
                            return self._finish_run()
                else:
                    self.hit_lock = False
                self.effects.trigger()
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.fill(WHITE)
                overlay.set_alpha(180)
                self.screen.blit(overlay, (0, 0))
                pygame.display.flip()
                pygame.time.delay(150)
                self.hull -= 20
                if self.hull <= 0:
                    return self._finish_run()
            collected = pygame.sprite.spritecollide(self.player, self.powerups, True)
            for p in collected:
                if p.type == "fuel":
                    self.fuel = min(100, self.fuel + 20)
                elif p.type == "shield":
                    self.hull = min(100, self.hull + 30)
                elif p.type == "slow":
                    for asteroid in self.asteroids:
                        asteroid.speed *= 0.7

            if self.hull <= 0 or self.fuel <= 0:
                return self._finish_run()

            self.bg_y += 0.5
            if self.bg_y >= HEIGHT:
                self.bg_y = 0
            self.screen.blit(self.assets["background"], (0, self.bg_y - HEIGHT))
            self.screen.blit(self.assets["background"], (0, self.bg_y))
            self.all_sprites.draw(self.screen)
            event_text = self.events.get_event()
            self.hud.render(self.score,
                            self.high_score,
                            self.fuel,
                            self.hull)
            if event_text:
                font = pygame.font.SysFont(None, 28)
                surface = font.render(str(event_text), True, WHITE)
                self.screen.blit(surface, (20, 150))
            offset_x = 0
            offset_y = 0

            if self.shake > 0:
                import random
                offset_x = random.randint(-3, 3)
                offset_y = random.randint(-3, 3)
                self.shake -= 1
            if self.effects.flash:
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(120)
                overlay.fill(WHITE)
                self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            self.score += 1
            for asteroid in self.asteroids:
                asteroid.speed += 0.0005