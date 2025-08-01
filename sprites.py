import random
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk1 = pygame.image.load(
            "./graphics/player/player_walk_1.png"
        ).convert_alpha()
        player_walk2 = pygame.image.load(
            "./graphics/player/player_walk_2.png"
        ).convert_alpha()

        self._player_walk = [player_walk1, player_walk2]
        self._idx = 0

        self._player_jump = pygame.image.load(
            "./graphics/player/jump.png"
        ).convert_alpha()

        self.image = self._player_walk[self._idx]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self._gravity = 0
        self._jump_snd = pygame.mixer.Sound("./audio/jump.mp3")
        self._jump_snd.set_volume(0.5)

    def __player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self._gravity = -20
            self._jump_snd.play()

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right <= 800:
            self.rect.x += 4

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left >= 10:
            self.rect.x -= 4

    def __apply_gravity(self):
        self._gravity += 1
        self.rect.y += self._gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def __animate(self):
        if self.rect.bottom < 300:
            self.image = self._player_jump
        else:
            self._idx += 0.1
            if self._idx >= len(self._player_walk):
                self._idx = 0
            self.image = self._player_walk[int(self._idx)]

    def update(self, reset_x: bool = False):
        if reset_x:
            self.rect.x = 80

        self.__player_input()
        self.__apply_gravity()
        self.__animate()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obs_type: str):
        super().__init__()
        assert obs_type in [
            "fly",
            "snail",
        ], f"Expected obs_type to be either fly/snail. Found {obs_type}"

        self._obs_type = obs_type
        self._frames = []
        x_pos = random.randint(900, 1100)
        y_pos = 0
        if obs_type == "snail":
            snail_1 = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("./graphics/snail/snail2.png").convert_alpha()
            self._frames = [snail_1, snail_2]
            y_pos = 300

        else:
            fly_1 = pygame.image.load("./graphics/fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("./graphics/fly/fly2.png").convert_alpha()
            self._frames = [fly_1, fly_2]
            y_pos = 210

        self._idx = 0
        self.image = self._frames[self._idx]
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))

    def __animate(self):
        self._idx += 0.1
        if self._idx >= len(self._frames):
            self._idx = 0
        self.image = self._frames[int(self._idx)]

    def __move(self, speed: int = 6):
        self.rect.x -= speed

    def __destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self, score: int):
        speed = 6
        if score > 100:
            speed = 10
        self.__animate()
        self.__move(speed)
        self.__destroy()
