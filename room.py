'''Diego de Jong'''

from item import Item
from npc import NPC

# This class is for rooms that make up the game and that the player travels through.
class Room:
    def __init__(self, desc, item = None, npc = None):
        self.set_description(desc)
        self.set_item(item)
        self.set_npc(npc)
        self.__neighbors = {}

    def get_description(self):
        return self.__description

    def get_item(self):
        return self.__item

    def get_npc(self):
        return self.__npc

    def set_description(self, desc):
        if not desc:
            raise ValueError('Description cannot be empty')
        if not isinstance(desc, str):
            raise TypeError('Description must be a string')
        self.__description = desc

    def set_item(self, item):
        if item:
            if not isinstance(item, Item):
                raise TypeError('Item must be an Item object')
        self.__item = item

    def set_npc(self, npc):
        if npc:
            if not isinstance(npc, NPC):
                raise TypeError('NPC must be an NPC object')
        self.__npc = npc

    def has_item(self):
        if self.__item:
            return True
        else:
            return False

    def has_npc(self):
        if self.__npc:
            return True
        else:
            return False

    def add_neighbor(self, direction, room):
        if not isinstance(room, Room):
            raise TypeError('Room must be an Room object')
        self.__neighbors[direction] = room

    def get_neighbor(self, direction):
        if direction in self.__neighbors.keys():
            return self.__neighbors[direction]
        else:
            return None

    def neighbors(self):
        return self.__neighbors

    def remove_item(self):
        temp_item = self.get_item()
        self.__item = None
        return temp_item

    def __str__(self):
        item_desc = 'nothing'
        npc_desc = 'nobody'
        if self.has_item():
            item_desc = self.__item.get_description()
        if self.has_npc():
            npc_desc = self.__npc.get_name()
        
        return f'You are {self.__description}.\nYou see {item_desc}.\nYou meet {npc_desc}.'
        # return f'You are {self.__description}'





