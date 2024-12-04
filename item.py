'''Diego de Jong'''

# This class is for items that the player can try to pick up, and maybe use.
class Item:
    def __init__(self, name, desc, weight):
        self.set_name(name)
        self.set_description(desc)
        self.set_weight(weight)

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_weight(self):
        return self.__weight

    def set_name(self, name):
        if not name:
            raise ValueError('Name cannot be empty')
        if not isinstance(name, str):
            raise TypeError('Name must be a string')
        self.__name = name

    def set_description(self, desc):
        if not desc:
            raise ValueError('Description cannot be empty')
        if not isinstance(desc, str):
            raise TypeError('Description must be a string')
        self.__description = desc

    def set_weight(self, weight):
        if not weight:
            raise ValueError('Weight cannot be empty')
        if not isinstance(weight, int):
            raise TypeError('Weight must be an integer')
        self.__weight = weight

    def __str__(self):
        return self.__description



