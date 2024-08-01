import pygame
import random

### Configuration ###
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
STEPS_PER_SECOND = 30

RECOVERY_TIME = 5
SYKEBIL_SPEED = 2

INFECTION_RANGE = 40
MOVEMENT_RANGE = 5
NUMBER_OF_PEOPLE = 100


####
# List and weights of behaviors and status
# Weights are relative (e.g. susceptible is 10 times more likely than infected)
####
behaviors = ["surrehode", "sykebil", "surrehode_munnbind"]    
behavior_weight = [20, 1, 15]
status = ["infected", "susceptible", "recovered"]
status_weight = [1, 10, 0]

#### Oppretter sprite groups ####
surrehoder_sprites = pygame.sprite.Group()
sykebil_sprites = pygame.sprite.Group()
surrehoder_munnbind_sprites = pygame.sprite.Group()


class Update:
    def __init__(self):
        pass
        
    """Metoden er ment å kunne opprette en instans av en klasse basert-
       på hvilket element fra listene som blir valgt.

       Fargen/status på instansen blir tilfeldig valgt fra status-listen
       Sykebilenes farge/status er alltid blå/recovered og blir bestemt i Sykebil klassen

       Instansen som blir laget blir puttet i en sprite group som senere kan bli oppdatert og tegnet"""
    def make_person():
        pos_x = random.randint(0, SCREEN_WIDTH)
        pos_y = random.randint(0, SCREEN_HEIGHT)
        person = random.choices(behaviors, behavior_weight)[0]
        position = pygame.math.Vector2(pos_x, pos_y)
        status = random.choices(status, status_weight)[0]
        
        if person == "surrehode":
            surrehode = Surrehode()
            surrehode.position = position
            if status == "infected":
                surrehode.color = (255, 0, 0)
            if status == "susceptible":
                surrehode.color = (0, 255, 0)
            if status == "recovered":
                surrehode.color = (0, 0, 255)

            surrehode.status = status
            surrehoder_sprites.add(surrehode)
            
        if person == "sykebil":
            sykebil = Sykebil()
            sykebil_sprites.add(sykebil)
        
        if person == "surrehode_munnbind":
            surrehode_munnbind = Surrehode_munnbind()
            surrehode_munnbind.center = position
            if status == "infected":
                surrehode_munnbind.color = (255, 0, 0)
            if status == "susceptible":
                surrehode_munnbind.color = (0, 255, 0)
            if status == "recovered":
                surrehode_munnbind.color = (0, 0, 255)

    """klassen metoden tar som argument er ment å ha en posisjons verdi som blir endret på med en tilfeldig verdi 
         for hvert "STEPS_PER_SECOND" """
    def move(class_object):
        if class_object == Surrehode:
            movement_x = random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE)
            movement_y = random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE)
            movement_vector = pygame.math.Vector2(movement_x, movement_y)

            class_object.position += movement_vector

            #Looper objektet gjennom veggene
            if class_object.position[0] < 0:
                class_object.position[0] = SCREEN_WIDTH + class_object.position[0]

            if class_object.position[0] > SCREEN_WIDTH:
                class_object.position[0] = class_object.position[0] % SCREEN_HEIGHT

            if class_object.position[1] < 0:
                class_object.position[1] = SCREEN_HEIGHT + class_object.position[1]

            if class_object.position[1] > SCREEN_HEIGHT:
                class_object.position[1] = class_object.position[1] % SCREEN_HEIGHT
        
        if class_object == Sykebil:
            closest_surrehode = find_closest_infected(target, others)
            if closest_surrehode is None:
                return
            difference_vector = closest_surrehode.center - class_object.center
            try:
                movement_direction = difference_vector.normalize()
            except ValueError:
                movement_direction = pygame.math.Vector2(0,0)
            class_object.center += movement_direction * SYKEBIL_SPEED


class Surrehode(Update):
    def __init__(self):
        super().__init__():
        self.x = 0
        self.y = 0
        self.position = pygame.Vector2(0,0)
        self.color = (0, 0, 0)
        self.status = ""
        self.INFECTION_RANGE = 40
        self.sick_time = 0

    """Metoden er tenkt slik at objektet skifter farge avhengig av hvilken status den har.
       Objektet skal sjekke seg selv opp mot et objekt fra sprite gruppen den får som argument og forandrer farge/status avhengig av hva som er i nærheten av den"""
    def update_infection_status(self, sprite_group):
        if self.color == (255, 0, 0): #Infected
            self.sick_time += 1
            if self.sick_time > RECOVERY_TIME * STEPS_PER_SECOND:
                self.color = (0, 0, 255) #Recovered
            for sprite in sprite_group:
                if sprite != self:
                    distance = Vector2.distance_to(self.position, sprite.position)
                    if distance < INFECTION_RANGE:
                        if sprite == Sykebil:
                            self.color = (0, 0, 255) #Recovered
                        if sprite == Surrehode or Surrehode_munnbind:
                            self.color = (255, 0, 0) #Infected           

    """Her er tanken at metoden "move" blir definert pånytt inne i klassen, slik at den ikke arver fra "move" metoden i Update klassen.
       Denne metoden forandrer kun på surrehodenes posisjon"""
    def move(self):
        movement_y = random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE)
        movement_x = random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE)
        movement_vector = pygame.math.Vector2(movement_x, movement_y)

        self.position += movement_vector
        
        #Looper objektet gjennom veggene
        if self.x < 0:
                self.x = SCREEN_WIDTH + self.x
        if self.x > SCREEN_WIDTH:
                self.x = self.x % SCREEN_HEIGHT
        if self.y < 0:
                self.y = SCREEN_HEIGHT + self.y
        if self.y > SCREEN_HEIGHT:
                self.y = self.y % SCREEN_HEIGHT


class Sykebil(Update):
    def __init__(self):
        super().__init__()  
        self.x = 0
        self.y = 0
        self.position = pygame.Vector2(0,0)
        self.color = (0, 0, 255)

    def find_closest_infected(self, sprite_group):
        min_distance = 1000
        closest = None

        for sprite in sprite_group:
            if sprite != self:
                if sprite.color == (255, 0, 0): #Infected
                    distance = sprite.position.distance_to(self.position)
                    if distance < min_distanceand distance != 0:
                        min_distance = distance
                        closest = other
        return closest


class Surrehode_munnbind(Surrehode):
    def __init__(self):
        super().__init__():
        self.x = 0
        self.y = 0
        self.position = pygame.Vector2(0,0)
        self.status = ""
        self.infection_range = 20

    """I denne funksjonen har jeg tenkt at infeksjonsradiusen til de med munnbind er mindre enn de uten munnbind.
        Derfor har jeg lagt til en ny variabel "self.infection_range" som har mindre radius enn "INFECTION_RANGE" som er definert øverst """
    def update_infection_status(self, sprite_group):
        if self.color == (255, 0, 0): #Infected
            self.sick_time += 1
            if self.sick_time > RECOVERY_TIME * STEPS_PER_SECOND:
                self.color = (0, 0, 255) #Recovered
            for sprite in sprite_group:
                if sprite != self:
                    distance = Vector2.distance_to(self.position, sprite.position)
                    if distance < self.infection_range:
                        if sprite == Sykebil:
                            self.color = (0, 0, 255) #Recovered
                        if sprite == Surrehode:
                            self.color = (255, 0, 0) #Infected

    """Funksjon som returnerer prosentandelen av de som bruker munnbind"""
    def antall_munnbind(self, sprite_group):
        length = len(sprite_group)

        percentage = (length / NUMBER_OF_PEOPLE) * 100

        return percentage


    """Tanken med metoden er at personer med munnbind vil holde seg unna personer uten munnbind.
       På den måten vil sannsynligheten for å bli smittet/smitte andre bli mindre"""
    def move(self, sprite_group):
        movement_y = random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE)
        movement_x = random.randint(-MOVEMENT_RANGE, MOVEMENT_RANGE)
        movement_vector = pygame.math.Vector2(movement_x, movement_y)
        
        self.position += movement_vector
        
        for surrehode in sprite_group:
            distance = Vector2.distance_to(self.position, surrehode.position)
            if distance < INFECTION_RANGE:
                difference_vector = surrehode.position - self.position
                movement_direction = difference_vector.normalize()
                self.position += movement_direction

        #Looper objektet gjennom veggene
        if self.x < 0:
                self.x = SCREEN_WIDTH + self.x
        if self.x > SCREEN_WIDTH:
                self.x = self.x % SCREEN_HEIGHT
        if self.y < 0:
                self.y = SCREEN_HEIGHT + self.y
        if self.y > SCREEN_HEIGHT:
                self.y = self.y % SCREEN_HEIGHT
                

#### Main loop ####
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    update = Update()
    #make_person() oppretter en instans av en klasse og legger de til i sprite groups
    for _ in range(NUMBER_OF_PEOPLE):
        update.make_person()

    #Oppdaterer og tegner sprites fra sprite groups
    sykebil_sprites.update(screen)
    sykebil_sprites.move() #sykebil klassen har ikke en egen "move" metode og må derfor bruke "Update" sin "move" metode
    sykebil_sprites.draw(screen)

    surrehoder_sprites.update(screen)
    surrehoder_sprites.draw(screen)

    surrehoder_munnbind_sprites.update(screen)
    surrehoder_munnbind_sprites.draw(screen)

    clock = pygame.time.Clock()
    while True:
        clock.tick(STEPS_PER_SECOND)
        screen.fill((0, 0, 0))          

        pygame.display.flip()