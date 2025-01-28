from create_pers import *
from explosion import *
from image import *


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        super().__init__()
        self.health = 100
        self.speed = speed
        self.cooldown = 0
        self.flip = False
        self.alive = True
        self.direction = 1
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(9):
            img = pygame.image.load(f'data/img/bird/fly/{i}.png')
            img = img.convert()
            img.set_colorkey((255, 255, 255))
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self, player):
        alife = self.alive
        self.check_alive(player)
        if alife != self.alive and not self.alive:
            return 50
        else:
            ANIMATION_COOLDOWN = 100
            self.image = self.animation_list[self.frame_index]
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
            return 0

    def move(self, scrol, player):
        if player.alive and self.rect.colliderect(player.rect) and self.cooldown == 0:
            player.health -= 5
            self.cooldown = 20
        if self.cooldown > 0:
            self.cooldown -= 1
        dx = 0
        if self.direction == -1:
            dx = -self.speed
            if ((self.rect.centerx + dx) - player.rect.centerx) < -2000:
                dx *= -1
                self.direction *= -1
            else:
                self.flip = True
        elif self.direction == 1:
            dx = self.speed
            if ((self.rect.centerx + dx) - player.rect.centerx) > 2000:
                dx *= -1
                self.direction *= -1
            else:
                self.flip = False

        self.rect.x += dx + scrol

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def check_alive(self, player):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            grenade_fx.play()
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2, 1)
            explosion_group.add(explosion)
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50


def bombs(self, player):
    if player.rect.midtop[1] == self.rect.y:
        pass
