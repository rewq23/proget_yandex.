import time

import pygame
import pygame as pg
import sys
import os

FPS = 25
size = WIDTH, HEIGHT = 900, 900
pygame.init()
screen = pygame.display.set_mode(size)

go_sound = pygame.mixer.Sound('Sound_038843_mp3cut.net.mp3')
zvuk_teleporta = pygame.mixer.Sound('jg-032316-sfx-time-machine-takeoff-7_mp3cut.net.mp3')

pygame.mixer.music.load('1579459482_undertale-megalovania-house-remix.mp3')
pygame.mixer.music.set_volume(0.09)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y, player_image, player_hitbox = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '-':
                Tile('background', x, y)
            elif level[y][x] == '=':
                Tile('water', x, y)
            elif level[y][x] == ',':
                Tile('rock', x, y)
            elif level[y][x] == "'":
                Tile('rock_B', x, y)
            elif level[y][x] == '>':
                Tile('exit', x, y)
            elif level[y][x] == '^':
                Tile('mobs', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                player_image = load_image('dino_front.png')
                new_player = Player(level, x, y, player_image)
    return new_player, x, y, player_image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["              История", "",
                  "              Вы динозав, который проснулся у себя в пещере",
                  "              и хочет проверить что произошло с наружи.",
                  "              Смысл игры",
                  "              Узнать что произошло пока спал динозавр.",
                  "              И встретиь много опасносей на своём пути.",
                  "              Удачного приключения!",
                  "              Приятной игры)"]

    fon = pygame.transform.scale(load_image('DdQvNbMW4AYCETw.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        pygame.mixer.music.play(-1, )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Mobs(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, all_sprites, bullets):
        super().__init__()
        shot_image = load_image('shot_up.png')
        self.image = mob_image
        self.x = pos_x
        self.y = pos_y
        pos = pos_y, pos_x
        self.all_sprites = all_sprites
        self.add(self.all_sprites)
        self.bullets = bullets
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 2, tile_height * pos_y)
        self.bullet_timer = 1

    def update(self, dt):
        self.rect.center = pg.mouse.get_pos()

        mouse_pressed = pg.mouse.get_pressed()
        self.bullet_timer -= dt
        if self.bullet_timer <= 0:
            self.bullet_timer = 1
            Bullet(pg.mouse.get_pos(), self.all_sprites, self.bullets)
            self.bullet_timer = .1

    def shot(self):
        shot = []
        spawn_counter = -1
        if spawn_counter <= 0:
            shot.append(mob_image.get_rect())
            spawn_counter = 30


class Player(pygame.sprite.Sprite):
    front_image = load_image('dino_front.png')
    down_image = load_image('dino_down.png')
    right_image = load_image('dino_right.png')
    left_image = load_image('dino_left.png')

    def __init__(self, level, pos_x, pos_y, player_image):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.x = pos_x
        self.y = pos_y
        self.level = level
        self.flag = True
        self.n = -1
        self.v = 'up'
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 2, tile_height * pos_y)

    def move(self, dx, dy):
        x = (self.x + dx) % len(self.level[0])
        y = (self.y + dy) % len(self.level)
        if self.level[y][x] == '>':
            if self.flag:
                pygame.mixer.Sound.play(zvuk_teleporta)
                self.n *= -1
                dx = -1
                dy = 49
                if y == 16:
                    dy = 45
                elif y == 17:
                    dy = 44
                elif y == 18:
                    dy = 44
                dy *= self.n
                x = (self.x + dx) % len(self.level[0])
                y = (self.y + dy) % len(self.level)
                self.x = x
                self.y = y
                self.rect.move_ip(dx * tile_width, dy * tile_height)
        if self.level[y][x] == '.' or self.level[y][x] == ',':
            self.x = x
            self.y = y
            self.rect.move_ip(dx * tile_width, dy * tile_height)

    def update(self, events):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            time.sleep(0.09)
            pygame.mixer.Sound.play(go_sound)
            self.move(0, -1)
            self.image = self.down_image
            self.v = 'up'
        if keystate[pygame.K_s]:
            time.sleep(0.09)
            pygame.mixer.Sound.play(go_sound)
            self.move(0, 1)
            self.image = self.front_image
            self.v = 'dowm'
        if keystate[pygame.K_a]:
            time.sleep(0.09)
            pygame.mixer.Sound.play(go_sound)
            self.move(-1, 0)
            self.image = self.left_image
            self.v = 'left'
        if keystate[pygame.K_d]:
            time.sleep(0.09)
            pygame.mixer.Sound.play(go_sound)
            self.move(1, 0)
            self.image = self.right_image
            self.v = 'right'
        events_s = pygame.event.get()
        for event in events_s:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    b = Bullet(self.v, self.rect.x + tile_width // 2, self.rect.y + tile_height // 2)
                    bullet_group.add(b)
                    all_sprites.add(b)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, v, x, y):
        super().__init__(all_sprites)
        self.image = shot_image['up']
        self.v = v
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.v == 'up':
            self.rect.y -= 5
        if self.v == 'down':
            self.rect.y += 5
            self.image = shot_image['down']
        if self.v == 'left':
            self.rect.x -= 5
            self.image = shot_image['left']
        if self.v == 'right':
            self.rect.x += 5
            self.image = shot_image['right']


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


if __name__ == '__main__':
    BACK_COLOR = pygame.Color('black')
    pygame.display.set_caption('Roguelike')
    clock = pygame.time.Clock()
    start_screen()
    tile_images = {
        'wall': load_image('stone_block.png'),
        'empty': load_image('stone_floor.png'),
        'background': load_image('background.png'),
        'water': load_image('water.png'),
        'rock': load_image('rock_1.png'),
        'rock_B': load_image('stone_B&F.png'),
        'exit': load_image('exit_1.png'),
        'mobs': load_image('mob.png')
    }
    tile_images_1 = {
        'wall': load_image('stone_block.png'),
        'empty': load_image('stone_floor.png'),
        'background': load_image('background.png'),
        'water': load_image('water.png'),
        'rock': load_image('rock_1.png'),
        'exit': load_image('exit_1.png')
    }
    tile_images_2 = {
        'wall': load_image('stone_block.png'),
        'empty': load_image('stone_floor.png'),
        'background': load_image('background.png'),
        'water': load_image('water.png'),
        'rock': load_image('rock_1.png'),
        'exit': load_image('exit_1.png')
    }
    tile_images_3 = {
        'wall': load_image('stone_block.png'),
        'empty': load_image('stone_floor.png'),
        'background': load_image('background.png'),
        'water': load_image('water.png'),
        'rock': load_image('rock_1.png'),
        'exit': load_image('exit_1.png')
    }
    exit_image = load_image('exit_1.png')
    mob_image = load_image('mob.png')
    shot_image = {'up': load_image('shot_up.png'),
                  'down': load_image('shot_down.png'),
                  'right': load_image('shot_right.png'),
                  'left': load_image('shot_left.png')
                  }
    tile_width = tile_height = 50  # 50
    exit = None
    all_sprites = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    player, level_x, level_y, player_image = generate_level(load_level('levelex_1.txt'))
    camera = Camera()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    pass

        player_group.update(events)
        camera.update(player)
        bullet_group.update()
        hits = pygame.sprite.groupcollide(tiles_group, bullet_group, True, True)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill(BACK_COLOR)
        tiles_group.draw(screen)
        player_group.draw(screen)
        bullet_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()
