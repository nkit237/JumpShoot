from soldier import *
from settings import *

clock = pygame.time.Clock()
FPS = 60

moving_left = False
moving_right = False
shoot = False

BG = (255, 255, 255)
RED = (255, 0, 0)


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 500), (SCREEN_WIDTH, 500))


player = Soldier('player', 200, 200, 3, 5, 20)
player_group.add(player)
enemy = Soldier('enemy', 400, 200, 3, 5, 20)
enemy_group.add(enemy)

run = True
while run:

    clock.tick(FPS)

    draw_bg()

    player.update()
    player.draw()

    enemy.update()
    enemy.draw()

    bullet_group.update()
    bullet_group.draw(screen)

    if player.alive:
        if shoot:
            player.shoot()
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

    pygame.display.update()

pygame.quit()
