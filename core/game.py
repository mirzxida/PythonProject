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

class Game:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.fuel = 100
        self.hull = 100
        self.hud = Hud(screen)
        self.game_over = GameOverScreen(screen)

        self.clock = pygame.time.Clock()

        self.player = Player(assets["ship"])
        self.all_sprites = pygame.sprite.Group(self.player)
        self.asteroids = pygame.sprite.Group()
        self.events =Event()

        self.score = 0
        self.save_data = load()
        self.high_score = self.save_data.get("high_score", 0)
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
            self.all_sprites.update()
            self.fuel -= 0.02

            if pygame.sprite.spritecollide(self.player, self.asteroids, False):
                self.hull -= 20
                if self.score > self.high_score:
                    self.save_data["high_score"] = self.score
                    save(self.save_data)
                return
            if self.hull <= 0 or self.fuel <= 0:
                if self.score > self.high_score:
                    self.save_data["high_score"] = self.score
                    save(self.save_data)
                result = self.game_over.run(self.score)
                return result

            self.screen.blit(self.assets["background"], (0, 0))
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

            pygame.display.flip()
            self.score += 1