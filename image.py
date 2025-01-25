import pygame
from pygame import mixer
from settings import *

mixer.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('JumpShoot')

jump_fx = pygame.mixer.Sound('data/audio/jump.wav')
jump_fx.set_volume(1.05)
shot_fx = pygame.mixer.Sound('data/audio/shot.wav')
shot_fx.set_volume(1.05)
grenade_fx = pygame.mixer.Sound('data/audio/grenade.wav')
grenade_fx.set_volume(1.05)

health_box_img = pygame.image.load('data/img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('data/img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('data/img/icons/grenade_box.png').convert_alpha()
bonus_box_img = pygame.image.load('data/img/icons/bonus_box.png').convert_alpha()
grenade_img = pygame.image.load('data/img/icons/grenade.png').convert()
grenade_img.set_colorkey((255, 255, 255))
bullet_img = pygame.image.load('data/img/icons/bullet.png').convert()
bullet_img.set_colorkey((255, 255, 255))

bk1_img = pygame.image.load('data/img/Background/bk1.png').convert()
bk1_img.set_colorkey((255, 255, 255))
bk2_img = pygame.image.load('data/img/Background/bk2.png').convert()
bk2_img.set_colorkey((255, 255, 255))
mountain_img = pygame.image.load('data/img/Background/mountain.png').convert()
mountain_img.set_colorkey((255, 255, 255))
sky_img = pygame.image.load('data/img/Background/sky_cloud.png').convert_alpha()
splashes_img = pygame.image.load('data/img/Background/splashes.png').convert()
splashes_img.set_colorkey((255, 255, 255))
splashes_img = pygame.transform.scale(splashes_img, (5, 5))

start_img = pygame.image.load('data/img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('data/img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('data/img/restart_btn.png').convert_alpha()
Governance_and_rules_img = pygame.image.load('data/img/Governance_and_rules_img.jpg').convert_alpha()
back_img = pygame.image.load('data/img/back.jpg').convert_alpha()

main_menu_img = pygame.image.load('data/img/main_menu.jpg').convert_alpha()

Governance = pygame.image.load('data/img/info/G_R.jpg').convert_alpha()
Governance = pygame.transform.scale(Governance, (SCREEN_WIDTH, SCREEN_HEIGHT))

img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'data/img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img.set_colorkey((255, 255, 255))
    img_list.append(img)

item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img,
    'Bonus': bonus_box_img
}
