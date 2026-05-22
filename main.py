import pygame

from settings import *
from core.game import Game
from ui.menu import Menu

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
assets = {"ship": pygame.transform.scale(pygame.image.load("assets/ship.png"), (50, 50)),
          "asteroid": pygame.transform.scale(pygame.image.load("assets/asteroid.png"), (50, 50)),
          "background": pygame.transform.scale(pygame.image.load("assets/background.png"), (WIDTH, HEIGHT)),}
game = Game(screen, assets)
menu = Menu(screen, game)
menu.run()