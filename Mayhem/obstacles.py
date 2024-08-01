import pygame
from pygame import Vector2
from CONFIG import Planet_obstacle
from CONFIG import Fuel_icon_traits
from CONFIG import Game_traits
pygame.init()

""" *Planet-class:
    -Contains instances of other sprite-classes to access variables from them
    -All of "Planets" variables are changed in the CONFIG-file
    -All of the methods in this class is updated in the "update" method
"""
class Planet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        ########## CREATING OBSTACLE-OBJECT TO ACCESS VARIABLES FROM CONFIG-FILE ##########
        self.planet = Planet_obstacle()
        self.game_traits = Game_traits()

        ########## TRAITS FOR THE SPRITE ##########
        self.original_image = self.planet.PLANET_IMAGE
        self.original_image = pygame.transform.scale(self.original_image, (self.planet.SIZE[0], self.planet.SIZE[1]))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = self.planet.POSITION[0], self.planet.POSITION[1]

        self.speed = self.planet.SPEED
        self.angle = self.planet.ANGLE
        self.rotation_speed = self.planet.ROTATION_SPEED
        self.direction = self.planet.DIRECTION 
    
    """ *Move_planet method:
        -Moves the planet in a desired direction, changing its X and Y coordinates and rotates it.
        -Makes it bounce of the walls if its X and Y coordinates are bigger or less than one of the walls.
        -If it hits a wall its X or Y value is changed to the opposite of the previous value.
        
        -The image of the sprite is rotated using pygame.transform.rotate() function.
        -If the same picture is rotated more than once it gets distorted, that's why I keep the original image
         and rotate this every time instead of rotating an already rotated image.  

        -The transform.rotate() method rotates an image from the top-left corner making the image bounce in a weird way, to fix this I keep track of 
         the images center, then i rotate the image and correct its new position to be the same as the "old" center 
    """
    def move_planet(self):
        ##### BOUNCE OF WALLS #####
        self.rect.center += self.direction * self.speed

        if self.rect.x + self.planet.SIZE[0] >= self.game_traits.SCREEN_WIDTH: #RIGHT WALL
            self.direction[0] *= -1
            
        if self.rect.y + self.planet.SIZE[1] >= self.game_traits.SCREEN_HEIGHT: #FLOOR
            self.direction[1] *= -1

        if self.rect.x <= 0: #LEFT WALL
            self.direction[0] *= -1

        if self.rect.y <= 0: #ROOF
            self.direction[1] *= -1
        
        ##### ROTATION #####
        if self.direction[0] > 0:
            self.angle -= self.rotation_speed

        if self.direction[0] < 0:
            self.angle = abs(self.angle)
            self.angle += self.rotation_speed

        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

    """ * Update method:
        -Calls all methods in this file:
        -All the methods contained in the Planet class are put inside this method since the sprite.update function requires a "update" method to update the sprite
    """
    def update(self, screen):
        self.move_planet()


""" *Fuel_icon class:
    -This class requires an X and Y position value, so that I can create more of it in different locations
    -Contains instances of other sprite-classes to access variables from them
    -All of "Fuel icons" variables are changed in the CONFIG-file
    -All of the methods in this class is updated in the "update" method
"""
class Fuel_icon(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)

        ########## CREATING OBSTACLE-OBJECT TO ACCESS VARIABLES FROM CONFIG-FILE ##########
        self.fuel_icon_traits = Fuel_icon_traits()
        self.game_traits = Game_traits()

        ########## TRAITS FOR THE SPRITE ##########
        self.image = self.fuel_icon_traits.FUEL_IMAGE
        self.image = pygame.transform.scale(self.image, (self.fuel_icon_traits.SIZE[0], self.fuel_icon_traits.SIZE[1]))
        self.rect = self.image.get_rect()
        self.rect.center = x_pos, y_pos