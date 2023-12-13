import pygame
import sys
import time
from settings import *
from tools import BG, Ground, Plane, Obstacle
from random import choice, randint
import os

class Hikgame:
    def __init__(self):
        pygame.init()

        # Print the current working directory for debugging
        #print("Current working directory:", os.getcwd())

        # Display setup
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Hiko Bird')

        # Clock for controlling the frame rate
        self.clock = pygame.time.Clock()

        # Game state
        self.active = True

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.hit_stuff = pygame.sprite.Group()

        # Scale factor
        bg_height = pygame.image.load('pics/bridge/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # Sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.hit_stuff], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)

        # Timer for spawning obstacles
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # Font and score
        self.font = pygame.font.Font('pics/font/style.ttf', 30)
        self.score = 0
        self.start_offset = 0

        # Menu setup
        self.menu_surf = pygame.image.load('pics/lastpic/lastpic.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Music setup
        self.music = pygame.mixer.Sound('voice/music.wav')
        self.music.play(loops=-1)
        self.music.set_volume(0.05)

        # Sound setup
        self.plane.son.set_volume(9.0)

    def hit(self):
        if pygame.sprite.spritecollide(self.plane, self.hit_stuff, False, pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
            # Stop background music
            pygame.mixer.music.stop()

            # Play collision sound when an obstacle is hit
            self.plane.son.play()

            for sprite in self.hit_stuff.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()

            self.active = False
            self.plane.kill()

            # Resume background music
            pygame.mixer.music.unpause()

    def score_screen(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:
            # Delta time
            dt = time.time() - last_time
            last_time = time.time()

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.hit_stuff], self.scale_factor * 1.1)

            # Game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.score_screen()

            if self.active:
                self.hit()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    hikgame = Hikgame()
    hikgame.run()
