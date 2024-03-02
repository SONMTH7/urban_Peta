"""
selection persos
timer
"""
from sys import exit
import pygame as pg
from time import sleep

pg.init()

ecran = pg.display.set_mode((0, 0), pg.FULLSCREEN)
ecran_rect = pg.Surface.get_rect(ecran)
center_ecran_x = pg.Surface.get_width(ecran)/2
center_ecran_y = pg.Surface.get_height(ecran)/2
police = pg.font.Font("font.otf", 95)
petite_police = pg.font.Font("font.otf", 55)
#limite framerate
pg.time.Clock().tick(60)
pg.mixer.init

#################################################################################################

def accueil (screen = ecran, font = police, mini_font = petite_police):
    """
    Hyp: affiche l'ecran d'acceuil et joue la musique
    """
    #variable spatiale
    screen_rect = pg.Surface.get_rect(screen)
    center_ecran_x = pg.Surface.get_width(ecran)/2
    #genere background
    background=pg.image.load("background.png")
    background_rect = background.get_rect()
    background = pg.transform.scale(
        background, (screen_rect.width, screen_rect.height))
    screen.blit(background,background_rect)
    #ajoute texte
    text = font.render("Urban Peta", False, (255,33,28))
    instruction = mini_font.render("Appuyer sur n'importe quelle touche pour continuer", False, (255,33,28))
    screen.blit(text, text.get_rect(
        center=((center_ecran_x, screen_rect.bottom - text.get_height()))))
    carre_instruction = instruction.get_rect(
        center=((center_ecran_x, screen_rect.bottom - text.get_height()*0.5)))
    screen.blit(instruction, carre_instruction)
    #musique
    pg.mixer.music.load("musique_ecran_daccueil.mp3")
    pg.mixer.music.play(-1)

    
#################################################################################################

class Box:
    """
    Hyp: affiche un rectangle sur l'ecran qui indique quel personnage le joueur choisit
    """
    def __init__(self, screen = ecran):
        #ecran
        self.screen = screen
        self.screen_rect = pg.Surface.get_rect(screen)
        self.sprite = pg.image.load("selection.png")
        self.sprite = pg.transform.scale(self.sprite,
             (round(pg.Surface.get_width(self.screen)/10.5)+30,
             round(pg.Surface.get_height(self.screen)/4.5)+28))
        #mouvement
        self.x = round(pg.Surface.get_width(self.screen)*0.035)+20
        self.y = round(pg.Surface.get_height(self.screen)*0.53)+10
        self.mouvement_x = (round(pg.Surface.get_width(self.screen)*0.06 + 1)*2)
        self.mouvement_y = round(pg.Surface.get_width(self.screen)*0.06 + 1)*0.5
        self.up = False
        self.right = 0
        self.hitbox =  self.sprite.get_rect(bottomleft=((self.x , self.y)))
        
        #sprite de l'ecran
        self.perso = ["capybara", "chinchilla", "e", "loup", "raton", "souris",'pp',"fa","gf","ac"]
        self.idle = 1
        
        #timer
        self.idle_timer = pg.time.get_ticks()
                
    def update(self,mov):
        """
        modifie la position de la boite sur l'ecran de selection 

        """
        if mov[pg.K_UP] == True and self.up == True :
            self.y -= (self.mouvement_x *1.25)
            self.up = False
            
        elif mov[pg.K_DOWN] == True and self.up == False and self.right <= 4 :
            self.y += (self.mouvement_x *1.25)
            self.up = True
        
        elif mov[pg.K_RIGHT] == True and self.right < 4:
            if not self.up :
                self.x += self.mouvement_x
                self.right += 1
            elif self.up and self.right< 4:
                self.x += self.mouvement_x
                self.right += 1
            
        elif mov[pg.K_LEFT] == True and self.right > 0 :
            self.x -= self.mouvement_x
            self.right -=1
        
        self.hitbox =  self.sprite.get_rect(bottomleft=((self.x , self.y)))
        self.screen.blit(self.sprite, self.hitbox)
        sleep(0.1)
        
    def timer(self):
        """
        Genere une variable qui compte depuis combien de temps l'ecran de selection est affiche
        """
        self.idle_timer = pg.time.get_ticks()
        
    def position(self):
        """
        Renvoie la position de la case sur l'écran
        """
        return [self.right, self.up]
    
    def animation(self):
        """
        Definie le portrait qu'on anime
        """
        if  pg.time.get_ticks() - self.idle_timer > 50 :
            self.idle += 1
            if self.idle > 3 :
                self.idle = 1
            self.timer()
            
        return str(self.idle)
        
    
    def portrait(self):
        """
        Genere les portraits de selection sur l'ecran de persos
        """
        index = 0
        gap = 0
        for i in self.perso :
            visage=pg.image.load('img1/' + i + "_idle" + self.animation() + ".png")
            visage_rect = visage.get_rect(bottomleft=((
                round(pg.Surface.get_width(self.screen)*0.035) + 15 + self.mouvement_x * index , 
                round(pg.Surface.get_height(self.screen)*0.53) - 140 + 5 * gap)))
            visage = pg.transform.scale(visage, (visage.get_width() * 3, visage.get_height() * 3))
            self.screen.blit(visage, visage_rect)
            index += 1
            if index > 4 :
                index = 0
                gap = self.mouvement_y
                
                
    def perso_selectionne(self):
        """
        Renvoie le perso sur laquelle se trouve la case
        """
        pos = self.position()
        if pos[1] :
            pos[0] += 5
        return self.perso[pos[0]]
        
#################################################################################################

def ecran_selection(placement, screen = ecran, font = police ):
    """
    Hyp: affiche l'ecran de selection
    """
    screen_rect = pg.Surface.get_rect(screen)
    background=pg.image.load("accueil\ecran_accueil.png")
    background_rect = background.get_rect()
    background = pg.transform.scale(
        background, (screen_rect.width, screen_rect.height))
    
    if placement[1]:
        placement[0] += 5

    liste_perso = ["capybara (loutre)", "chinchilla (lapin)", "elephant (girafe)", "loup (mouton)", 
                   "raton laveur (panda roux)", "souris (chauve-souris)",'poule (paon)','flamant (autruche)','gorille sapiens',"alpaga (cheval)"]
    #font
    petite_police = pg.font.Font("font.otf", 60)
    text = petite_police.render(liste_perso[placement[0]], False, (255,255,255))
    
    screen.blit(background,background_rect)
    screen.blit(text, text.get_rect(
        center=((center_ecran_x*0.65, screen_rect.bottom - 5.7*text.get_height()))))
    
#################################################################################################

class Initialisation:
    
    def __init__(self,skip = False):
        self.boite = Box()
        if not skip :
            self.attente = True
        else :
            self.attente = False
        self.jeu = False
        
        
    def activite(self, evenement,cle):
        if cle[pg.K_SPACE] and not self.attente:
            self.jeu = True
            pg.mixer.music.stop()
            sleep(0.1)
            self.boite.timer()            
            
        if evenement.type == pg.KEYDOWN and self.attente:
            self.attente = False
            
        
    def ecran(self):
        if self.attente :
            accueil()
        else : 
            ecran_selection(self.boite.position())
            self.boite.update(pg.key.get_pressed())
            self.boite.portrait()
            
    def lancement(self):
        while not self.jeu :
            for event in pg.event.get() :
                 if pg.event.get() == pg.QUIT:
                     pg.quit()
                     exit()
                 
                 self.activite(event,pg.key.get_pressed())
                 
            self.ecran()
                 
 
            pg.display.update()
        return self.boite.perso_selectionne()
            
#################################################################################################  