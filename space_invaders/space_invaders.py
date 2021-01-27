import pygame
from pygame import *
import sys
import random
import time


# Initialize Pygame
pygame.init()

# variables
width = 750
height = 750
red = (255, 0, 0)
green = (255, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

# initialize window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invader")

# loading the images
opening = pygame.image.load("images/space.png")

# resizing images
opening = pygame.transform.scale(opening, (width, height + 10))

# load enemy space ship image
enemy_space_ship = pygame.image.load("images/ufo.png")


# load player space ship image
player_space_ship = pygame.image.load("images/yellow_player.png")

# load laser image
green_laser = pygame.image.load("images/green_laser.png")
yellow_laser = pygame.image.load("images/yellow_laser.png")

# load background image
BG = pygame.transform.scale(pygame.image.load("images/background.png"), (width, height))

# load sound / music
mixer.music.load("sounds/background.wav")
mixer.music.play(-1)


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(height >= self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    countdown = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cool_down()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
                explosion_sound = mixer.Sound("sounds/explosion.wav")
                pygame.mixer.Sound.set_volume(explosion_sound, 0.1)
                explosion_sound.play()

    def cool_down(self):
        if self.cool_down_counter >= self.countdown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = player_space_ship
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cool_down()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            explosion_sound = mixer.Sound("sounds/explosion.wav")
                            pygame.mixer.Sound.set_volume(explosion_sound, 0.1)
                            explosion_sound.play()

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
                "green": (enemy_space_ship, green_laser),
                }

    def __init__(self, x, y, colors, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[colors]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("roman", 50)
    lost_font = pygame.font.SysFont("roman", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        screen.blit(BG, (0, 0))
        lives_label = main_font.render(f"Lives: {lives}", True, yellow)
        level_label = main_font.render(f"Level: {level}", True, yellow)

        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (width - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(screen)

        player.draw(screen)

        if lost:
            lost_label = lost_font.render("You Lost!!", True, yellow)
            screen.blit(lost_label, (width / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, width - 100), random.randrange(-1500, -100),
                              random.choice(["green"]))
                enemies.append(enemy)

        for EVENT in pygame.event.get():
            if EVENT.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < width:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < height:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
            laser_sound = mixer.Sound("sounds/laser.wav")
            pygame.mixer.Sound.set_volume(laser_sound, 0.1)
            laser_sound.play()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
                explosion_sound = mixer.Sound("sounds/explosion.wav")
                pygame.mixer.Sound.set_volume(explosion_sound, 0.1)
                explosion_sound.play()
            elif enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)


def reset():
    global won, run
    time.sleep(3)
    won = False
    run = True


def game_open():
    screen.blit(opening, (0, 0))
    pygame.display.update()
    time.sleep(3)


def main_menu():
    game_open()
    title_font = pygame.font.SysFont("roman" "bold", 75)
    title_font1 = pygame.font.SysFont("roman" "bold", 75)
    title_font2 = pygame.font.SysFont("aerial" "bold", 75)
    title_font3 = pygame.font.SysFont("aerial" "bold", 75)
    run = True
    while run:
        screen.blit(BG, (0, 0))
        message = "Space Bar ... Player Shoot"
        message1 = "Arrows ... Moves Player"
        message2 = "Click Mouse Button"
        message3 = "To Play Space Invader"
        title_label = title_font.render(message, True, white)
        title_label1 = title_font1.render(message1, True, white)
        title_label2 = title_font2.render(message2, True, red)
        title_label3 = title_font3.render(message3, True, red)
        screen.blit(title_label, (width / 2 - title_label.get_width() / 2, 500))
        screen.blit(title_label1, (width / 2 - title_label.get_width() / 2, 400))
        screen.blit(title_label2, (width / 2 - title_label.get_width() / 2, 100))
        screen.blit(title_label3, (width / 2 - title_label.get_width() / 2, 200))
        pygame.display.update()
        for EVENT in pygame.event.get():
            if EVENT.type == QUIT:
                run = False
                reset()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()
    sys.exit()


main_menu()
