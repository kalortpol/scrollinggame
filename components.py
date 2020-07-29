"""

***     ***     ***     ***     ***     ***     ***     ***
Det går att lägga till en komponent
till ett UID, metoden sköter allt automatiskt.
Komponentklass.add_to_UID(uid: int, component_args)

En instans av komponenten som är unik för UID instantieras
och UIDd som är "world dict" uppdateras med formatet:
        UIDd[uid][komponentnamn] = Komponentklass(args)

Detta sker skyddat, dvs finns det redan en komponent med samma namn
så skrivs inte den över, utan inget händer.
***     ***     ***     ***     ***     ***     ***     ***

***
All hantering sker via separat world_handler-klass. Komponenterna
listför sig automatiskt i components: dict
***

"""
from config import cfg
import pygame


class Component:
    """
    Base class for components.
    Name is set by the first instance to be created
    of sub-class component
    """

    def __init__(self, uid):
        """
        Base clase for all components.
        Functionality:

        Automatically adds each sub-class name to cfg.components as key (component name)
        Automatically adds each sub-class instance in cfg.components[sub-class] = list() (unique component)

        Each component belongs to a uid, call super().__init__(self, uid) in sub-class initiator

        All other functionality, such as attributes, are defined in sub-classes

        :param uid: uid the sub-class instance belongs to
        """

        # this method is inherited, meaning class_name will be sub_class-name
        class_name = self.__class__.__name__

        # make sure sub_class-name exists as key in cfg.components and points to a list
        if not str(class_name) in cfg.components: cfg.components[str(class_name)] = list()

        # add current instance of sub-class to the sub-class list
        if str(class_name) in cfg.components: cfg.components[str(class_name)].append(self)

        # uid this sub-class instance belongs to
        self.uid = uid


class Life(Component):
    """
    Hp and stamina.

    Add changes to hp to the hp-queue (just add a positive or negative value)
    and the Life Processor will make the change at the correct time in the frame
    """
    def __init__(self, uid: int, hp: int, alive: bool, hp_regen=1, stam=100):
        super().__init__(uid)
        self.hp = hp
        self.hp_queue = list()

        self.stam = stam
        self.alive = alive
        self.hp_regen = hp_regen


class Character(Component):
    def __init__(self, uid, name):
        super().__init__(uid)
        self.name = name


class CSprite(Component, pygame.sprite.Sprite):
    """
    Sprite for characters.
    Adds itself to rendering group
    """

    def __init__(self, uid: int, image: str, collide: bool):
        super().__init__(uid)
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.collide = collide

        self.move_queue = []
        self.pos = [3000, 3000]

        # different move speeds for different terrain
        # 0 is block
        self.current_terrain_type_under_feet = "grass"
        self.terrain_move_speed = {"grass": 1,
                                   "dirt": 0.5,
                                   "water": 0}

        self.add(cfg.sprite_group)

    def update(self):
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]


print(cfg.components)
