'''Diego de Jong'''

import random

# This class is for NPCs that the player can interact with throughout the game.
class NPC:
    def __init__(self, name, phrase):
        self.set_name(name)
        self.set_phrase(phrase)

    def get_name(self):
        return self.__name

    def get_phrase(self):
        return self.__phrase

    def set_name(self, name):
        if not name:
            raise ValueError("Name cannot be empty")
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        self.__name = name

    def set_phrase(self, phrase):
        if not phrase:
            raise ValueError("Phrase cannot be empty")
        if not isinstance(phrase, list):
            raise TypeError("Phrase must be a list of strings")
        self.__phrase = phrase

    def speak(self):
        return f'{self.__name} says, "{self.__phrase[random.randint(0, len(self.__phrase)-1)]}"'

