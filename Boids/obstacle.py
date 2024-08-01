import pygame   
pygame.init()   
import random   
from pygame import Vector2

class Obstacle(pygame.sprite.Sprite): #Sprite for obstacle
    def __init__(self):
        super().__init__()

        self.x, self.y = 400, 250
        self.position = Vector2(400, 250)
        self.radius = 10
        self.color = (0, 225, 0)
        self.rect = pygame.Rect(self.x, self.y, (self.radius), (self.radius))
        
    def draw(self, screen):
        pygame.draw.circle(screen, (self.color), (int(self.rect.x), int(self.rect.y)), self.radius) 
        
    def obstacle_update(self, screen):
        self.draw(screen)