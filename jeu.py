# main
from class_Personnages1 import Player_1
from class_Personnages1 import Player_2
from class_Personnages1 import obstacle
from design import *
import sys
import pygame
pygame.mixer.init()

class Game() :
    """Cette classe contient la boucle principale"""
    ecran = pygame.display.set_mode((0,0),pg.FULLSCREEN)
    clock = pygame.time.Clock()

    pygame.display.set_caption("Urban Peta")
    Taille_fen = (1200, 650)
    mx, my = pygame.mouse.get_pos()
    obstacle1 = obstacle
    
    def __init__(self,perso1,perso2):
        """definition de la classe Game"""
        #persos 
        self.persos = ["capybara","chinchilla","e","loup","raton","souris","pp","fa","gf","ac"]
        self.path_persos =  [[3,2,2,2,2,1,1],[3,4,2,2,2,1,1],[2,2,2,3,2,1,1],[3,2,2,2,2,1,1],[3,2,2,3,2,2,1],[3,3,3,2,2,3,1],[3,2,2,2,2,1,1],[3,2,2,3,2,1,1],[3,2,2,2,2,1,1],[3,2,2,2,2,1,1]]
        self.donnees = [[], [], [], [], [], [], []]
        self.path = ["_idle","_attaque_haut", "_attaque_bas", "_saut","_marche","_garde", "_degat"]
        self.sol = pg.image.load("sol.png")
        self.sol_rect = self.sol.get_rect() 
        self.sol = pg.transform.scale(self.sol,(pg.Surface.get_width(self.ecran),pg.Surface.get_height(self.ecran)))
        
    #selection des deux persos
        #joueur 1
        index1 = self.persos.index(perso1)
        i = 0
        for j in self.path_persos[index1] :
            for p in range(j) :
                self.donnees[i].append(perso1  + self.path[i] + str(p + 1) + ".png")
            i += 1

        self.girafe = Player_1(self.donnees)
        self.donnees = [[], [], [], [], [], [], []]
        #joueur2
        index2 = self.persos.index(perso2)
        i=0
        for j in self.path_persos[index2] :
            for p in range(j) :
                self.donnees[i].append(perso2  + self.path[i] + str(p + 1) + ".png")
            i += 1
        self.chinchilla = Player_2(self.donnees)
        self.donnees = [[], [], [], [], [], [], []]
        
    def draw(self):
        """la fonction draw 'dessine' la girafe, la chinchilla et l'écran noir"""   
        touches =  pygame.key.get_pressed()     
        self.ecran.fill((91, 125, 255)) #ecran noir
        self.ecran.blit(self.sol,self.sol_rect)
        pygame.draw.rect(self.ecran, (0, 0, 0), self.obstacle1,4)
        if touches[pygame.K_p]: #Pour montre la hitbox des personnages 
            pygame.draw.rect(self.ecran,(255,0,0),self.girafe,4)
            pygame.draw.rect(self.ecran,(255,0,0),self.chinchilla,4)
        self.girafe.draw(self.ecran,self.chinchilla)
        self.chinchilla.draw(self.ecran,self.girafe)
        pygame.display.update()


    def play(self): #main loop
        """la fonction play execute le programme de base en utilisant une boucle """
        execute = True
        while execute:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    execute = False    
            self.draw()
            if self.girafe.collision(self.chinchilla):
                self.girafe.retroceso()
            if self.chinchilla.collision(self.girafe):
                self.chinchilla.retroceso()
            
            self.girafe.mouvements()  
            self.chinchilla.mouvements()
            self.girafe.attaque()
            self.chinchilla.attaque()
            self.girafe.garde_active()
            self.chinchilla.garde_active()
            print(self.girafe.vie)
            print(self.chinchilla.vie)
            

            if self.girafe.vie <= 0:
                execute = False 
                print('Joueur 1 tu as gagné !')            
            elif self.chinchilla.vie <= 0:
                execute = False 
                print('Joueur 2 tu as gagné !')
            elif self.girafe.vie <= 0 and self.chinchilla.vie <= 0:
                print('Bande de nulos')

            pygame.display.update()
            self.clock.tick(60)


start = Initialisation()



if __name__ == "__main__":
    pygame.init()
    perso1 = start.lancement()
    start = Initialisation(True)
    perso2 = start.lancement()
    g = Game(perso1,perso2)
    g.play()
    pygame.quit()
    sys.exit()