import pygame
from pygame import Vector2
from CONFIG import Game_traits
from CONFIG import Player1_traits
from CONFIG import Player2_traits
from player1 import Player1
from player2 import Player2
from bullet import Bullet
from obstacles import Planet
from obstacles import Fuel_icon
pygame.init()

""" *Game-class:
    -Contains six methods checking for collisions between players, obstacles and bullets using "pygame.sprite.spritecollide()" and "pygame.sprite.groupcollide()".
    -If collisions are detected players, bullets or obstacles are removed and respawned, scores are updated and sound effects are played using pygame's functions.

    -"Score" method and "players refuel" methods blits their current score and fuel level to the screen
    -If one of the players score is more than 10, a message saying "Player(X) wins!" is blitted to the screen

    -All of these methods are called upon in the "game_updates" method which is updated in the main program loop
"""
class Game:
    def __init__(self):
        ########## CREATING CONFIG-OBJECT TO ACCESS VARIABLES FROM CONFIG-FILE ##########
        self.game_traits = Game_traits()
        self.player1_traits = Player1_traits()
        self.player2_traits = Player2_traits()

        ########## TRAITS FOR GAME ##########
        self.screen_width = self.game_traits.SCREEN_WIDTH
        self.screen_heigth = self.game_traits.SCREEN_HEIGHT
        self.screen = self.game_traits.SCREEN
        self.background = self.game_traits.BACKGROUND
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_heigth))
        self.background = self.background.convert_alpha()

        self.clock = pygame.time.Clock()
        self.background_music = self.game_traits.BACKGROUND_MUSIC
        self.explosion_sound = self.game_traits.EXPLOSION_SOUND 
        
        self.p1_score = 0
        self.p2_score = 0

        ########## CREATING SPRITE GROUPS ##########
        self.player1_group = pygame.sprite.Group()
        self.player2_group = pygame.sprite.Group()
        self.player1_bullets = pygame.sprite.Group()
        self.player2_bullets = pygame.sprite.Group()
        self.planet_group = pygame.sprite.Group()
        self.fuel_icon_group1 = pygame.sprite.Group()
        self.fuel_icon_group2 = pygame.sprite.Group()

        ########## CREATING OBJECTS ##########
        self.player1 = Player1(self.player1_bullets, self.player1_traits.POSITION[0], self.player1_traits.POSITION[1])
        self.player2 = Player2(self.player2_bullets, self.player2_traits.POSITION[0], self.player2_traits.POSITION[1])
        self.planet_obstacle = Planet()
        self.fuel_icon1 = Fuel_icon(self.player1_traits.POSITION[0] + 50, self.player1_traits.POSITION[1])
        self.fuel_icon2 = Fuel_icon(self.player2_traits.POSITION[0] - 50, self.player2_traits.POSITION[1])
        
        ########## ADDING OBJECTS TO SPRITE GROUPS ##########
        self.player1_group.add(self.player1)
        self.player2_group.add(self.player2)
        self.planet_group.add(self.planet_obstacle)

        self.fuel_icon_group1.add(self.fuel_icon1)
        self.fuel_icon_group2.add(self.fuel_icon2)

        ########## PLAYING MUSIC ##########
        pygame.mixer.music.play(loops=-1, start=0.0)
        pygame.mixer.music.set_volume(1.0)

    def p1_shot_p2(self):
        collide_list = pygame.sprite.spritecollide(self.player2, self.player1_bullets, True)

        if len(collide_list) > 0:
            self.p1_score += 1
            self.explosion_sound.play()
            self.player2_group.remove(self.player2)
            self.player2 = Player2(self.player2_bullets, self.player2_traits.POSITION[0], self.player2_traits.POSITION[1])
            self.player2_group.add(self.player2)

    def p2_shot_p1(self):
        collide_list = pygame.sprite.spritecollide(self.player1, self.player2_bullets, True)
        
        if len(collide_list) > 0:
            self.p2_score += 1
            self.explosion_sound.play()

            self.player1_group.remove(self.player1)
            self.player1 = Player1(self.player1_bullets, self.player1_traits.POSITION[0], self.player1_traits.POSITION[1])
            self.player1_group.add(self.player1)
    
    def player_hit_player(self):
        collide_list = pygame.sprite.spritecollide(self.player1, self.player2_group, True)

        if len(collide_list) > 0:
            self.p1_score -= 1
            self.p2_score -= 1
            self.explosion_sound.play()
            self.player1_group.remove(self.player1)
            self.player2_group.remove(self.player2)

            ##### RESPAWNING PLAYERS #####
            self.player1 = Player1(self.player1_bullets, self.player1_traits.POSITION[0], self.player1_traits.POSITION[1])
            self.player1_group.add(self.player1)

            self.player2 = Player2(self.player2_bullets, self.player2_traits.POSITION[0], self.player2_traits.POSITION[1])
            self.player2_group.add(self.player2)
    
    def player1_hit_planet(self):
        collide_list = pygame.sprite.spritecollide(self.player1, self.planet_group, True)

        if len(collide_list) > 0:
            self.p1_score -= 1
            self.explosion_sound.play()
            self.player1_group.remove(self.player1)

            ##### RESPAWNING PLAYER AND PLANET #####
            self.player1 = Player1(self.player1_bullets, self.player1_traits.POSITION[0], self.player1_traits.POSITION[1])
            self.player1_group.add(self.player1)
        
            self.planet_obstacle = Planet()
            self.planet_group.add(self.planet_obstacle)
    
    def player2_hit_planet(self):
        collide_list = pygame.sprite.spritecollide(self.player2, self.planet_group, True)

        if len(collide_list) > 0:
            self.p2_score -= 1
            self.explosion_sound.play()
            self.player2_group.remove(self.player2)

            ##### RESPAWNING PLAYER AND PLANET #####
            self.player2 = Player2(self.player2_bullets, self.player2_traits.POSITION[0], self.player2_traits.POSITION[1])
            self.player2_group.add(self.player2)

            self.planet_obstacle = Planet()
            self.planet_group.add(self.planet_obstacle)

    def bullets_hit_planet(self):
        collide_list1 = pygame.sprite.groupcollide(self.player1_bullets, self.planet_group, True, False)
        collide_list2 = pygame.sprite.groupcollide(self.player2_bullets, self.planet_group, True, False)

        if len(collide_list1) > 0:
            self.explosion_sound.play()
            
        if len(collide_list2) > 0:
            self.explosion_sound.play()
    
    def player1_refuel(self):
        collide_list = pygame.sprite.spritecollide(self.player1, self.fuel_icon_group1, False)

        if len(collide_list) > 0:
            self.player1.fuel_tank = self.player1_traits.FUEL_TANK

    def player2_refuel(self):
        collide_list = pygame.sprite.spritecollide(self.player2, self.fuel_icon_group2, False)

        if len(collide_list) > 0:
            self.player2.fuel_tank = self.player2_traits.FUEL_TANK

    def score(self):
        p2_score = self.p2_score
        p1_score = self.p1_score

        ##### SCORE #####
        font = pygame.font.Font(None, 70)
        text = font.render(str(p1_score), 1, (255,255,255))
        self.screen.blit(text, ((self.game_traits.SCREEN_WIDTH - 90),10))
        text = font.render(str(p2_score), 1, (255,255,255))
        self.screen.blit(text, (10,10))

        if p1_score >= 10:
            win = pygame.font.Font(None, (200))
            text = win.render(str("PLAYER 1 WINS!"), 1, (0, 255, 0))
            self.screen.blit(text, (10, 200))
        if p2_score >= 10:
            win = pygame.font.Font(None, (200))
            text = win.render(str("PLAYER 2 WINS!"), 1, (0, 255, 255))
            self.screen.blit(text, (10, 200))

        
        ##### BLITTING FUEL TO SCREEN #####
        font = pygame.font.Font(None, 70)
        if self.player1.fuel_tank >= 0:
            text = font.render(str(self.player1.fuel_tank), 1, (255, 0, 0))
            self.screen.blit(text, ((self.game_traits.SCREEN_WIDTH - 90), 70))
        else:
            text = font.render(str(0), 1, (255, 0, 0))
            self.screen.blit(text, ((self.game_traits.SCREEN_WIDTH - 90), 70))

        if self.player2.fuel_tank > 0:
            text = font.render(str(self.player2.fuel_tank), 1, (255, 0, 0))
            self.screen.blit(text, (10, 50))
        else:
            text = font.render(str(0), 1, (255, 0, 0))
            self.screen.blit(text, (10, 50))

    def game_updates(self):
        self.p1_shot_p2()
        self.p2_shot_p1()
        self.player_hit_player()
        self.player1_hit_planet()
        self.player2_hit_planet()
        self.player1_refuel()
        self.player2_refuel()
        self.score()
        self.bullets_hit_planet()
            
    """ *Program loop:
        -Runs the program and stops it if escape key is pressed or game-window is closed
        -Contains time that runs the program in 60 FPS using the pygame.time.Clock() function
        -Displays a caption "Mayhem" on the screen window
        -Updates ALL the sprites and draws them using the "sprite.update()" and "sprite.draw()" functions
        -Runs the program using Pythons "if __name__ == "__main__":" idiom
    """
    def programloop(self):
        running = True
        while running:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if keys[pygame.K_ESCAPE]:
                    running = False
                if event.type == pygame.QUIT:
                    running = False
            
            self.clock.tick(self.game_traits.FPS)
            self.screen.blit(self.background, (0,0))
            pygame.display.set_caption("MAYHEM")     

            ########## UPDATING AND DRAWING SPRITES ##########
            self.player1_group.update(self.screen)
            self.player1_group.draw(self.screen)   

            self.player2_group.update(self.screen)
            self.player2_group.draw(self.screen)

            self.player1_bullets.update(self.screen)
            self.player1_bullets.draw(self.screen)

            self.player2_bullets.update(self.screen)
            self.player2_bullets.draw(self.screen)

            self.planet_group.update(self.screen)
            self.planet_group.draw(self.screen)

            self.fuel_icon_group1.update(self.screen)
            self.fuel_icon_group1.draw(self.screen)

            self.fuel_icon_group2.update(self.screen)
            self.fuel_icon_group2.draw(self.screen)

            ########## UPDATING GAME METHODS ##########
            self.game_updates()

            ########## UPDATE DISPLAY ##########
            pygame.display.update()


if __name__ == "__main__":
    sim = Game()
    sim.programloop()