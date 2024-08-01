import pygame
from pygame import Vector2
from CONFIG import Bullet_traits
from CONFIG import Game_traits
pygame.init()

""" *Bullet-class:
    -This class requires a player-class argument so that it can access the players direction variable. The direction of the bullet (when created) is to be
     the same as the players direction.
    -Contains instances of other sprite-classes to access variables from them
    -All of bullets variables are changed in the CONFIG-file
    -All of the methods in this class is updated in the "update" method
"""
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)

        ########## CREATING OBJECTS TO ACCESS VARIABLES FROM CONFIG-FILE ##########
        self.bullet = Bullet_traits()
        self.game_traits = Game_traits()

        ########## TRAITS FOR THE SPRITE ##########
        self.image = self.bullet.BULLET_IMAGE
        self.speed = self.bullet.SPEED
        self.image = pygame.transform.scale(self.image, (self.bullet.SIZE[0], self.bullet.SIZE[1]))
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center + 15 * player.direction
        self.direction = player.direction
    
    """ *Move method:
        -Moves the bullet X and Y coordinates in the same direction as one of the players. 
        -The direction variable is calculated inside the players "move_spaceship" methods.
        -This method also removes the bullets from its group when they hit a wall.
    """
    def move(self):
        self.rect.center -= self.direction * self.speed
        
        if self.rect.x >= self.game_traits.SCREEN_WIDTH:
            pygame.sprite.Sprite.kill(self)

        if self.rect.x <= 0:
            pygame.sprite.Sprite.kill(self)

        if self.rect.y >= self.game_traits.SCREEN_HEIGHT:
            pygame.sprite.Sprite.kill(self)

        if self.rect.y <= 0:
            pygame.sprite.Sprite.kill(self)
    
    """ *Update method:
        -Updates all methods in this class
    """
    def update(self, screen):
        self.move()