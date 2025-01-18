import pygame


class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health, screen):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, 'black', (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, 'darkgreen', (self.x, self.y, 150 * ratio, 20))
