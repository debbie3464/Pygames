from pathlib import Path
import random

import pygame as pg

pg.init()

ASSETS = Path(__file__).parent / "assets"

screen = pg.display.set_mode((631, 500))
pg.display.set_caption("When It Rains")

# Fonts
font = pg.font.SysFont("Arial", 48)

# Images
bg = pg.image.load(ASSETS / "bg.png")
platform = pg.image.load(ASSETS / "platform.png")
rain_drop_img = pg.image.load(ASSETS / "raindrop.png").convert_alpha()
rain_drop_mask = pg.mask.from_surface(rain_drop_img)

class Cloud:
    def __init__(self):
        self.cloud_1 = pg.image.load(ASSETS / "cloud_1.png")
        self.cloud_2 = pg.image.load(ASSETS / "cloud_2.png")
        self.cloud_3 = pg.image.load(ASSETS / "cloud_3.png")
        
        self.cloud_1_x = 600
        self.cloud_1_y = -100

        self.cloud_2_x = -500
        self.cloud_2_y = -50

        self.cloud_3_x = 400
        self.cloud_3_y = 0

    def draw_cloud(self):
        screen.blit(self.cloud_1, (self.cloud_1_x, self.cloud_1_y))
        screen.blit(self.cloud_2, (self.cloud_2_x, self.cloud_2_y))
        screen.blit(self.cloud_3, (self.cloud_3_x, self.cloud_3_y))

    def cloud_animation(self):
        self.cloud_1_x -= 0.8
        self.cloud_2_x += 0.8
        self.cloud_3_x -= 0.8

        if self.cloud_1_x <= -self.cloud_1.get_width():
            self.cloud_1_x = 620
        if self.cloud_2_x >= screen.get_width():
            self.cloud_2_x = -self.cloud_2.get_width()
        if self.cloud_3_x <= -self.cloud_3.get_width():
            self.cloud_3_x = 620

class Player:
    def __init__(self):
        self.cat = pg.image.load(ASSETS / "cat.png").convert_alpha()
        self.cat_mask = pg.mask.from_surface(self.cat)
        self.cat_x = 240
        self.cat_y = 350
        self.cat_speed = 5

    def draw_cat(self):
        screen.blit(self.cat, (self.cat_x, self.cat_y))

    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.cat_x -= self.cat_speed
        if keys[pg.K_RIGHT]:
            self.cat_x += self.cat_speed
        # keep the cat on screen
        self.cat_x = max(0, min(self.cat_x, screen.get_width() - self.cat.get_width()))

    def get_rect(self):
        return self.cat.get_rect(topleft=(self.cat_x, self.cat_y))

class Raindrop:
    def __init__(self, x, y):
        self.image = rain_drop_img
        self.mask = rain_drop_mask
        self.x = x
        self.y = y
        self.speed = 5

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))

def draw_game_over():
    text = font.render("Game Over", True, (255, 0, 0))
    subtext = pg.font.SysFont("Arial", 24).render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 180))
    screen.blit(subtext, (screen.get_width()//2 - subtext.get_width()//2, 240))

def reset_game():
    return Player(), [], 0, False

# Game setup
cloud = Cloud()
cat, raindrops, spawn_time, game_over = reset_game()
spawn_interval = 20

# Game loop
clock = pg.time.Clock()
run = True
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
        if game_over:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_r:
                    cat, raindrops, spawn_time, game_over = reset_game()
                elif e.key == pg.K_ESCAPE:
                    run = False

    if not game_over:
        spawn_time += 1
        if spawn_time >= spawn_interval:
            x = random.randint(0, 631 - rain_drop_img.get_width())
            raindrops.append(Raindrop(x, -20))
            spawn_time = 0

        cat.controls()
        for drop in raindrops:
            drop.move()

        cat_rect = cat.get_rect()
        for drop in raindrops:
            offset = (drop.get_rect().x - cat_rect.x, drop.get_rect().y - cat_rect.y)
            if cat.cat_mask.overlap(drop.mask, offset):
                game_over = True
                break

        raindrops = [drop for drop in raindrops if drop.y < screen.get_height()]

    # Drawing
    screen.blit(bg, (0, 0))
    cloud.draw_cloud()
    cloud.cloud_animation()
    screen.blit(platform, (0, 0))
    cat.draw_cat()
    for drop in raindrops:
        drop.draw()

    if game_over:
        draw_game_over()

    pg.display.flip()
    clock.tick(60)

pg.quit()
