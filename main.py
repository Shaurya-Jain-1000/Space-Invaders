import time
import json
import pygame
import random
from pygame import mixer
# Initialize the pygame
pre_data = {
    'highscore': 0,
    'money': 0,
    'pistol_speed': 0,
    'pistol_damage':0,
    'shotgun_speed': 0,
}

try:
    with open('data.txt', 'r') as datafile:
        data = json.load(datafile)
        print(data)
except:
    with open('data.txt', 'w') as datafile:
        json.dump(pre_data, datafile)
    with open('data.txt', 'r') as datafile:
        data = json.load(datafile)
        print(data)

pygame.init()


#score
score = 0
highscore = data['highscore']
money = data['money']
gun = 'pistol'

# The Font
myfont = pygame.font.SysFont('Garamond', 50, 'White')
score_font = pygame.font.SysFont('Garamond', 30, 'Black')

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)
enemy_die_sound = mixer.Sound('explosion.wav')
bullet_sound = mixer.Sound('laser.wav')

# Loading sounds
purchase_sound = mixer.Sound('purchase.wav')

# The game starts on menu screen
screen = 'menu'

fire = False

# Loading Images
icon_img = pygame.image.load('icon.png')
bg_img = pygame.image.load('bg.jpg')
play_img = pygame.image.load('play_btn.png')
player_img = pygame.image.load('spaceship.png')
enemy_img = pygame.image.load('enemy.png')
bullet_img = pygame.image.load('bullet.png')
shopbtn_img = pygame.image.load('shop_btn.png')
tutorialbtn_img = pygame.image.load('tutorial.png')
tutorial_screen_img = pygame.image.load('tutorial_screen.png')
menubtn_img = pygame.image.load('menu.png')
shop_page1 = pygame.image.load('shoppistol.gif')
shop_page2 = pygame.image.load('shopshotgun.gif')
left_btn_img = pygame.image.load('left_btn.png')
right_btn_img = pygame.image.load('right_btn.png')
bullet_speed_img = pygame.image.load('bulletspeed.png')
bullet_damage_img = pygame.image.load('bulletdamage.png')

# For creating screen objects
class Screen():

    # Setting up the screen
    def __init__(self, height, width, image, caption, icon):
        self.height = height
        self.width = width
        self.image = pygame.transform.scale(image, (height, width))
        self.screen = pygame.display.set_mode((height, width))
        pygame.display.set_caption(f'{caption}')
        pygame.display.set_icon(icon)

    def draw(self):
        # Applies Background
        self.screen.blit(self.image, (0, 0))

class Text():
    def __init__(self, x, y, text, font, rgb, thescreen):
        self.text = font.render(text, True, rgb)
        self.x = x
        self.y = y
        self.screen = thescreen
    def write(self):
        self.screen.blit(self.text, (self.x, self.y))

# For Creating Buttons
class Button():
    def __init__(self, x, y, image, scale, function):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        # Creates a rectangle for clicking detection
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

        self.function = function

    def draw(self):
        action = False
        # Draw Button on Screen
        pos = pygame.mouse.get_pos()

        # check clicking conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        menu.screen.blit(self.image, (self.rect.x, self.rect.y))

        # If clicked triggers the respective function
        if action:
            self.function()


class Sprite():
    def __init__(self, x, y, image, type):
        self.x = x
        self.y = y
        self.image = image
        self.type = type
        self.width = image.get_width()
        self.height = image.get_height()

        # Enemy Sprite
        if type == 'enemy':
            self.enemy_type = random.choice(enemies_type)
            print(self.enemy_type)
            if self.enemy_type == 'normal':
                self.dx = 0.3
                self.dy = 50
                self.max_health = 10
                self.health_color = (255, 0, 0)
            elif self.enemy_type == 'fast':
                self.dx = 0.6
                self.dy = 100
                self.max_health = 1
                self.health_color = (0, 255, 0)
            elif self.enemy_type == 'tank':
                self.dx = 0.1
                self.dy = 20
                self.max_health = 30
                self.health_color = (0, 0, 255)

            self.health = self.max_health
            self.health_bar_length = self.width - 10
            self.health_ration = self.max_health/self.health_bar_length

        # Player Sprite
        if type == 'player':
            self.dx = 0.6
            self.dy = 0.1
            self.move_left = False
            self.move_right = False

        # Bullet Sprite
        if type == 'bullet':
            self.fire = False
            if gun == 'pistol':
                self.dy = data['pistol_speed'] # 0.8 by default
                self.damage = data['pistol_damage'] # 1 by default
            if gun == 'shotgun':
                self.dy = data['shotgun_speed'] # 0.2 by default
                self.damage = data['shotgun_damage'] # 5 by default

    def reset_bullet(self):
        self.x = player.x
        self.y = player.y
        self.fire = False
        cooldown_bullets.remove(self)
        ready_bullets.append(self)

    def reset_enemy(self):
        self.__init__(random.randint(100, 700), random.randint(10, 100), enemy_img, 'enemy')

    def basic_health(self):
        pygame.draw.rect(game.screen, self.health_color, (self.x + 5, self.y - 20, self.health/self.health_ration, 5))
        pygame.draw.rect(game.screen, (255, 255, 255), (self.x + 5, self.y - 20, self.health_bar_length, 5), 1)

    def draw(self):
        if self.type == 'enemy':
            # Moving the enemy
            self.x += self.dx
            # Border collisions of enemy
            # Moves down if collided by border and changes direction
            if self.x < 0:
                self.x = 0
                self.y = self.y + self.dy
                self.dx = self.dx * -1
            if self.x > game.height - 50:
                self.x = game.height - 50
                self.y = self.y + self.dy
                self.dx = self.dx * -1

        if self.type == 'player':

            # If left key is being pressed
            if self.move_left:
                self.x = self.x - self.dx
            # If right key is being pressed
            if self.move_right:
                self.x = self.x + self.dx
            # To avoid going out from border
            if self.x > game.height - 50:
                self.x = game.height - 50
            if self.x < 0:
                self.x = 0

        # Fires the bullet in ready_bullets list
        if self.type == 'bullet' and self.fire:
            # Updates the speed
            if gun == 'pistol':
                self.dy = data['pistol_speed'] # 0.8 by default
                self.damage = data['pistol_damage'] # 1 by default
            if gun == 'shotgun':
                self.dy = data['shotgun_speed'] # 0.2 by default
                self.damage = data['shotgun_damage'] # 5 by default

            self.y -= self.dy

        # If it reached above the screen the player can fire it again
        if self.y < 0:
            self.reset_bullet()

        game.screen.blit(self.image, (self.x, self.y))

    def is_collision(self, other):
        if self.x < other.x + other.width and\
            self.x + self.width > other.x and\
            self.y < other.y + other.height and\
            self.y + self.height > other.y:
            return True
        else:
            return False


# This create the game screen from the play button
def clk_play_btn():
    global score
    global screen
    global game
    score = 0
    for enemy in enemies:
        enemy.reset_enemy()
    screen = 'play'

shoppage = 1

def shop():
    global screen
    screen = 'shop'
def rightbtn():
    global shoppage
    shoppage += 1
def increase_damage():
    global money
    if money >= 10:
        data[f'{gun}_damage'] += 0.5
        money -= 10
        purchase_sound.play()
def increase_speed():
    global money
    if money >= 10:
        data[f'{gun}_speed'] += 0.05
        money -= 10
        purchase_sound.play()
def leftbtn():
    global shoppage
    shoppage -= 1
def tutorial():
    global screen
    screen = 'tutorial'
def menu():
    global screen
    screen = 'menu'

# Buttons
play_btn = Button(280, 130, play_img, 1, clk_play_btn)
shop_btn = Button(280, 230, shopbtn_img, 1, shop)
tutorial_btn = Button(280, 330, tutorialbtn_img, 1, tutorial)
menu_btn = Button(10, 530, menubtn_img, 1, menu)
right_btn = Button(600, 120, right_btn_img, 1, rightbtn)
left_btn = Button(50, 120, left_btn_img, 1, leftbtn)
bullet_damage_btn = Button(500, 190, bullet_damage_img, 1, increase_damage)
bullet_speed_btn = Button(100, 190, bullet_speed_img, 1, increase_speed)
# Player
player = Sprite(350, 500, player_img, 'player')

# Bullets
num_of_bullet = 1
ready_bullets = []
cooldown_bullets = []

# Makes all the bullets
for i in range(num_of_bullet):
    ready_bullets.append(Sprite(player.x, player.y, bullet_img, 'bullet'))

# Enemies
enemies_type = ['fast', 'normal', 'tank']
num_of_enemies = 5
enemies = []

for i in range(num_of_enemies):
    
    enemies.append(Sprite(random.randint(100, 700), random.randint(10, 100), enemy_img, 'enemy'))

# Creating a screen
HEIGHT = 800
WIDTH = 600
menu = Screen(HEIGHT, WIDTH, bg_img, 'Space Invaders', icon_img)

# Game screen
game = Screen(800, 600, bg_img, 'The Game', icon_img)

#Tut. screen
tutorial = Screen(800, 600, tutorial_screen_img, 'Tutorial', icon_img)

#Shop screen
shop = Screen(800, 600, shop_page1, 'Shop', icon_img)

# Adding a title to the game on menu screen
title_text = Text(200, 40, 'Space Invaders', myfont, (255, 0, 0), menu.screen)
#Game over text
gameover_text = Text(300, 200, 'Game Over', myfont, (255, 0, 0), game.screen)


# Creating a game loop

running = True
while running:

    # The menu screen
    if screen == 'tutorial':
        tutorial.draw()
        menu_btn.draw()
    if screen == 'shop':
        if shoppage == 1:
            gun = 'pistol'
            shop = Screen(800, 600, shop_page1, 'Shop', icon_img)
            shop.draw()
            right_btn.draw()

        if shoppage == 2:
            gun = 'shotgun'
            shop = Screen(800, 600, shop_page2, 'Shop', icon_img)
            shop.draw()
            left_btn.draw()
        bullet_damage_btn.draw()
        bullet_speed_btn.draw()
        menu_btn.draw()
    if screen == 'menu':
        menu.draw()
        title_text.write()

        # Drawing buttons
        play_btn.draw()
        shop_btn.draw()
        tutorial_btn.draw()

    # The game screen
    if screen == 'play':

        game.draw()

        # Updates the score
        score_text = Text(10, 10, f'Score: {score} Highscore: {highscore} Money: {money}$ Gun: {gun}', score_font, (255, 255, 255), game.screen)
        score_text.write()

        player.draw()

        # Draws the bullets that are being fired
        for bullet in cooldown_bullets:
            bullet.draw()

        # Updates the bullet position
        for bullet in ready_bullets:
            bullet.x = player.x + 22
            bullet.y = player.y

        for enemy in enemies:
            enemy.draw()
            enemy.basic_health()
            if player.is_collision(enemy):
                gameover_text.write()
                pygame.display.update()
                time.sleep(2)
                print('game over')
                screen = 'menu'
            for bullet in cooldown_bullets:
                if enemy.is_collision(bullet):
                    bullet.reset_bullet()
                    enemy.health -= bullet.damage
                    money += 0.1
                    money = round(money, 1)
                    if enemy.health <= 0:
                        score += 10
                        if score > highscore:
                            highscore = score
                        print(score)
                        enemy_die_sound.play()
                        enemy.reset_enemy()

    # Goes through all the events in pygame
    for event in pygame.event.get():
        # Checks if the cross button is being pressed if it is then the game ends
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # For moving the player
            if event.key == pygame.K_a:
                player.move_left = True
            if event.key == pygame.K_d:
                player.move_right = True
            if event.key == pygame.K_1:
                gun = 'pistol'
            if event.key == pygame.K_2:
                gun = 'shotgun'
                print(gun)

            # For Firing the bullets
            if event.key == pygame.K_SPACE:
                if len(ready_bullets) > 0:
                    bullet_sound.play()
                    ready_bullets[0].fire = True
                    cooldown_bullets.append(ready_bullets[0])
                    ready_bullets.remove(ready_bullets[0])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.move_left = False
            if event.key == pygame.K_d:
                player.move_right = False

    # Updates the Screen
    pygame.display.update()


data['highscore'] = highscore
data['money'] = money
with open('data.txt', 'w') as datafile:
    json.dump(data, datafile)
