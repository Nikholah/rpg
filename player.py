import pygame

from animation import AnimateSprite



class Entities(AnimateSprite):
    """Classe joueur qui sert a controler les différente actions du joueur

    Methode:
        update (): Permet de mettre a jour la position du joueur
        get_image (x, y --> int): Permet d'afficher l'image du joueur
        change_animation(name --> str): Permet de changer l'animation du joueur selon la direction
        move_(...) : permet de faire bouger le joueur selon les direction indiquer
    """
    
    def __init__(self, name, posJoueurX , posJoueurY ):
        """Sert a initialier le joueur

        Args:
            posX (int): position initial du joueur en x
            posY (int): position initial du joueur en y
        """
        super().__init__(name)
        
        
        # fait appelle a la méthode get_image selon les differente direction
        
        
        self.image = self.get_image(0, 0)
        
        # enleve le fond noir de l'image 
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
                
        # position du joueur 
        self.position = [posJoueurX, posJoueurY]
        
        # position des pied du joueur
        self.feet = pygame.Rect(0, 0, self.rect.width // 2, 12)
        
        # copier la position du joueur
        self.oldPosition = self.position.copy()
        
    def save_location(self):
        """copie la localisation pour en garder une ancienne
        """
        self.oldPosition = self.position.copy()
            
    def move_right(self):
        """permet de bouger vers la droite
        """
        self.change_animation("right")
        self.position[0] += self.speed
                
    def move_left(self):
        """permet de bouger vers la gauche
        """
        self.change_animation("left")
        self.position[0] -= self.speed
        
    def move_up(self):
        """permet de bouger vers le haut
        """
        self.change_animation("up")
        self.position[1] -= self.speed
        
    def move_down(self):
        """permet de bouger vers le bas
        """
        self.change_animation("down")
        self.position[1] += self.speed        
       
    def update(self):
        """met a jour la position du joueur 
        """
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
    def move_back(self):
        """permet de revenir en arrière
        """
        self.position = self.oldPosition
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
                
    
    
class Player(Entities):
    
    def __init__(self):
        super().__init__("player", 0, 0)
        
class NPC(Entities):
    
    def __init__(self, name, nb_points, speed=1):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.points = []
        self.name = name
        self.speed = speed
        self.current_point = 0
        
    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1
        
        if target_point >= self.nb_points:
            target_point = 0
        
        current_rect = self.points[current_point]
        target_rect = self.points[target_point]
        
        if current_rect.y < target_rect.y and abs(current_rect.x - current_rect.x ) < 3:
            self.move_down()
            
        elif current_rect.y > target_rect.y and abs(current_rect.x - current_rect.x ) < 3:
            self.move_up()
            
        elif current_rect.x < target_rect.x and abs(current_rect.y - current_rect.y ) < 3:
            self.move_right()
            
        elif current_rect.x > target_rect.x and abs(current_rect.y - current_rect.y ) < 3:
            self.move_left()
            
        if self.rect.colliderect(target_rect):
            self.current_point = target_point
            
    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()
        
    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
        