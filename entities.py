"""
All entities are stored here

Format: UID = [Component1(), Component2() et c]
"""
from components import *

entity_dict = {1: [Life(1, 100, True),
                   Character(1, "Player"),
                   CSprite(1, "monster_slug.png", True)],
               2: [Life(2, 60, True),
                   CSprite(2, "blue_slug.png", True)],
               3: [],
               4: [],
               5: [],
               6: [],
               7: [],
               8: [],
               9: [],
               10: [],
               11: []}


def entity_creator(components: list):
    uid = 12

    while uid in entity_dict:
        uid += 1

    entity_dict[uid] = components