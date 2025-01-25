import random
from image import *
from create_pers import *

screen_rect = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


class Particle(pygame.sprite.Sprite):
    fire = [splashes_img]
    for scale in (5, 10, 15):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(splashes_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx // 1.5, dy * 8]
        self.rect.x, self.rect.y = pos
        self.pos = pos

        self.gravity = GRAVITY

    def update(self, SCREEN_SCROLL):
        self.velocity[1] += self.gravity
        self.rect.x += (self.velocity[0] // 2) + SCREEN_SCROLL * 0.6
        self.rect.y += self.velocity[1] // 8
        if not self.rect.colliderect(screen_rect) or self.rect.y > self.pos[1] + random.randint(10, SCREEN_HEIGHT):
            self.kill()
