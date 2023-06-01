from dataclasses import dataclass
import pygame
import pytmx
import pyscroll
from pytmx.util_pygame import load_pygame
from player import NPC

@dataclass
class Portal:
    """but de stocker le portail
    """
    fromWorld : str
    originPoint : str
    targetWorld : str
    teleportPoint : str

@dataclass
class Map:
    """but de stocker les differentes maps
    """
    name: str
    collisions : list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals : list[Portal]
    npcs : list[NPC]
    
class Mapmanager:
    """Recupere les info des maps et agis en fonction
    """
    
    def __init__(self, screen, player):
        self.maps = {}
        self.currentMap = "world"
        self.screen = screen
        self.player = player
        
        # enregistre la map world et ses different portails
        self.register_map("world", portals=[
            Portal(fromWorld="world", originPoint="enter_house", targetWorld="house", teleportPoint="spawn_house"),
            Portal(fromWorld="world", originPoint="enter_house_2", targetWorld="house2", teleportPoint="spawn_house"),
            Portal(fromWorld="world", originPoint="enter_dungeon", targetWorld="dungeon", teleportPoint="spawn_dungeon")
        ], npcs=[
            NPC("paul", nb_points=4, speed=1), NPC("robin", nb_points=2, speed=2.5)
        ])
        
        # enregistre la map house et ses differents portails    
        self.register_map("house", portals=[
            Portal(fromWorld="house", originPoint="exit_house", targetWorld="world", teleportPoint="enter_house_exit")
        ])
        
        # enregistre la map house2 et ses differents portails
        self.register_map("house2", portals=[
            Portal(fromWorld="house2", originPoint="exit_house", targetWorld="world", teleportPoint="enter_house_2_exit")
        ])
        
        # enregistre la map dungeon et ses differents portails
        self.register_map("dungeon", portals=[
            Portal(fromWorld="dungeon", originPoint="exit_dungeon", targetWorld="world", teleportPoint="enter_dungeon_exit")
        ], npcs=[
            NPC("boss", nb_points=2, speed=2)
        ])
        
        # teleport le joueur a sont point de spawn
        self.teleport_player("spawn")
        self.teleport_npcs()
        
    def check_collisions(self):
        """permet de prendre en compte le collision et d'agir par conséquents
        """
        
        # prend les differents portails et agis en conséquence 
        for portal in self.get_map().portals:
            if portal.fromWorld == self.currentMap:
                point = self.get_object(portal.originPoint)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                
                if self.player.feet.colliderect(rect):
                    copyPortal = portal
                    self.currentMap = portal.targetWorld
                    self.teleport_player(copyPortal.teleportPoint)
        
        # prend le differents group et agis si c'est de collision             
        for sprite in self.get_group().sprites():
            
            if type(sprite) is NPC:
                
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 2
            
            if sprite.feet.collidelist(self.get_collisions()) > -1:
                sprite.move_back()
    
    def teleport_player(self, name):
        """teleporte le joueur a la balise ayant le nom name

        Args:
            name (str): nom de la balise de téléportation
        """
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()
        
    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs
            
            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()
        
    def register_map(self, name, portals=[], npcs=[]):
        """enregistre une map

        Args:
            name (str): nom de la map
            portals (list, optional): liste de tout les portails du monde. Defaults to [].
        """
        # charger la carte
        tmx_data = load_pygame(f"maps/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        
        # generer un liste des collision
        collisions = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        # dessiner le groupe de calque
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer = 6 )
        group.add(self.player)
        
        # recuperer tout les npc de la map
        for npc in npcs:
            group.add(npc)
        
        # creer un objet map
        self.maps[name] = Map(name, collisions, group, tmx_data, portals, npcs)
        
    def get_map(self):
        """recupere la map en cours d'utilisation
        
        Returns:
            les information sur la map en cours d'utilisation
        """
        return self.maps[self.currentMap]
    
    def get_group(self):
        """recupere le group

        Returns:
            le groupe
        """
        return self.get_map().group
    
    def get_collisions(self):
        """recupere les collisions

        Returns:
            les collisions
        """
        return self.get_map().collisions
    
    def get_object(self, name):
        """recupère les objets ayant pour nom name

        Args:
            name (str): nom de l'objets

        Returns:
            les differents information de l'objets
        """
        return self.get_map().tmx_data.get_object_by_name(name)
    
    def draw(self):
        """dessiner l'ecran et le joueur
        """
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)
        
    def update(self):
        """mettre a jour les differente chose
        """
        self.get_group().update()
        self.check_collisions()
        
        for npc in self.get_map().npcs:
            npc.move()