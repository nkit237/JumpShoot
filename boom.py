from explosion import *
from image import *
from create_pers import *


class Boom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 8
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, player, world, SCREEN_SCROLL):
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + self.speed, self.width, self.height):
                self.speed = 0
        self.rect.y += self.speed
        self.rect.x += SCREEN_SCROLL

        if self.speed == 0:
            grenade_fx.play()
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5, 0)
            explosion_group.add(explosion)
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
