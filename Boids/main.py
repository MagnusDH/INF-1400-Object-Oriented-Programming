import pygame                   
import random                   
from boid import Boid          
from hoik import Hoik           
from obstacle import Obstacle
from pygame import Vector2
pygame.init()                   

class Game:
    def __init__(self):
        self.screen_size_x = 800
        self.screen_size_y = 500
        self.screen = pygame.display.set_mode((self.screen_size_x, self.screen_size_y), 0, 32)
        self.clock = pygame.time.Clock()

        ## OBJECTS ##

        ## HOIK ##
        self.hoik = Hoik()
        self.list_hoik = pygame.sprite.Group()
        self.list_hoik.add(self.hoik)

        ## Obstacle ##

        self.obstacle = Obstacle()
        self.list_obstacle = pygame.sprite.Group
        self.list_obstacle.add(self.obstacle)

        ## List for boids ##

        self.list_boids = pygame.sprite.Group()
    
    def create_boid(self):
        if pygame.mouse.get_pressed()[0]:
            new_boid = Boid(self.screen_size_x, self.screen_size_y)
            self.list_boids.add(new_boid)
    
    def hoik_eat_boid(self):
        pygame.sprite.spritecollide(self.hoik, self.list_boids, True, pygame.sprite.collide_circle)

    def programloop(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type ==pygame.QUIT:
                    running = False
            
            self.clock.tick(60)
            self.screen.fill((0,0,0))
            pygame.display.set_caption("BOIDS")

            ## Updating boids ##
            for boid in self.list_boids:
                boid.update(self.screen_size_x, self.screen_size_y, self.screen, self.list_boids, self.list_hoik, self.list_obstacle)
           
            self.create_boid()

            ## Updating hoik ##
            self.hoik.hoik_update(self.screen)            
            self.hoik_eat_boid()

            ## Updating obstacle ##
            #self.obstacle.obstacle_update(self.screen)

            pygame.display.update()

if __name__ == "__main__":
    sim = Game()
    sim.programloop()
