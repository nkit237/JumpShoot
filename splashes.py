import random
from image import *
from create_pers import *

screen_rect = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [splashes_img]
    for scale in (5, 10, 15):   # 5, 10, 20
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(splashes_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx // 1.5, dy * 8]
        # и свои координаты
        self.rect.x, self.rect.y = pos
        self.pos = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0] // 2
        self.rect.y += self.velocity[1] // 8
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect) or self.rect.y > self.pos[1] + random.randint(10, 300):
            self.kill()
