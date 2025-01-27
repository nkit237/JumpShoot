import time
import button
import csv
import sqlite3
from granade import *
from fade import *
from world import *
from splashes import *

font = pygame.font.SysFont('consolas', 20)
font1 = pygame.font.SysFont('consolas', 65)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill('black')
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height()))


def create_particles(position):
    particle_count = random.randint(8, 30)
    numbers_x = range(-4, 5)
    numbers_y = range(-6, 1)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers_x), random.choice(numbers_y))


splashes_pos = [(113, 274), (387, 331), (752, 233), (1089, 227),
                (1489, 274), (1763, 331), (2128, 233), (2465, 227),
                (2865, 274), (3139, 331), (3504, 233), (3841, 227)]

moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False
SCREEN_SCROLL = 0
start_game = False
start_intro = False
pause = False
menu = False
info = False
kill_point = 0
bonus_point = 0
bird_point = 0
final_menu = False
splashes_cooldown = 0


def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    bird_group.empty()

    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)

intro_fade = ScreenFade(1, 'black', 8)
death_fade = ScreenFade(2, '#660000', 6)

start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 200, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 45, restart_img, 1)
Governance_and_rules_button = button.Button(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2, Governance_and_rules_img, 1)
back_button = button.Button(0, 0, back_img, 2)
main_menu_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT - 250, main_menu_img, 1)

clock = pygame.time.Clock()
FPS = 60
PLAY = True
TIMER = -1
SUM_TIMER = 0

while PLAY:
    clock.tick(FPS)
    if TIMER != -1 and not pause and level <= 3:
        time1 = time.strftime("%H:%M:%S").split(':')
        TIMER_NOW = int(time1[0]) * 360 + int(time1[1]) * 60 + int(time1[2])
        TIMER = TIMER_NOW - TIMER_START

    for pos in splashes_pos:
        if splashes_cooldown == 0:
            x, y = pos
            create_particles((x - bg_scroll * 0.6, y))
            splashes_cooldown = random.randint(20, 100)
        splashes_cooldown -= 1

    if info:
        screen.fill('black')
        screen.blit(Governance, (0, 0))
        if back_button.draw(screen):
            info = False
    elif final_menu:
        screen.fill('darkred')
        h = str(SUM_TIMER + TIMER // 360).zfill(2)
        m = str((SUM_TIMER + TIMER // 60) % 60).zfill(2)
        s = str(SUM_TIMER + TIMER % 360).zfill(2)
        t1 = f'За поражённых  противников вы набрали {kill_point} очков!'
        t2 = f'За поражённых птиц вы набрали {bird_point} очков!'
        t3 = f'За сбор бонусов вы набрали {bonus_point} очков!'
        t4 = f'Затраченное время: {h}.{m}.{s}'
        draw_text('ПОЗДРАВЛЯЕМ!', font, 'black', SCREEN_WIDTH * 0.4375, 80)
        draw_text('ВЫ ВЫИГРАЛИ!', font, 'black', SCREEN_WIDTH * 0.4375, 100)
        draw_text(t1, font, 'black', SCREEN_WIDTH * 0.25, 120)
        draw_text(t2, font, 'black', SCREEN_WIDTH * 0.25, 140)
        draw_text(t3, font, 'black', SCREEN_WIDTH * 0.25, 160)
        draw_text(t4, font, 'black', SCREEN_WIDTH * 0.25, 180)
        draw_text(f'Общий счёт: {kill_point + bonus_point + bird_point}', font, 'black', SCREEN_WIDTH * 0.25, 200)

        conn = sqlite3.connect('statistics.db')
        cursor = conn.cursor()
        cursor.execute("SELECT enemy, bird, bonus, time, checks FROM statistics")
        st = cursor.fetchall()[0]
        stat_p_enemy, stat_p_bird, stat_p_bonus, stat_time, stat_checks = st[0], st[1], st[2], st[3], st[4]
        cursor.execute("DELETE FROM statistics")
        stat_p_enemy = str(max(int(stat_p_enemy), kill_point))
        stat_p_bird = str(max(int(stat_p_bird), bird_point))
        stat_p_bonus = str(max(int(stat_p_bonus), bonus_point))
        stat_time = str(min(int(stat_time), SUM_TIMER + TIMER))
        stat_checks = str(max(int(stat_checks), kill_point + bird_point + bonus_point))
        cursor.execute("INSERT INTO statistics (enemy, bird, bonus, time, checks) VALUES (?, ?, ?, ?, ?)",
                       (stat_p_enemy, stat_p_bird, stat_p_bonus, stat_time, stat_checks))
        conn.commit()

        h = str(int(stat_time) // 360).zfill(2)
        m = str((int(stat_time) // 60) % 60).zfill(2)
        s = str(int(stat_time) % 360).zfill(2)
        t1 = f'За поражённых  противников вы набрали {stat_p_enemy} очков!'
        t2 = f'За поражённых птиц вы набрали {stat_p_bird} очков!'
        t3 = f'За сбор бонусов вы набрали {stat_p_bonus} очков!'
        t4 = f'Затраченное время: {h}.{m}.{s}'
        draw_text('Лучшие результаты:', font, 'black', SCREEN_WIDTH * 0.4, 240)
        draw_text(t1, font, 'black', SCREEN_WIDTH * 0.25, 260)
        draw_text(t2, font, 'black', SCREEN_WIDTH * 0.25, 280)
        draw_text(t3, font, 'black', SCREEN_WIDTH * 0.25, 300)
        draw_text(t4, font, 'black', SCREEN_WIDTH * 0.25, 320)
        draw_text(f'Общий счёт: {stat_checks}', font, 'black', SCREEN_WIDTH * 0.25, 340)
        if main_menu_button.draw(screen):
            kill_point = 0
            bonus_point = 0
            bird_point = 0
            final_menu = False
            menu = False
            pause = False
            level = 1
            death_fade.fade_counter = 0
            start_intro = True
            bg_scroll = 0

            with open(f'level{level}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            world = World()
            player, health_bar = world.process_data(world_data)
            start_game = False
        if exit_button.draw(screen):
            PLAY = False

    elif not start_game:
        screen.fill('darkred')
        draw_text('JumpShoot', font1, 'black', SCREEN_WIDTH * 0.34, 50)
        if start_button.draw(screen):
            time1 = time.strftime("%H:%M:%S").split(':')
            TIMER_START = int(time1[0]) * 360 + int(time1[1]) * 60 + int(time1[2])
            TIMER = 0
            SUM_TIMER = 0
            start_game = True
            start_intro = True
        if Governance_and_rules_button.draw(screen):
            info = True
        if exit_button.draw(screen):
            PLAY = False

    elif pause:
        if menu:
            screen.fill('darkred')
            draw_text('Меню', font1, 'black', SCREEN_WIDTH * 0.427, 50)
            if restart_button.draw(screen):
                time1 = time.strftime("%H:%M:%S").split(':')
                TIMER_START = int(time1[0]) * 360 + int(time1[1]) * 60 + int(time1[2])
                TIMER = 0
                SUM_TIMER = 0
                kill_point = 0
                bonus_point = 0
                bird_point = 0
                menu = False
                pause = False
                level = 1
                death_fade.fade_counter = 0
                start_intro = True
                bg_scroll = 0
                world_data = reset_level()

                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, health_bar = world.process_data(world_data)
            if exit_button.draw(screen):
                PLAY = False
            if start_button.draw(screen):
                time1 = time.strftime("%H:%M:%S").split(':')
                TIMER_START = int(time1[0]) * 360 + int(time1[1]) * 60 + int(time1[2])
                TIMER = 0
                SUM_TIMER = 0
                menu = False
                pause = False
            if Governance_and_rules_button.draw(screen):
                info = True
            if main_menu_button.draw(screen):
                kill_point = 0
                bonus_point = 0
                bird_point = 0
                menu = False
                pause = False
                level = 1
                death_fade.fade_counter = 0
                start_intro = True
                bg_scroll = 0
                world_data = reset_level()

                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, health_bar = world.process_data(world_data)
                start_game = False

    else:
        draw_bg()

        splashes_group.update(SCREEN_SCROLL)
        splashes_group.draw(screen)

        world.draw(SCREEN_SCROLL)

        draw_text('Здоровье: ', font, 'white', 10, 10)

        draw_text('Пули: ', font, 'white', 10, 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + (x * 10), 40))

        draw_text('Гранаты: ', font, 'white', 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 60))

        player.update()
        player.draw(screen)

        health_bar.draw(player.health, screen)

        for enemy in enemy_group:
            enemy.ai(player, world, SCREEN_SCROLL)
            kill_point += enemy.update()
            enemy.draw(screen)

        bullet_group.update(player, world, SCREEN_SCROLL)
        bullet_group.draw(screen)

        grenade_group.update(player, world, SCREEN_SCROLL)
        grenade_group.draw(screen)

        explosion_group.update(SCREEN_SCROLL)
        explosion_group.draw(screen)

        for i in item_box_group:
            bonus_point += i.update(player, SCREEN_SCROLL)
        item_box_group.draw(screen)

        decoration_group.update(SCREEN_SCROLL)
        decoration_group.draw(screen)

        water_group.update(SCREEN_SCROLL)
        water_group.draw(screen)

        exit_group.update(SCREEN_SCROLL)
        exit_group.draw(screen)

        for bird in bird_group:
            bird_point += bird.update_animation(player)
            bird.move(SCREEN_SCROLL, player)
            bird.draw(screen)

        if start_intro:
            if intro_fade.fade(screen):
                start_intro = False
                intro_fade.fade_counter = 0

        if player.alive:
            if shoot:
                player.shoot()
            elif grenade and not grenade_thrown and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
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
            SCREEN_SCROLL, level_complete = player.move(moving_left, moving_right, world, bg_scroll)
            bg_scroll -= SCREEN_SCROLL

            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    SUM_TIMER += TIMER

                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
                else:
                    final_menu = True

        else:
            screen_scroll = 0
            if death_fade.fade(screen):
                draw_text('Вы проиграли!!!', font1, 'black', SCREEN_WIDTH * 0.24, 100)
                if main_menu_button.draw(screen):
                    kill_point = 0
                    bonus_point = 0
                    bird_point = 0
                    menu = False
                    pause = False
                    level = 1
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()

                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
                    start_game = False
                if exit_button.draw(screen):
                    PLAY = False
                if restart_button.draw(screen):
                    time1 = time.strftime("%H:%M:%S").split(':')
                    TIMER_START = int(time1[0]) * 360 + int(time1[1]) * 60 + int(time1[2])
                    TIMER = 0
                    SUM_TIMER = 0
                    kill_point = 0
                    bonus_point = 0
                    bird_point = 0
                    level = 1
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()

                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            PLAY = False
        if event.type == pygame.KEYDOWN:
            if player.alive and start_game:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w:
                    player.jump = True
                    jump_fx.play()
                if event.key == pygame.K_SPACE:
                    shoot = True
                if event.key == pygame.K_q:
                    grenade = True
            if event.key == pygame.K_ESCAPE:
                if start_game:
                    pause = True
                    menu = True
            if event.key == pygame.K_p:
                if start_game:
                    pause = not pause

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
