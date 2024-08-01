import pygame
from pygame import Vector2
from math import radians, sin, cos
from CONFIG import Player2_traits
from CONFIG import Game_traits
from CONFIG import Bullet_traits
from bullet import Bullet
pygame.init()

""" *Player2-class:
    -This class requires a sprite group argument and a X and Y position value. The sprite group argument is used to put 
     bullets inside when they are created, and the X and Y values are position values so that I can either create more of them or change their "starting position"
    -Contains instances of other sprite-classes to access variables from them
    -All of player2's variables are changed in the CONFIG-file
    -All of the methods in this class is updated in the "update" method
"""
class Player2(pygame.sprite.Sprite):
    def __init__(self, player2_bullets, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)

        ########## CREATING player2-OBJECT TO ACCESS VARIABLES FROM CONFIG-FILE ##########
        self.p2 = Player2_traits()
        self.game_traits = Game_traits()
        self.bullet_traits = Bullet_traits()
    
        ########## TRAITS FOR THE SPRITE ##########       
        self.original_image = self.p2.PLAYER_IMAGE
        self.original_image = pygame.transform.scale(self.original_image, (self.p2.SIZE[0], self.p2.SIZE[1]))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = x_pos, y_pos

        self.speed = self.p2.PLAYER_SPEED
        self.fuel_tank = self.p2.FUEL_TANK
        self.fuel_consumption = self.p2.FUEL_CONSUMPTION
        self.angle = self.p2.ANGLE
        self.rotation_speed = self.p2.ROTATION_SPEED
        self.center = Vector2(self.rect.center)

        self.player2_bullets = player2_bullets
        self.start_time = pygame.time.get_ticks()                 #USED FOR FIRE METHOD
        self.cooldown = self.bullet_traits.COOLDOWN_TIME    #USED FOR FIRE METHOD
        self.shooting_sound = self.bullet_traits.SHOOTING_SOUND
    
    """ *Gravity method:
        -Changes the sprites x.position by the "GRAVITY-EFFECT" variable
        -Mainly encreases the x.position to push the player downwards
    """
    def gravity(self):
        self.rect.y += self.p2.GRAVITY_EFFECT

    """ *Move_spaceship method:
        -Rotates and moves the spaceship in a spesific direction while keeping track on fuel-consumption
        
        -The image of the sprite is rotated using pygame.transform.rotate() function.
        -If the same picture is rotated more than once it gets distorted, that's why I keep the original image
         and rotate this every time instead of rotating an already rotated image.  

        -The transform.rotate() method rotates an image from the top-left corner making the image bounce in a weird way, to fix this I keep track of 
         the images center, then i rotate the image and correct its new position to be the same as the "old" center 

        -The direction and movement is decided by a vector. This vector is calculated by using pythons function for calculating radians which converts a variable X
         from "angle" to radians. The angle value is encreased or decreased depending on which key is pressed, then converted to a radian value. 
        -To figure out the vector(direction) for the player I use the sin() and cos() functions which returns a sine and cosine values of a variable. 
        -The calculated vector is stored as a "direction" variable, and the players X and Y position is moved acordingly. 

        -To keep track of the angle-variable I set its value to be zero whenever it becomes more than positive or negative 359 degress, since 360 degrees
         is the same as 0 degrees.          
    """
    def move_spaceship(self):
        keys = pygame.key.get_pressed()

        ##### ROTATION #####
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

        ##### DIRECTION AND MOVEMENT #####
        rad = radians(self.angle)                           #Metoden returnerer radianer verdien til self.angle
        self.direction = pygame.Vector2(sin(rad), cos(rad)) #Konverterer sinusverdien og cosinus verdien til radianer verdier
        self.direction = self.direction.normalize()

        if self.angle > 359:
            self.angle = 0
        if self.angle < -359:
            self.angle = 0

        if keys[pygame.K_a]:
            self.angle += self.rotation_speed

        if keys[pygame.K_d]:
            self.angle -= self.rotation_speed

        if keys[pygame.K_w]:
            self.fuel_tank -= self.fuel_consumption
            if self.fuel_tank > 0:
                self.rect.center -= self.direction * self.speed

        if keys[pygame.K_s]:
            self.rect.center += self.direction * self.speed/2
           
    """ *Loop_walls method:
        -Makes the player able to loop through walls
        -Simply by checking if the players X and Y position is greater or less than a spesific walls, then changing it X or Y value to the opposite side 
         of the screen.
    """
    def loop_walls(self):
        if (self.rect.x + self.p2.SIZE[0]) < 0:             #Left wall
            self.rect.x = self.game_traits.SCREEN_WIDTH
        if self.rect.x > self.game_traits.SCREEN_WIDTH:     #Right wall
            self.rect.x = -self.p2.SIZE[0]
        if (self.rect.y + self.p2.SIZE[1]) < 0:             #Roof
            self.rect.y = self.game_traits.SCREEN_HEIGHT
        if self.rect.y > self.game_traits.SCREEN_HEIGHT:    #Floor
            self.rect.y = -self.p2.SIZE[1]

    """ *Fire method:
        -Creates a bullet when a key is pressed:
        -Using the pygame.key.get_pressed() function a bullet-object is created using the Bullet-class.
        -The object is stored inside a sprite group which gets updated in the main-programloop
        -I use the pygame.time.get_ticks function to calculate how many miliseconds have passed since the first bullet is created. The player is not allowed
         to create more bullets unless a spesific "cooldown" time have passed, which can be modified in the CONFIG file.
        -The bullets are added to a spesific sprite group belonging to Player2 to separate them from player1's bullets
    """
    def fire(self):
        keys = pygame.key.get_pressed()
        self.now_time = pygame.time.get_ticks()
        if self.now_time - self.start_time >= self.cooldown:
            if keys[pygame.K_c]:
                self.start_time = self.now_time
                self.shooting_sound.play()
                bullet = Bullet(self)
                self.player2_bullets.add(bullet)

    """ * Update method:
        -Calls all methods in this file:
        -All the methods contained in the player1 class are put inside this method since the sprite.update function requires a "update" method to update the sprite
    """
    def update(self, screen):
        self.move_spaceship()
        self.gravity()
        self.loop_walls()
        self.fire()