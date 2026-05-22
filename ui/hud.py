import pygame
from settings import WHITE, RED

class Hud:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)
    def draw_bar(self, x, y, value, max_value, color):
        width = 200
        height = 15
        ratio = max(value / max_value, 0)
        pygame.draw.rect(self.screen, (50, 50, 50), (x, y, width, height))
        pygame.draw.rect(self.screen, color, (x, y, width * ratio, height))
    def draw_text(self, text, x, y, color = WHITE):
        font = self.font
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))
    def render(self, score, high_score, fuel, hull):
        self.draw_bar(20, 20, fuel, 100, WHITE)
        self.draw_bar(20, 45, hull, 100, RED)
        self.draw_text(f"Score: {score}", 20, 80)
        self.draw_text(f"High Score: {high_score}", 20, 110)
