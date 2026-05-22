import pygame
import sys
from settings import *
from core.game import Game

class Menu():
    def __init__(self, screen, game):
        self.screen = screen
        self.assets = game.assets
        self.selected = 0
        self.options = ["Easy", "Medium", "Hard"]

    def draw_text(self, text, size, x, y, color=WHITE):
        font = pygame.font.Font(None, size)
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def run(self):
        while True:
            self.screen.fill(BLACK)

            self.draw_text("Звёздные войны", 60, WIDTH // 2, 120)
            self.draw_text("Бегство от астероидов", 40, WIDTH // 2, 180)

            for i, option in enumerate(self.options):
                color = RED if i == self.selected else WHITE
                self.draw_text(option, 40, WIDTH // 2, 300 + i * 60, color)

            self.draw_text("↑ ↓ для выбора, Enter для старта", 20, WIDTH // 2, HEIGHT - 50)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % 3
                    if event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % 3
                    if event.key == pygame.K_RETURN:
                        while True:
                            game = Game(self.screen, self.assets)
                            result = game.run(self.selected + 1)
                            if result == "restart":
                                continue
                            break
