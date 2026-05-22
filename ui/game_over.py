import pygame
import sys

from settings import *

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.big = pygame.font.Font(None, 80)
        self.small = pygame.font.Font(None, 35)
    def draw_center(self, text, y, color = WHITE, big = False):
        font = self.big if big else self.small
        surface = font.render(text, True, color)
        rect = surface.get_rect(center = (WIDTH // 2, y))
        self.screen.blit(surface, rect)
    def run(self, score):
        pygame.event.clear()
        while True:
            self.screen.fill(BLACK)
            self.draw_center("SIGNAL LOST", 180, RED, True)
            self.draw_center(f"SCORE: {score}", 300)
            self.draw_center("MISSION FAILED", 340)
            self.draw_center("ENTER - RESTART", 400)
            self.draw_center("ESC - MENU", 450)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    if event.key == pygame.K_RETURN:
                        return "restart"