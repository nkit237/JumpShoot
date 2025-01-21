import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, type):
        super().__init__()
        self.images = []
        if type == 0:
            for num in range(1, 6):
                img = pygame.image.load(f'data/img/explosion/exp{num}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.images.append(img)
        elif type == 1:
            for num in range(0, 7):
                img = pygame.image.load(f'data/img/explosion_bird/{num}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self, SCREEN_SCROLL):
        self.rect.x += SCREEN_SCROLL

        EXPLOSION_SPEED = 4
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]
