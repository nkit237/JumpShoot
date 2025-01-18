from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.speed = 50
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        for player in player_group:
            if pygame.sprite.spritecollide(player, bullet_group, False):
                if player.alive:
                    player.health -= 5
                    self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()
