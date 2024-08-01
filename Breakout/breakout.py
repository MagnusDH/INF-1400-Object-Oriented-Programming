import pygame #importerer pygame bibliotek
pygame.init() #setter opp pygame sine funksjonen og gjør dem klar


screen_size_x = 830                                                     #Bredden på skjermen
screen_size_y = 500                                                     #Høyden på skjermen
screen = pygame.display.set_mode((screen_size_x, screen_size_y), 0, 32) #Oppretter skjermen
pygame.display.set_caption("BREAKOUT")                                  #Setter et navn på displaybildet når programmet kjører
background_filename = "universe.png"                                    #Filnavnet på bakgrunnsbildet som brukes
game_over_filename = "game_over.jpg"                                    #Filnavnet til game over bildet som skal brukes
win_filename = "win.jpg"
music = "take_on_me.mp3"
music2 = "MEGALOVANIA.mp3"

pygame.mixer.music.load(music)
pygame.mixer.music.play(loops=-1, start=0.0)
pygame.mixer.music.set_volume(1.0)

clock = pygame.time.Clock()


background = pygame.image.load(background_filename)                             #Laster opp bakgrunnsbildet
background = pygame.transform.scale(background, (screen_size_x, screen_size_y)) #Skalerer bakgrunnsbildet så det passer skjermen
background = background.convert()                                               #Konverterer bildet som gjør det enklere for python å bruke/kjøre

win = pygame.image.load(win_filename)
win = pygame.transform.scale(win, (screen_size_x, screen_size_y))
win = win.convert()

game_over = pygame.image.load(game_over_filename)                               #Laster opp game over bildet
game_over = pygame.transform.scale(game_over, (screen_size_x, screen_size_y))   #Skalerer game over bildet så det passer skjermen
game_over = game_over.convert()                                                 #Konverterer bildet som gjør det enklere for python å bruke/kjøre

class Paddle: #En klasse med paddle sine attributter
    def __init__(self):
        self.x = screen_size_x / 2          #Rektanglet sin posisjon x (høyre/venstre)
        self.y = screen_size_y - 20             #Rektanglet sin posisjon y (opp/ned)
        self.width = 150                    #bredden på rektanglet
        self.height = 20                    #Høyden på rektangletimport pygame #importere
        self.speed = 5                      #Farten til rektanglet
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height) #oppretter rektangelet med spesifikke verdier

    
    def Paddle_move(self, events):
        keys = pygame.key.get_pressed()                         #Sjekker om en tastaturknapp er trykket
        
        if keys[pygame.K_LEFT] and paddle1.rectangle.left > 0:  #Er venstre piltast trykket og paddle ikke er utfor skjermen
                self.rectangle.x -= self.speed                  #Paddle flytter seg til venstre
        
        if keys[pygame.K_RIGHT] and paddle1.rectangle.right < screen_size_x:    #Er høyre piltast trykket og paddle ikke er utfor skjermen
                self.rectangle.x += self.speed                                  #Paddle flytter seg til høyre
        

    def draw(self): #Funksjon som tegner rektanglet (paddle)
        color_silver = (192, 192, 192)                          #Fargen til rektanglet
        pygame.draw.rect(screen, color_silver, self.rectangle)  #Selve funksjonen som tegner opp paddle, "screen", "color", "self.rectangle(x,y,width,height)"

class Block: #En klasse med blokk sine attributter

    def __init__(self, x, y):
        self.x = x                                                          #Rektanglet sin posisjon x (høyre/venstre)
        self.y = y                                                          #Rektanglet sin posisjon y (opp/ned)
        self.width = 100                                                    #Rektanglet sin bredde
        self.height = 50                                                    #Rektanglet sin høyde
        self.block = pygame.Rect(self.x, self.y, self.width, self.height)   #Oppretter rektangel med en spesifikk posisjon, bredde og høyde

    def draw(self): #Funksjon som tegner block
        
        pygame.draw.rect(screen, (0,0,225), self.block) #tegner opp blokken
                        

class Ball: #En klasse med ballen sine attributter
    def __init__(self):
        self.radius = 10                                        #Radius til sirklen
        self.center = [(screen_size_x/3), (screen_size_y / 2)]  #Posisjonen til sirklen på skjermen 
        self.speed_x = 1                                      #Hastigheten til sirklen
        self.speed_y = 1                                      #Hastigheten til sirklen
        self.color = (192, 192, 192)                            #Fargen til ballen (Sølv)
        

    def move(self): #Funksjon som flytter på ballen
        self.center[0] += self.speed_x  #Hvor mye x-posisjonen til ballen skal flyttes 
        self.center[1] += self.speed_y  #Hvor mye y-posisjonen til ballen skal flyttes

    def ball_wall_collision(self): #Funksjon som sjekker om ballen treffer kantene av skjermen
        
        if self.center[0] + self.radius >= screen_size_x:   #Hvis ballen treffer høyre del av skjermen
            self.speed_x = -abs(self.speed_x)               #blir hastigheten til ballen negativ

        if self.center[1] + self.radius >= screen_size_y:   #Hvis ballen treffer bunnen av skjermen
            return True                                     #Returnerer funksjonen TRUE, som brukes i PROGRAM LOOPEN

        if self.center[0] - self.radius <= 0:               #Hvis ballen treffer venstre kant av skjermen
            self.speed_x = abs(self.speed_x)                #blir hastigheten til ballen positiv

        if self.center[1] - self.radius <= 0:               #Hvis ballen treffer bunnen av skjermen
            self.speed_y = abs(self.speed_y)                #blir hastigheten til ballen positiv

    def ball_paddle_collision(self, paddle1):   #Funksjon som sjekker om ballen treffer paddle, paddle blir delt i 3 deler
        
        ball_top_side = self.center[1] - self.radius    #Definerer toppen til ballen
        ball_left_side = self.center[0] - self.radius   #Definerer venstre side til ballen
        ball_right_side = self.center[0] + self.radius  #Definerer høyre side til ballen
        ball_bottom_side = self.center[1] + self.radius #Definerer bunnen til ballen
        ball_middle = self.center[0]

        paddle_top_side = paddle1.rectangle.y
        paddle_bottom_side = paddle1.rectangle.y + paddle1.rectangle.height
        paddle_left_side = paddle1.rectangle.x
        paddle_right_side = paddle1.rectangle.x + paddle1.rectangle.width
                

        if ball_bottom_side == paddle_top_side and ball_top_side < paddle_top_side:    #Hvis bunnen av ballen er større enn toppen av block OG toppen av ballen er mindre enn toppen av block
            if ball_middle > paddle_left_side and ball_middle < (paddle_right_side - ((paddle1.rectangle.width/3) * 2)):   #Sjekk om ballen er på venstre del av 1/3 paddle
                self.speed_y *= (-1)
                self.speed_x = -2
                

            if ball_left_side > (paddle_right_side - (paddle1.rectangle.width/3)*2) and ball_right_side < (paddle_right_side - (paddle1.rectangle.width/3)): #Sjekk om ballen er i midtdelen av paddle
                self.speed_y == (-1)
                if self.speed_x == 1 or self.speed_x == 2:
                    self.speed_x = 1
                if self.speed_x == (-1) or self.speed_x == (-2):
                    self.speed_x = -1
                    
            if ball_middle > (paddle_right_side - ((paddle1.rectangle.width/3)*2)) and ball_middle < paddle_right_side:    #Sjekk om ballen er på høyre del av paddle
                self.speed_y *= (-1)
                self.speed_x = 2
                
    
    def ball_block_collision(self, block1): #Funksjon som sjekker om ballen treffer block
        
        ball_top_side = self.center[1] - self.radius    #Definerer toppen til ballen
        ball_left_side = self.center[0] - self.radius   #Definerer venstre side til ballen
        ball_right_side = self.center[0] + self.radius  #Definerer høyre side til ballen
        ball_bottom_side = self.center[1] + self.radius #Definerer bunnen til ballen

        block_top_side = block1.block.y                             #Definerer toppen av block
        block_bottom_side = (block1.block.y + block1.block.height)  #Definerer bunnen av block
        block_left_side = block1.block.x                            #Definerer venstre side av block
        block_right_side = (block1.block.x + block1.block.width)    #Definerer høyre side av block

        
        if ball_top_side <= block_bottom_side and ball_bottom_side >= block_bottom_side: #Kommentar står under
            if ball_right_side <= block_right_side and ball_left_side >= block_left_side:
                self.speed_y *= (-1)
                return True
        #Hvis toppen av ballen er mindre enn bunnen av block OG bunnen av ballen er større enn bunnen av block
        #Sjekk om høyre side av ballen er mindre enn høyre side av block OG venstre side av ballen er større enn venstre side av block
            #farten oppover endres til nedover
            #Returnerer TRUE som brukes i PROGRAM LOOPEN
    

        if ball_left_side <= block_right_side and ball_right_side >= block_right_side:
            if ball_top_side >= block_top_side and ball_bottom_side <= block_bottom_side:
                self.speed_x *= (-1)
                return True
        #Hvis venstre side av ballen er mindre enn høyre side av block OG høyre side av ballen er større en høyre side av block
        #Sjekk om toppen av ballen er mindre enn toppen av block OG bunn av ballen er større enn bunnen av block
            #farten til venstre endres til høyre
            #Returnerer TRUE som brukes i PROGRAM LOOPEN

        if ball_right_side >= block_left_side and ball_left_side <= block_left_side:
            if ball_top_side >= block_top_side and ball_bottom_side <= block_bottom_side:
                self.speed_x *= (-1)
                return True
        #Hvis høyre side av ballen er større enn venstre side av block
        #Sjekk om toppen av ballen er mindre enn toppen av block OG bunn av ballen er større enn bunnen av block
            #farten til høyre endres til venstre
            #Returnerer TRUE som brukes i PROGRAM LOOPEN
        

        if ball_bottom_side >= block_top_side and ball_top_side <= block_top_side:
            if ball_right_side <= block_right_side and ball_left_side >= block_left_side:
                self.speed_y *= (-1)
                return True
        #Hvis bunnen av ballen er større enn toppen av block OG toppen av ballen er mindre enn toppen av block
        #Sjekk om høyre side av ballen er mindre enn høyre side av block OG venstre side av ballen er større enn venstre side av block
            #Farten nedover endres til oppover
            #Returnerer TRUE som brukes i PROGRAM LOOPEN

        return False #Returnerer FALSE om ballen ikke treffer en block
        
            
    def draw(self): #Funksjon som tegner ballen
        pygame.draw.circle(screen, (192,192,192), (int(self.center[0]), int(self.center[1])), self.radius) #tegner opp rektanglet og konverterer "float" til "int"


#OBJECTS
paddle1 = Paddle()  #Oppretter et objekt (Paddle)
ball1 = Ball()      #Oppretter et objekt (Ball)
list_blocks = []    #Lager liste som inneholder blocks

#Loop som lager flere blocks
xpos = 0
ypos = 0

for i in range(3):                      #Kjører en loop for å lage 3 rekker med blocks
    for x in range (8):                 #Loop for å lage 8 blocker bortover
        block1 = Block(xpos, ypos)      #Oppretter objekt (Block)
        list_blocks.append(block1)      #Setter blockene inn i listen list_blocks
        xpos += block1.block.width + 5  #Forandrer x-posisjonen til block
    xpos = 0                         #Oppdaterer x-posisjon for å starte på posisjon 0 igjen
    ypos += 55                       #Oppdaterer y-posisjonen for å lage blocks på neste linje


##################################################################### Program loop #####################################################################################

running = True
while running:
    events = pygame.event.get()
    for event in events:    #sjekker etter "eventer" i programmet
        if event.type == pygame.QUIT:   #Hvis eventet er å lukke programmet
            running = False             #Avslutter programmet

    clock.tick(120)

    screen.blit(background, (0, 0))             #tegner opp bakgrunnsbildet i posisjon 0,0 (blitter bakgrunnsbildet) 

    paddle1.Paddle_move(events)                 #Funksjon som flytter paddle og tar inn "events"
    paddle1.draw()                              #Tegner opp paddle
    
    ball1.move()                                #funksjon som flytter ballen
    if ball1.ball_wall_collision():             #Funksjon som sjekker om ballen treffer vegger, returnerer TRUE om ballen treffer bunn av skjermen
        list_blocks.clear()                         #Om ballen treffer bunnen av skjermen, slettes alle blocker
        screen.blit(game_over, (0, 0))              #Om ballen treffer bunnen av skjermen, tegnes game_over bildet i posisjon 0,0 (blitter bakgrunnsbildet)

    ball1.ball_paddle_collision(paddle1)        #Funksjon som sjekker om ball treffer paddle og tar inn objektet paddle1
    ball1.draw()                                #Tegner opp ball
    
    for block1 in list_blocks:                  #Loop som kjører ball-block-collision funksjonen på alle blockene
        if ball1.ball_block_collision(block1):  #Hvis det er kollisjon mellom ball og block
            list_blocks.remove(block1)          #Fjernes den blocken som ble truffet fra listen
    if len(list_blocks) == 0 and ball1.center[1] < screen_size_y:
        screen.blit(win, (0, 0)) 
    
    
    
    for block1 in list_blocks:                  #Loop som tar inn alle blockene i listen
        block1.draw()                               #Tegner opp blokkene i listen
                      
    pygame.display.update()                     #Oppdaterer skjermen/displayet og tegner alt