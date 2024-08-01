import pygame   
pygame.init()   
import random   
from pygame import Vector2
from hoik import Hoik

#DEFINING VARABLES
ALIGN_FORCE = 1
SEPARAT_FORCE = 1.2
COHESION_FORCE = 1
FLEE_FORCE = 1
#AVOID_FORCE = 1

class Boid(pygame.sprite.Sprite):   #Sprite for boid
    def __init__(self, screen_size_x, screen_size_y):
        super().__init__()
         
        self.x = random.randint(0, screen_size_x)
        self.y = random.randint(0, screen_size_y)
        self.position = Vector2(self.x, self.y)
        self.radius = 3
        self.color = (195, 195, 195)
        self.speeds = [-4, -3, 3, 4]                                                 
        self.speed = pygame.Vector2(random.choice(self.speeds) ,random.choice(self.speeds))
        self.maxspeed = Vector2(random.randint(-7, 7), random.randint(-7, 7))
        self.rect = pygame.Rect(self.x, self.y, (self.radius*2), (self.radius*2))  #(Left, top, width, height)
        self.alignRadius = 50
        self.cohesionRadius = 50
        self.separationRadius = 30
        self.acceleration = Vector2(0.0)
        self.maxspeed = 3
             
    def wall_loop(self, screen_size_x, screen_size_y):  #Makes the boids loop through the edges of the screen
        if self.position.x > screen_size_x:                  
            self.position.x = 0                              
        if self.position.y > screen_size_y:                  
            self.position.y = 0                              
        if self.position.x < 0 and self.speed[0] < 0:        
            self.position.x = screen_size_x                  
        if self.position.y < 0 and self.speed[1] < 0:        
            self.position.y = screen_size_y                  

    def align(self, list_boids):    #Gets a boid to align and get the average speed as other boids
        counter = 0
        average_speed = Vector2(0,0)

        for boid in list_boids:

            if boid != self:

                distance = Vector2.distance_to(self.position, boid.position)
                if distance <= self.alignRadius:
                    counter += 1
                    average_speed += boid.speed

        if counter > 0:
            average_speed /= counter    #Average speed of boids within a radius

        if average_speed.length() != 0:
            return average_speed.normalize()

        return average_speed 

    def cohesion(self, list_boids):    #Gets boids to move towards the centre of a flock
        average_position = Vector2(0,0)
        counter = 0

        for boid in list_boids:

            if boid != self:
                    
                distance = Vector2.distance_to(self.position, boid.position)
                if distance <= self.cohesionRadius:
                    average_position += boid.position
                    counter += 1

        if counter > 0:
            average_position /= counter     #Average position of boids within a radius
            average_position -= self.position
        if average_position.length() != 0:
            return average_position.normalize()

        return average_position

    def separation(self, list_boids):  #Gets boids to not collide with each other
        average_position = Vector2(0,0)
        counter = 0

        for boid in list_boids:
            if boid != self:
                distance = Vector2.distance_to(self.position, boid.position)
                if distance <= self.separationRadius:
                    difference = self.position - boid.position
                    difference = difference / distance
                    average_position += difference
                    counter += 1
                    

        if counter > 0:
            average_position /= counter     #Average position of boids within a radius
            
        if average_position.length() != 0:
            return average_position.normalize()

        return average_position
    
    def flee(self, list_boids, list_hoik):  #Makes boids avoid a Hoik
        average_position = Vector2(0,0) 
        counter = 0

        for hoik in list_hoik:
            distance = Vector2.distance_to(self.position, hoik.position)
            if distance <= self.alignRadius:
                difference = self.position - hoik.position
                difference = difference / distance
                average_position += difference
                counter += 1
                    

        if counter > 0:
            average_position /= counter
            
        if average_position.length() != 0:
            return average_position.normalize()

        return average_position
    
    def avoid_obstacle(self, list_boids, list_obstacle):    #Makes the boids avoid obstacles
        average_position = Vector2(0,0) 
        counter = 0

        for obstacle in list_obstacle:
            distance = Vector2.distance_to(self.position, obstacle.position)
            if distance <= self.alignRadius:
                difference = self.position - obstacle.position
                difference = difference / distance
                average_position += difference
                counter += 1
                    

        if counter > 0:
            average_position /= counter
            
        if average_position.length() != 0:
            return average_position.normalize()

        return average_position

    def move(self): #Moves the boids
        self.speed += self.acceleration
        self.speed = self.speed.normalize() * self.maxspeed
        self.position += self.speed

        ## Updating rectangle coordinates ##
        self.rect = pygame.Rect(self.x, self.y, (self.radius*2), (self.radius*2))  #(Left, top, width, height)
        
        self.rect.x = self.position[0]  #Changes position to rect.x to get the hoik_boid_collide method to work correctly
        self.rect.y = self.position[1]  #Changes position to rect.y to get the hoik_boid_collide method to work correctly
    
    def draw(self, screen): #Draws the boids
        pygame.draw.circle(screen, (self.color), (int(self.position.x), int(self.position.y)), self.radius)
    
    def apply_rules(self, list_boids, list_hoik, list_obstacle):    #Applies all the rules for the boids
        alignment = self.align(list_boids)
        cohesion = self.cohesion(list_boids)
        separation = self.separation(list_boids)
        flee = self.flee(list_boids, list_hoik)
        #avoid_obstacle = self.avoid_obstacle(list_boids, list_obstacle)

    ## How much force each rule should apply ##
        alignment *= ALIGN_FORCE
        cohesion *= COHESION_FORCE
        separation *= SEPARAT_FORCE
        flee *= FLEE_FORCE
        #avoid *= AVOID_FORCE

    ## All the forces added together ##

        #self.acceleration = alignment
        #self.acceleration = cohesion
        #self.acceleration = separation
        #self.acceleration = flee
        self.acceleration = separation + cohesion + alignment + flee #+ avoid

    def update(self, screen_size_x, screen_size_y, screen, list_boids, list_hoik, list_obstacle):   #Updates all the methods in the Boid class
            self.wall_loop(screen_size_x, screen_size_y)
            self.move()
            self.draw(screen)
            self.apply_rules(list_boids, list_hoik, list_obstacle)