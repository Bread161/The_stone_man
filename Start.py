import pygame

image_path = '/data/data/com.poliakov.gamestone/files/app/'
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Pygame project')
icon = pygame.image.load(image_path + 'images/Gameicon.png')
pygame.display.set_icon(icon)

#Player
background = pygame.image.load(image_path + 'images/background2.jpg')

walk_left = [
pygame.image.load(image_path + 'images/player_left/player_left1.png'),
pygame.image.load(image_path + 'images/player_left/player_left2.png'),
pygame.image.load(image_path + 'images/player_left/player_left3.png'),
pygame.image.load(image_path + 'images/player_left/player_left4.png')
]
walk_right = [
pygame.image.load(image_path + 'images/player_right/player_right1.png'),
pygame.image.load(image_path + 'images/player_right/player_right2.png'),
pygame.image.load(image_path + 'images/player_right/player_right3.png'),
pygame.image.load(image_path + 'images/player_right/player_right4.png')
]

enemy = pygame.image.load(image_path + 'images/enemy.png')
enemy_list_in_game = []

player_anim_count = 0
background_x = 0

player_speed = 6
player_x = 150
player_y = 530

is_jump = False
jump_count = 8

background_sound = pygame.mixer.Sound(image_path + 'sounds/sound_walk.mp3')
background_sound.play()

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 5000)

label = pygame.font.Font(image_path + 'fonts/JosefinSans-Italic.ttf', 100)
lose_label = label.render("Ooops, You lose!", False, (5, 5, 5))
restart_label = label.render("Play again", False, (247, 134, 12))
restart_label_rect = restart_label.get_rect(topleft=(400, 550))

pebbles_left = 5
pebble = pygame.image.load(image_path + 'images/pebble.png')
pebbles = []

gameplay = True

running = True
while running:


    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + 1280, 0))

    if gameplay:


        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if enemy_list_in_game:
            for (i, el) in enumerate(enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 10

                if el.x < -10:
                    enemy_list_in_game.pop(i)
                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))


        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 500:
            player_x += player_speed


        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                    background_sound.stop()
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8
                background_sound.play()


        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        background_x -= 2
        if background_x == -1280:
            background_x = 0


        if pebbles:
            for (i,el) in enumerate(pebbles):
                screen.blit(pebble, (el.x, el.y))
                el.x += 6

                if el.x > 1280:
                    pebbles.pop(i)
                if enemy_list_in_game:
                    for (index, enemy_el) in enumerate(enemy_list_in_game):
                        if el.colliderect(enemy_el):
                            enemy_list_in_game.pop(index)
                            pebbles.pop(i)

    else:
        screen.fill((8, 46, 27))
        screen.blit(lose_label, (300, 300))
        background_sound.stop()
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            enemy_list_in_game.clear()
            pebbles.clear()
            background_sound.play()
            pebbles_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(1290, 550)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_TAB and pebbles_left > 0:
            pebbles.append(pebble.get_rect(topleft=(player_x + 30, player_y + 10)))
            pebbles_left -= 1
    clock.tick(8)

    pygame.display.update()
