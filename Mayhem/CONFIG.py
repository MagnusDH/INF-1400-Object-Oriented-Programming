import pygame
from pygame import Vector2
import random
pygame.init()

""" THIS FILE CONTAINS ALL CHANGABLE VARIABLES FOR EACH CLASS CONTAINED IN THE GAME """ 

########## GAME FEATURES ##########
class Game_traits():
    FPS = 60                                                            #HOW MANY FRAMES PER SECOND THE PROGRAM RUNS ON
    SCREEN_WIDTH = 1200                                                 #WIDTH OF THE SCREEN (SHOULD BE 1200 SINCE PLAYERS POSITIONS ARE BASED ON THIS)
    SCREEN_HEIGHT = 600                                                 #HEIGHT OF THE SCREEN (SHOULD BE 600 SINCE PLAYERS POSITIONS ARE BASED ON THIS)
    SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])     #SETTING UP A SCREEN
    BACKGROUND = pygame.image.load('background.jpg')                    #BACKGROUND IMAGE
    BACKGROUND_MUSIC = pygame.mixer.music.load('background_music.mp3')  #REGULAR BACKGROUND MUSIC
    EXPLOSION_SOUND = pygame.mixer.Sound('Explosion.wav')            #SOUND WHEN THINGS EXPLODES

class Planet_obstacle():
    PLANET_IMAGE = pygame.image.load('planet.png').convert_alpha()
    SIZE = 200, 200                                                     #OBSTACLE SIZE (X AND Y SHOULD BE EQUAL)
    POSITION = 600, 300                                                 #STARTING POSITION (FROM IT'S CENTER)
    SPEED = 1                                                           #HOW FAST THE OBSTACLE TRAVELS
    DIRECTION = Vector2(0,1)#(random.randint(-1, 1), random.randint(-1, 1))   #DO NOT GIVE X-DIRECTION A CHANCE TO BE ZERO!!!!
    ANGLE = 0                                                           #STARTING ANGLE OF THE OBSTACLE
    ROTATION_SPEED = 0                                                  #HOW FAST THE OBSTQACLE ROTATES

class Fuel_icon_traits():
    FUEL_IMAGE = pygame.image.load('fuel_recharge.png').convert_alpha()
    SIZE = 50, 70

######## PLAYER 1 FEATURES ########
class Player1_traits():
    PLAYER_IMAGE = pygame.image.load('spaceship1.png').convert_alpha()
    SIZE = 40, 40                                                       #PLAYERS SIZE (X AND Y SHOULD BE EQUAL)
    POSITION = 1100, 450                                                #STARTING POSITION OF THE PLAYER (FROM IT'S CENTER)
    PLAYER_SPEED = 5                                                    #HOW FAST THE PLAYER TRAVELS
    FUEL_TANK = 800                                                     #HOW MUCH FUEL THE PLAYER HAS
    FUEL_CONSUMPTION = 1                                                #HOW FAST THE FUEL TANK IS DEPLETED
    ANGLE = 0                                                           #STARTING ANGLE
    ROTATION_SPEED = 5                                                  #HOW FAST THE IMAGE ROTATES
    GRAVITY_EFFECT = 1                                                  #HOW FAST THE PLAYER IS BEING PULLED DOWN

########## PLAYER 2 FEATURES ##########
class Player2_traits():
    PLAYER_IMAGE = pygame.image.load('spaceship2.png').convert_alpha()
    SIZE = 40, 40                                                       #PLAYERS SIZE (X AND Y SHOULD BE EQUAL)
    POSITION = 100, 450                                                 #STARTING POSITION OF THE PLAYER (FROM IT'S CENTER)
    PLAYER_SPEED = 5                                                    #HOW FAST THE PLAYER TRAVELS
    FUEL_TANK = 800                                                     #HOW MUCH FUEL THE PLAYER HAS
    FUEL_CONSUMPTION = 1                                                #HOW FAST THE FUEL TANK IS DEPLETED
    ANGLE = 0                                                           #STARTING ANGLE
    ROTATION_SPEED = 5                                                  #HOW FAST THE IMAGE ROTATES
    GRAVITY_EFFECT = 1                                                  #HOW FAST THE PLAYER IS BEING PULLED DOWN

########## BULLET FEATURES ##########
class Bullet_traits():
    BULLET_IMAGE = pygame.image.load('bullet1.png')
    SHOOTING_SOUND = pygame.mixer.Sound('Laser.wav')
    SIZE =  30, 30                                                      #BULLETS SIZE (X AND Y SHOULD BE EQUAL)
    SPEED = 40                                                          #HOW FAST THE BULLET TRAVELS
    COOLDOWN_TIME = 500                                                 #HOW OFTEN SHOTS CAN BE FIRES IN MILISECONDS (1000 ms = 1 sec)