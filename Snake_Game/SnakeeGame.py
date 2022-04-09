import pygame
import random
import sys
import os
from math import ceil
from display import *

def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

# initialize 
pygame.init()
random.seed()
pygame.mixer.init(44100, -16,2,2048)

# create display & run update
width = 640
height = 480
display = pygame.display.set_mode((width, height))
 
pygame.display.update()
pygame.display.set_caption("SnakeeGame")

fn = pygame.image.load(resource_path('floor.jpg'))

#sound
pygame.mixer.music.load(resource_path('background.wav'))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

eat_sound = pygame.mixer.Sound(resource_path('foodeaten_sound.wav'))
lose_sound = pygame.mixer.Sound(resource_path('lose_sound.wav'))
click_sound = pygame.mixer.Sound(resource_path('click_sound.wav'))
win_sound = pygame.mixer.Sound(resource_path('winner.wav'))

#snake skin
skin = 0

snake_head =[{
    'up': pygame.image.load(resource_path('SnakeHead_up.png')),
    'right': pygame.image.load(resource_path('SnakeHead_right.png')),
    'down': pygame.image.load(resource_path('SnakeHead_down.png')),
    'left': pygame.image.load(resource_path('SnakeHead_left.png'))},
    {'up': pygame.image.load(resource_path('SnakeHead_up_2.png')),
    'right': pygame.image.load(resource_path('SnakeHead_right_2.png')),
    'down': pygame.image.load(resource_path('SnakeHead_down_2.png')),
    'left': pygame.image.load(resource_path('SnakeHead_left_2.png'))},
    {'up': pygame.image.load(resource_path('SnakeHead_up_3.png')),
    'right': pygame.image.load(resource_path('SnakeHead_right_3.png')),
    'down': pygame.image.load(resource_path('SnakeHead_down_3.png')),
    'left': pygame.image.load(resource_path('SnakeHead_left_3.png'))}]
snake_tail = [{
    'up': pygame.image.load(resource_path('Tail_up.png')),
    'right': pygame.image.load(resource_path('Tail_right.png')),
    'down': pygame.image.load(resource_path('Tail_down.png')),
    'left': pygame.image.load(resource_path('Tail_left.png'))},
    {'up': pygame.image.load(resource_path('Tail_up_2.png')),
    'right': pygame.image.load(resource_path('Tail_right_2.png')),
    'down': pygame.image.load(resource_path('Tail_down_2.png')),
    'left': pygame.image.load(resource_path('Tail_left_2.png'))},
    {'up': pygame.image.load(resource_path('Tail_up_3.png')),
    'right': pygame.image.load(resource_path('Tail_right_3.png')),
    'down': pygame.image.load(resource_path('Tail_down_3.png')),
    'left': pygame.image.load(resource_path('Tail_left_3.png'))}]
snake_eat =[{
    'up': pygame.image.load(resource_path('SnakeEat_up.png')),
    'right': pygame.image.load(resource_path('SnakeEat_right.png')),
    'down': pygame.image.load(resource_path('SnakeEat_down.png')),
    'left': pygame.image.load(resource_path('SnakeEat_left.png'))},
    {'up': pygame.image.load(resource_path('SnakeEat_up_2.png')),
    'right': pygame.image.load(resource_path('SnakeEat_right_2.png')),
    'down': pygame.image.load(resource_path('SnakeEat_down_2.png')),
    'left': pygame.image.load(resource_path('SnakeEat_left_2.png'))},
    {'up': pygame.image.load(resource_path('SnakeEat_up_3.png')),
    'right': pygame.image.load(resource_path('SnakeEat_right_3.png')),
    'down': pygame.image.load(resource_path('SnakeEat_down_3.png')),
    'left': pygame.image.load(resource_path('SnakeEat_left_3.png'))}]
TL = {'0': pygame.image.load(resource_path('TL.png')),
      '1': pygame.image.load(resource_path('TL_2.png')),
      '2': pygame.image.load(resource_path('TL_3.png'))}

#skin button
start_button = [pygame.image.load(resource_path('start.png')), pygame.image.load(resource_path('startOFF.png'))]
skins_button = [pygame.image.load(resource_path('skins.png')), pygame.image.load(resource_path('skinsOFF.png'))]
exit_button = [pygame.image.load(resource_path('exit.png')), pygame.image.load(resource_path('exitOFF.png'))]
menu_button = [pygame.image.load(resource_path('menu.png')), pygame.image.load(resource_path('menuOFF.png'))]
survival_button = [pygame.image.load(resource_path('survival.png')), pygame.image.load(resource_path('survivalOFF.png'))]
continue_button = [pygame.image.load(resource_path('continue.png')), pygame.image.load(resource_path('continueOFF.png'))]
normal_button = [pygame.image.load(resource_path('normal.png')), pygame.image.load(resource_path('normalOFF.png'))]
restart_button = [pygame.image.load(resource_path('restart.png')), pygame.image.load(resource_path('restartOFF.png'))]

#skin food
skin_f = 0

apple = [pygame.image.load(resource_path('apple.png')),pygame.image.load(resource_path('cherry.png'))]

#win
golden_cup = pygame.image.load(resource_path('golden_cup.png'))

#START
game_end = True

menu_display(
    width, height, display,
    fn, start_button, skins_button,
    exit_button, skin, snake_head,
    snake_tail,snake_eat,
    TL, golden_cup, skin_f, apple,
    menu_button, survival_button,
    continue_button, normal_button,
    restart_button, game_end,
    eat_sound, lose_sound, click_sound, win_sound)

#close display
pygame.quit()
