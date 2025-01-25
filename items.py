import pygame

from message import Message
from settings import *
from image import *
from create_pers import *


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        super().__init__()
        self.item_type = item_type
        self.count = 0
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, player, SCREEN_SCROLL):
        self.rect.x += SCREEN_SCROLL
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                self.count = 25
                player.health += self.count
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                self.count = 15
                player.ammo += self.count
            elif self.item_type == 'Grenade':
                self.count = 3
                player.grenades += self.count
            elif self.item_type == 'Bonus':
                self.kill()
                return 10
            message = Message(self.count, player.rect.midtop[0], player.rect.midtop[1])
            message_group.add(message)
            self.kill()
        return 0
