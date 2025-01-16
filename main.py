from soldier import *
from grenade import *
from items import *
from interface import *

clock = pygame.time.Clock()
FPS = 60

moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

BG = (255, 255, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont('Futura', 30)


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def draw_bg():
	screen.fill(BG)
	pygame.draw.line(screen, RED, (0, 500), (SCREEN_WIDTH, 500))


player = Soldier('player', 200, 200, 3, 5, 20, 5)
player_group.add(player)
enemy = Soldier('enemy', 400, 200, 3, 5, 20, 0)
enemy_group.add(enemy)
enemy2 = Soldier('enemy', 300, 400, 3, 5, 20, 0)
enemy_group.add(enemy2)

item_box = ItemBox('Health', 100, 460)
item_box_group.add(item_box)
item_box = ItemBox('Ammo', 400, 460)
item_box_group.add(item_box)
item_box = ItemBox('Grenade', 500, 460)
item_box_group.add(item_box)

health_bar = HealthBar(10, 10, player.health, player.health)

run = True
while run:

	clock.tick(FPS)

	draw_bg()

	health_bar.draw(player.health, screen)
	draw_text('Пули: ', font, WHITE, 10, 35)
	for x in range(player.ammo):
		screen.blit(bullet_img, (90 + (x * 10), 40))
	draw_text('Гранаты: ', font, WHITE, 10, 60)
	for x in range(player.grenades):
		screen.blit(grenade_img, (135 + (x * 15), 60))

	player.update()
	player.draw()

	for enemy in enemy_group:
		enemy.update()
		enemy.draw()

	bullet_group.update()
	bullet_group.draw(screen)

	grenade_group.update()
	grenade_group.draw(screen)

	explosion_group.update()
	explosion_group.draw(screen)

	item_box_group.update()
	item_box_group.draw(screen)

	if player.alive:
		if shoot:
			player.shoot()
		elif grenade and grenade_thrown == False and player.grenades > 0:
			grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
						player.rect.top, player.direction)
			grenade_group.add(grenade)
			player.grenades -= 1
			grenade_thrown = True
		if player.in_air:
			player.update_action(2)
		elif moving_left or moving_right:
			player.update_action(1)
		else:
			player.update_action(0)
		player.move(moving_left, moving_right)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_q:
				grenade = True
			if event.key == pygame.K_w and player.alive:
				player.jump = True
			if event.key == pygame.K_ESCAPE:
				run = False

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_d:
				moving_right = False
			if event.key == pygame.K_SPACE:
				shoot = False
			if event.key == pygame.K_q:
				grenade = False
				grenade_thrown = False

	pygame.display.update()

pygame.quit()
