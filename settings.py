import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

bullet_img = pygame.image.load('data/img/icons/bullet.png').convert()
bullet_img.set_colorkey((255, 255, 255))
grenade_img = pygame.image.load('data/img/icons/grenade.png').convert()
grenade_img.set_colorkey((255, 255, 255))
health_box_img = pygame.image.load('data/img/icons/health_box.png').convert()
health_box_img.set_colorkey((255, 255, 255))
ammo_box_img = pygame.image.load('data/img/icons/ammo_box.png').convert()
ammo_box_img.set_colorkey((255, 255, 255))
grenade_box_img = pygame.image.load('data/img/icons/grenade_box.png').convert()
grenade_box_img.set_colorkey((255, 255, 255))
bonus_box_img = pygame.image.load('data/img/icons/bonus_box.png').convert()
bonus_box_img.set_colorkey((255, 255, 255))
item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img,
    'Bonus': bonus_box_img
}

GRAVITY = 0.75
TILE_SIZE = 40

bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
