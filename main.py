import os
import sys
import numpy as np
import pygame

from sprites import Obstacle, Player


FPS = 60


def display_score() -> int:
    score = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = game_fnt.render(f"Score: {score}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return score


def collision_check() -> bool:
    if len(pygame.sprite.spritecollide(player.sprite, obstacle, False)):
        obstacle.empty()
        return False
    return True


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Simple Runner")
    clock = pygame.time.Clock()

    game_fnt = pygame.font.Font("./font/Pixeltype.ttf", 50)
    game_active = False
    start_time = 0
    score = 0
    h_score = 0
    if os.path.exists("./h_score"):
        with open("./h_score", "rb") as fp:
            h_score = int.from_bytes(fp.read())

    sky_surf = pygame.image.load("./graphics/sky.png").convert_alpha()
    ground_surf = pygame.image.load("./graphics/ground.png").convert_alpha()

    # Intro and score screen
    player_stand_surf = pygame.image.load(
        "./graphics/player/player_stand.png"
    ).convert_alpha()
    player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
    player_stand_rect = player_stand_surf.get_rect(center=(400, 200))

    game_name = game_fnt.render("Simple Runner", False, (111, 196, 169))
    game_name_rect = game_name.get_rect(center=(400, 80))

    game_message = game_fnt.render("Press space to run", False, (111, 196, 169))
    game_message_rect = game_message.get_rect(center=(400, 330))

    # Player sprite

    player = pygame.sprite.GroupSingle()
    player.add(Player())

    # Obstacle sprite
    obstacle = pygame.sprite.Group()

    # Obstacle Timer
    obs_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obs_timer, 1500)

    # BG Music
    bg_music = pygame.mixer.Sound("./audio/music.wav")
    bg_music.set_volume(0.7)
    bg_music.play(loops=-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_active:
                if event.type == obs_timer:
                    choice = np.random.choice(["fly", "snail"], p=[0.2, 0.8])
                    obstacle.add(Obstacle(str(choice)))
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
                    player.update(reset_x=True)

        if game_active:

            screen.blit(sky_surf, (0, 0))
            screen.blit(ground_surf, (0, 300))
            score = display_score()

            player.draw(screen)
            player.update()

            obstacle.draw(screen)
            obstacle.update(score)

            game_active = collision_check()

        else:
            screen.fill((94, 129, 162))
            screen.blit(game_name, game_name_rect)
            screen.blit(player_stand_surf, player_stand_rect)

            if score != 0:
                score_message = game_fnt.render(
                    f"Your Score: {score}", False, (111, 196, 169)
                )
                score_msg_rect = score_message.get_rect(center=(400, 330))
                screen.blit(score_message, score_msg_rect)
                h_score_message = game_fnt.render(
                    f"High Score: {h_score}", False, (229, 13, 0)
                )
                h_score_message_rect = h_score_message.get_rect(center=(400, 370))
                screen.blit(h_score_message, h_score_message_rect)

                if score > h_score:
                    with open("./h_score", "wb") as fp:
                        fp.write(score.to_bytes())
                    h_score = score

            else:
                screen.blit(game_message, game_message_rect)

        pygame.display.update()
        clock.tick(FPS)
