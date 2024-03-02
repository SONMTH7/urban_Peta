import pygame 



#PLAYER_KEYS = {
#    "HAUT": pygame.K_z,
#    "GAUCHE": pygame.K_q,
#    "DROITE": pygame.K_d,
#    "CBAS": pygame.K_r,
#    "CHAUT": pygame.K_t,
#    "GARDE": pygame.K_SPACE,
#}


##################################################################################################################################################
                                                        #Vie des Joueurs 
            
class Vies():
    """Cette class sert à definir la barre de vie des joueurs"""
    def __init__(self,xx, yy, longeur, h, max_vie):
        self.xx = xx
        self.yy = yy
        self.longeur = longeur
        self.h = h 
        self.vie = max_vie
        self.max_vie = max_vie
        
    def prend_degat(self):
        """Cette fonction enlève de la vie au joueur qui a été touché"""
        self.vie -= 3

    def prend_degat_garde(self):
        """Cette fonction enlève de la vie au joueur qui a été touché mais réduit à cause de la garde"""
        self.vie -= 1

    def draw(self,surface):
        """Cette focntion dessine deux barres de coleurs differentes l'une sur l'autre
        La verte representant celle de la vie au complet, quand le joueur perd de la vie celle-ci disparait
        et laisse place à la rouge"""
        ratio = self.vie / self.max_vie
        pygame.draw.rect(surface,'red', (self.xx, self.yy, self.longeur, self.h))
        pygame.draw.rect(surface,'green', (self.xx, self.yy, self.longeur * ratio, self.h))

#######################################################################################################################################
                                        #class Player
class Player():
    """Classe géneral des joueurs"""
    def __init__(self,donnees=[list], PLAYER_KEYS = {"HAUT": pygame.K_z,"GAUCHE": pygame.K_q,
                                                    "DROITE": pygame.K_d,"CBAS": pygame.K_r,
                                                    "CHAUT": pygame.K_t,"GARDE": pygame.K_s}
                                                    ,vie = 100,x = 300 , y = 750,taille = 2):
        """ définition de la classe Player"""
        self.depart = donnees[0]
        self.coups_haut = donnees[1]
        self.coups_bas = donnees[2]
        self.saut = donnees[3]
        self.deplacements = donnees[4]
        self.garde = donnees[5] 
        self.degat = donnees[6]
        self.PLAYER_KEYS = PLAYER_KEYS
        self.x = x
        self.y = y 
        self.vitesse_x = 4
        self.hauteur_y = 0
        self.taille = taille 
        self.cooldown = 200 
        self.cooldown_attaque_faite = 0
        self.temps_collision = 0  
        self.duree_collision = 150
        self.img_index = [0,0,0,0,0,0,0]
        self.vie = vie 
        self.temps = int(pygame.time.get_ticks())
        self.vie_Player1 = Vies(90,150,300,40,vie) # lien avec la classe Vies, c'st la vie du Player 1
        self.vie_Player2 = Vies(800,150,300,40,vie)# lien avec la calsse Vies, c'est la vie du Player 2
        self.creation_sprite()

    def creation_sprite(self):
        """Hyp : Cette fonction permet de charger l'image à partir des documents
            et la rédimensionner """
        image_lists = [self.deplacements, self.coups_bas, self.depart, self.saut, self.coups_haut,self.garde,self.degat]
        for i in range(len(image_lists)):
            if self.img_index[i] < len(image_lists[i]):
                img_path = image_lists[i][self.img_index[i]]
                img_path = 'img1/'+ img_path
                img = pygame.image.load(img_path)
                img = pygame.transform.scale(img, (img.get_width() * self.taille, img.get_height() * self.taille))
                setattr(self, f'img_{i}', img)
    

    def change_img(self,index):
        """ Hyp: Cette focntion permet de passer d'une animation à l'autre de façon fluide""" 
        clock = pygame.time.Clock()
        animation_speed = 5  

        while pygame.time.get_ticks() - self.temps < (60 / animation_speed):
            clock.tick(60)
        self.temps = pygame.time.get_ticks()

        self.img_index[index] = (self.img_index[index] + 1) % len(self.deplacements)
        self.creation_sprite()


    def mouvements(self):
        """HYP: Cette fonction permet les mouvement de nos personnages"""
        touches = pygame.key.get_pressed()
        if touches[self.PLAYER_KEYS["HAUT"]]:
            self.change_img(3)
        elif touches[self.PLAYER_KEYS["GAUCHE"]] or touches[self.PLAYER_KEYS["DROITE"]]:  
            self.change_img(0)
        else:
            self.change_img(2)

        if touches[self.PLAYER_KEYS["GAUCHE"]]:
            self.x -= self.vitesse_x
        elif touches[self.PLAYER_KEYS["DROITE"]]:
            self.x += self.vitesse_x

        if touches[self.PLAYER_KEYS["HAUT"]]:
            self.change_img(3)
            self.y1 = self.y
            self.y -= self.hauteur_y
            self.y = self.y1


    def attaque(self):
        """Hyp: Cette fonction permet les attaques des personnages"""
        touches = pygame.key.get_pressed()
        clock_actuel = pygame.time.get_ticks()

        if touches[self.PLAYER_KEYS["CBAS"]] and clock_actuel - self.cooldown_attaque_faite >= self.cooldown:
            self.change_img(1)
            r_width = self.img_1.get_width() *0.5
            r_height = self.img_1.get_height()
            r_x = self.x + (self.img_1.get_width() - r_width) / 1.9 
            self.cooldown_attaque_faite = clock_actuel
            # Définir le rectangle autour de l'attaque
            return pygame.Rect(r_x, self.y, r_width, r_height)

        elif touches[self.PLAYER_KEYS["CHAUT"]] and clock_actuel - self.cooldown_attaque_faite >= self.cooldown:
            self.change_img(4)
            r_width = self.img_4.get_width() *0.5
            r_height = self.img_4.get_height()
            r_x = self.x + (self.img_4.get_width() - r_width) / 1.9 
            self.cooldown_attaque_faite = clock_actuel
            # Définir le rectangle autour de l'attaque
            return pygame.Rect(r_x, self.y, r_width, r_height)
        else:
            self.change_img(2)
            return pygame.Rect(0, 0, 0, 0)


    def garde_active(self):
        """Hyp :cette fonction renvoie le sprite de degat du personnage"""
        touches = pygame.key.get_pressed()
        if touches[self.PLAYER_KEYS["GARDE"]]:
            self.change_img(5)
            return True 


    def image_act(self,autre_joueur):
        """Cette fonction sert à être utilisé dans la fonction draw car contrairement à la fonction attaque 
            ou mouvements celle-ci retourne des valeurs et pas None comme dans les autres fonctions précédement citées 
        """
        touches = pygame.key.get_pressed()
        if touches[self.PLAYER_KEYS["HAUT"]]:
            return self.img_3
        elif touches[self.PLAYER_KEYS["DROITE"]] or touches[self.PLAYER_KEYS["GAUCHE"]]:
            return self.img_0
        elif touches[self.PLAYER_KEYS["CBAS"]]:
            return self.img_1
        elif touches[self.PLAYER_KEYS["CHAUT"]]:
            return self.img_4
        elif touches[self.PLAYER_KEYS["GARDE"]]:
            return self.img_5
        elif self.collision(autre_joueur):
            return self.img_6
        else:
            return self.img_2
        
    def rect(self):
        """Hyp: Cette fonction crée un Rect autour des players"""
        rect_width = self.img_0.get_width() *0.5
        rect_height = self.img_0.get_height()
        rect_x = self.x + (self.img_0.get_width() - rect_width) / 1.9  # Ajuste la position x pour centrer le rectangle
        return pygame.Rect(rect_x, self.y, rect_width, rect_height)
    
    def collision(self,autre_joueur):
        """Hyp: cette fonction detecte la collision et renvoie True s'il y en a une sinon False"""
        if self.rect().colliderect(autre_joueur.attaque()):
            self.change_img(6)
            self.temps_collision = pygame.time.get_ticks()
            if self.garde_active():
                self.vie_Player1.prend_degat_garde()
                self.vie -= 1
            else:
                self.vie_Player1.prend_degat()
                self.vie -= 3
            return True
        else:
            return False
    
    def retroceso(self):
        '''Cette fonction enregistre le temps puis active une animation tout en faisant que le personnage recule 
        Cette fonction se sert de la fonction collision'''
        temps_actuel = pygame.time.get_ticks()
        temps_ecoule = temps_actuel - self.temps_collision


        if temps_ecoule < self.duree_collision:
            if self.garde_active():
                self.img_index[6] = 0
                self.x -= 4
            else:
                self.change_img(6) 
                self.x -= 2 

    def draw(self, display,autre_joueur):
        """fonction qui nous sert à afficher le changements des sprites et la barre de vie """
        display.blit(self.image_act(autre_joueur), (self.x, self.y))
        self.vie_Player1.draw(display)
        


##################################################################################################################################
                                                #PLAYER_1
    
class Player_1(Player):
    """Classe du Joueur 1, classe enfant de Player"""
    def __init__(self, donnees, PLAYER_KEYS= {
                                    "HAUT": pygame.K_z,
                                    "GAUCHE": pygame.K_q,
                                    "DROITE": pygame.K_d,
                                    "CBAS": pygame.K_r,
                                    "CHAUT": pygame.K_t,
                                    "GARDE": pygame.K_s
                                            }, vie=100, x=200, y=410, taille=2):
        """défintion de la class"""
        super().__init__(donnees,PLAYER_KEYS, vie, x, y, taille)

#####################################################################################################################################################
                                        #PLAYER_2

class Player_2(Player):
    """Classe du joueur 2, classe enfant de Player"""
    def __init__(self,donnees, PLAYER_KEYS ={
                                    "HAUT": pygame.K_o,
                                    "GAUCHE": pygame.K_k,
                                    "DROITE": pygame.K_m,
                                    "CBAS": pygame.K_i,
                                    "CHAUT": pygame.K_u,
                                    "GARDE": pygame.K_l
                                    }, vie = 100, x = 750, y = 410,taille= 2):
        """défintion de la class"""
        self.direction = -1

        super().__init__(donnees,PLAYER_KEYS,vie,x,y,taille)

    def collision(self,autre_joueur):
        """Hyp: cette fonction detecte la collision et renvoie True s'il y en a une sinon False"""

        if self.rect().colliderect(autre_joueur.attaque()):
            self.change_img(6)
            self.temps_collision = pygame.time.get_ticks()
            if self.garde_active():
                self.vie_Player2.prend_degat_garde()
                self.vie -= 1
            else:
                self.vie_Player2.prend_degat()
                self.vie -= 3
            return True
        else:
            return False

    def retroceso(self):
        '''Cette fonction enregistre le temps puis active une animation tout en faisant que le personnage recule 
        Cette fonction se sert de la fonction collision'''
        temps_actuel = pygame.time.get_ticks()
        temps_ecoule = temps_actuel - self.temps_collision


        if temps_ecoule < self.duree_collision:
            if self.garde_active():
                self.img_index[6] = 0
                self.x += 4
            else:
                self.change_img(6) 
                self.x += 2 

    def draw(self, display,autre_joueur):
        """même chose que Player sauf qu'ici on inverse le l'image pour être face au joueur adverse """
        if self.direction == -1:
            display.blit(pygame.transform.flip(self.image_act(autre_joueur), True, False), (self.x, self.y))
        else:
            display.blit(self.image_act(autre_joueur), (self.x, self.y))
        self.vie_Player2.draw(display)
            

    

#########################################################################################################################################
                                                        #OBSTACLE 
        
obstacle = pygame.Rect(20,20,20,20) #carré qui nous permet d'essayer la hitbox