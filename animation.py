import pygame


class AnimateSprite(pygame.sprite.Sprite):
    
    def __init__(self, name):
        super().__init__()
        
        # importer l'image du joueur 
        self.sprite_sheet = pygame.image.load(f'images/{name}.png')
        
        # vitesse du joueur
        self.speed = 2
        
        # clock pour compter le nombre de tour de boucle
        self.clock = 0
        
        # index de l'animation a utiliser
        self.animation_index = 0
        
        
        self.anim = {
            
            "down": self.get_images(0),
            "left": self.get_images(32),
            "right": self.get_images(64),
            "up": self.get_images(96)
        }
    
    def change_animation(self, name):
        """change l'animation de marche selon la direction

        Args:
            name (str): nom de la direction dans laquelle on vas
        """
        if self.anim.get(name) is not None:
            self.image = self.anim.get(name)[self.animation_index]
            self.image.set_colorkey([0,0,0])   
            self.clock += self.speed * 8 
            if self.clock >= 100:
                self.animation_index += 1
                if self.animation_index >= len(self.anim.get(name)):
                    self.animation_index = 0
                    self.clock = 0
    
    def get_images(self, y):
        images = []
        
        for i in range(0, 3):
            x = i*32
            image = self.get_image(x, y)
            
            images.append(image)
            
        return images
        

    def get_image(self, posSpriteX, posSpriteY):
        """permet de charger le sprite voulue dans la grille de sprite

        Args:
            x (int): position de du sprite voulu sur la grille de sprite en positon x
            y (int): position de du sprite voulu sur la grille de sprite en positon y

        Returns:
            _type_: renvoie l'image qui a etait pris
        """
        # image sur une surface de 32 par 32
        image = pygame.Surface([32,32])
        image.blit(self.sprite_sheet, (0, 0), (posSpriteX, posSpriteY, 32, 32))
        return image