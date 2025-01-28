from image import *

def draw_text(text, font, text_col):
    img = font.render(text, True, text_col)
    return img


class Message(pygame.sprite.Sprite):
    def __init__(self, count, x, y):
        super().__init__()
        self.image = draw_text(f'+{count}', pygame.font.SysFont('consolas', 20),'yellow')
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.update_time = pygame.time.get_ticks()
        self.time = 50

    def update(self):
        self.time -= 1
        screen.blit(self.image, self.rect.center)
        if self.time == 0:
            self.kill()

