import pygame
import pytmx
import pyscroll
from pytmx.util_pygame import load_pygame
from player import Player
from maps import Mapmanager

class Game:
    """gère tout se qui concerne le jeu en lui même
    
    Methode:
        handle_input : recupere les touche saisie et agis en fonction
        update : met a jour les deplacement du joueur
        run : fait tourner le jeu
    """
    
    def __init__(self):
        """initialise la fenetre puis affiche la map et le joueur 
        """
        
        # creation de la fenetre du jeu

        # definir la dimention 
        fenetreHauteur = 800 
        fenetreLargeur = 600
        self.screen = pygame.display.set_mode((fenetreHauteur, fenetreLargeur))
        
        # definir son nom
        pygame.display.set_caption("Rpg aventure")
        
        # generer le joueur 
        self.player = Player()
        
        # gerer la map grace a la class mapmanager
        self.map_manager = Mapmanager(self.screen, self.player)
        
    def handle_input(self):
        """recupere toute les inputs et agis en fonction
        """
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_UP]:
            self.player.move_up()
            
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        
    def update(self):
        """met a jour les deplacement du joueur 
        """
        self.map_manager.update()
        
    def run(self):
        """fait tourner le jeu et prend en compte tout les évènements 
        """

        # boucle du jeu
        running = True
        
        # permet de limiter le nombre de fps
        clock = pygame.time.Clock()
        
        while running:
            
            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            pygame.display.flip()
            
            for event in pygame.event.get():
                # verifier si le jouer a quitter la fenetre
                if event.type == pygame.QUIT:
                    running = False
                    
            clock.tick(60)
                    
        pygame.quit()