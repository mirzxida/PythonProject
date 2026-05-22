import pygame
import random

from settings import *


class PowerUp(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.type = random.choice([
            "fuel",
            "shield",
            "slow"
        ])

        self.image = pygame.Surface((25, 25))

        colors = {
            "fuel": (0, 255, 0),
            "shield": (0, 100, 255),
            "slow": (255, 255, 0)
        }

        self.image.fill(
            colors[self.type]
        )

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(
            50,
            WIDTH - 50
        )

        self.rect.y = -50

        self.speed = 3

    def update(self):

        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()