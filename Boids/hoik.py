import pygame   
pygame.init()   
import random   
from pygame import Vector2

class Hoik(pygame.sprite.Sprite): #Sprite for hoik
    def __init__(self):
        super().__init__()

        self.x, self.y = pygame.mouse.get_pos()
        self.position = pygame.mouse.get_pos()
        self.radius = 10
        self.color = (225, 0, 0)
        self.rect = pygame.Rect(self.x, self.y, (self.radius), (self.radius))
    
    def move(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()   #Hoiks position depending on the mouse
        self.position = pygame.mouse.get_pos()
        
    def draw(self, screen):
        pygame.draw.circle(screen, (self.color), (int(self.rect.x), int(self.rect.y)), self.radius) 
        
    def hoik_update(self, screen):
        self.move()
        self.draw(screen)