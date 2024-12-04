'''
Diego de Jong
This program runs a text based story quest game.
I certify that this code is mine, and mine alone, in accordance with
GVSU academic honesty policy.
I received help from a number of individuals throughout this project, including:
my Dad, my rubber duck, the Panzer of the Lake, Prof.Woodring, and Elija Morgan.
11/26/2024
'''

from item import Item
from npc import NPC
from room import Room
import colorama
from colorama import Fore, Back, Style
colorama.init()
import random

# This class is the entire game
class Game:
    def __init__(self):
        self.inventory = []
        self.gun_ammo = 1
        self.create_world()
        self.current_room = self.small_rm
        self.prior_room = self.small_rm
        self.set_welcome_message()
        self.current_message = str('')
        self.win_condition = 0      # 0 is no game over, -1 is lose(dead), 1 is win(escaped)
        self.win_progress = 0       # 0-1 is neutral ending, 2 is true ending (kill monster + save Krei)

    # Return the current message
    def get_message(self):
        return self.current_message

    # Return the current room that the player is in
    def get_current_room(self):
        return self.current_room

    # Create all items, NPCs, rooms, and neighbor connections
    def create_world(self):
        #Items
        self.sword = Item('giant sword',
                          'a really big sword made out of some really dense steel.',
                          100)
        self.phone = Item('cell phone',
                          'a little Nokia. It has no battery.',
                          10)
        self.papernote = Item('paper note',
                              'a little yellow paper note with some writing on it. '
                              'It\'s all scratched up, and hard to read:\n' + Style.DIM + Fore.WHITE +
                              '\'The mo_st_r\'s we_kn_ss _s the No___!\'' + Style.RESET_ALL,
                              1)
        self.gun = Item('nerf gun',
                        f'one of those big, two-handed Nerf Guns. Nerf or nothin\'.\nBullets: {self.gun_ammo}',
                        30)
        self.photo = Item('photograph',
                          'a photograph of a' + Fore.LIGHTYELLOW_EX +' happy family.' + Style.RESET_ALL,
                          1)
        #NPCs
        self.krei = NPC('Krei Z.',
                        [Fore.BLUE + 'I go that way and it leads me this way, '
                        'I go the other way and it leads me that way, '
                        'I don’t know what’s going on…!' + Style.RESET_ALL,
                         Fore.BLUE + '...ijustwannagohomeijustwannagohomeijustwannagohomeijustwannagohome…!'
                         + Style.RESET_ALL,
                         Fore.BLUE + 'GET AWAY FROM ME!' + Style.RESET_ALL,
                         Fore.BLUE + 'I need...I need my family...' + Style.RESET_ALL])
        self.monster = NPC(Style.BRIGHT + 'THE MONSTER' + Style.RESET_ALL,
                           [Fore.BLUE + '……………………………………………………………………………………………………………………………………………………'
                            + Style.RESET_ALL])
        # Rooms
        self.small_rm = Room('in a small, empty room', None, None)
        self.monster_rm = Room('in a room' + Style.BRIGHT + ' WITH A MONSTER IN IT' + Style.RESET_ALL,
                               None, self.monster)
        self.hallway_rm = Room('in a long hallway', self.photo, self.krei)
        self.sword_rm = Room('in a small, dimly-lit room', self.sword, None)
        self.splithall_rm = Room('in a long hallway that splits at the end', self.papernote, None)
        self.stair_rm = Room('at a large spiral staircase', self.phone, None)
        self.large_rm = Room('in a large room', self.gun, None)
        self.exit_rm = Room('in a room with a bright' + Fore.RED + ' exit'
                            + Style.RESET_ALL + ' door at the end', None, None)
        # Most rooms connect infinitely and randomly, except for the monster room and exit room
        # Must defeat the monster to progress to the exit room, where you can escape and win the game
        self.monster_rm.add_neighbor('forward', self.exit_rm)

    # Set the game's message to the starting description that sets the scene
    def set_welcome_message(self):
        self.current_message = str('You fell asleep while doing your Computer Science homework one day, '
                                'and woke up in the back rooms from that meme you saw the other day.\n'
                                'You\'re not done with your homework, so you gotta find an' + Fore.RED +
                                ' exit' + Fore.RESET + ' fast!\nYou also sense a' + Fore.LIGHTYELLOW_EX +
                                ' dangerous presence' + Fore.RESET +', so you pick up the pace.')

    # This is the player's input command. It returns only the first two words given in lowercase.
    def parse_command(self):
        words = input(Fore.LIGHTGREEN_EX + "Enter>>> ").split()
        first = words[0].lower()
        if len(words) > 1:
            second = words[1].lower()
        else:
            second = None
        return first, second

    # This function drives the game! All output comes from this function alone!
    # While the game hasn't finished, loop inputs from the player, and play the game.
    # Once game over occurs, print the game over message.
    def play(self):
        # print initial welcome message
        self.set_welcome_message()
        print(Style.RESET_ALL + self.get_message())
        # Loop until game over
        move_commands = ['move', 'run', 'go', 'escape', 'travel', 'walk', 'exit', 'advance', 'turn', 'spin', 'dash']
        while not self.game_over():
            first, second = self.parse_command()
            if first == 'help':
                self.help()
            elif first in move_commands:
                self.move(second)
            elif first == 'look':
                self.look()
            elif first == 'take':
                self.take()
            elif first == 'place':
                self.place(second)
            elif first == 'speak':
                self.speak()
            elif first == 'retreat':
                self.retreat()
            elif first == 'items':
                self.items()
            elif first == 'attack':
                self.attack()
            elif first == 'dance':
                self.dance()
            else:
                self.current_message = Fore.LIGHTGREEN_EX + 'Not a valid command! Try \'help\''
            print(Style.RESET_ALL + self.get_message())
        self.game_over()
        print(Style.RESET_ALL + self.get_message())

    # Player Action Functions
    # Give this helpful message with keywords in different colors.
    def help(self):
        self.current_message = ('You gotta get outta here fast! You have computer science homework to finish!'
                                ' Maybe you\'ll find the' + Fore.RED + ' exit' + Fore.RESET + ' if you just'
                                + Fore.LIGHTYELLOW_EX + ' keep moving forward?\n' + Fore.LIGHTGREEN_EX +
                                'Valid Commands:\n1.help\n2.move(direction)\n3.look\n4.take\n5.place(item)\n6.speak\n'
                                '7.retreat\n8.items\n9.attack\n10.dance' + Style.RESET_ALL)

    # If the room has an item, and it's not too heavy,
    # remove the item from the room and add it to inventory.
    def take(self):
        if not self.current_room.has_item():
            self.current_message = 'There is nothing to take.'
            return
        if self.current_room.get_item().get_weight() >= 50:
            self.current_message = 'The item is too heavy to pick up!'
            return
        new_item = self.current_room.remove_item()
        self.inventory.append(new_item)
        self.current_message = f'You are holding {new_item}'

    # Place an item from your inventory in the current room.
    # Only one item can be stored per room.
    # Special cutscene occurs if you give Krei his photo.
    def place(self, name):
        if not name:
            self.current_message = Fore.LIGHTGREEN_EX + 'Need to specify an item to place'
            return
        item = self.search_items(name)
        if not item:
            self.current_message = f'You are not holding {name}.'
            return
        if self.current_room.get_item():
            self.current_message = f'There is already an item in the room.'
            return
        if item == self.photo and self.current_room.get_npc() == self.krei:
            self.current_message = (f'You placed the {name} down in the room.\n' 
                                    f'Krei Z. says, "' + Fore.BLUE +
                                    f'Oh...my family...thank you...\n'
                                    f'............................................\n'
                                    f'I need to return...I will escape...!' + Style.RESET_ALL + '"')
            self.win_progress += 1
            self.inventory.remove(self.photo)
            return
        self.current_message = f'You placed the {name} down in the room.'
        self.inventory.remove(item)
        self.current_room.set_item(item)

    # Print the current room's message.
    def look(self):
        self.current_message = self.current_room.__str__()

    # If there's an NPC in the room, have them say a phrase.
    def speak(self):
        if not self.current_room.has_npc():
            self.current_message = 'There is no one here to speak.'
        else:
            self.current_message = self.current_room.get_npc().speak()

    # Move to the last room you were in.
    # Can only retreat one room back at a time, no consecutive retreating allowed.
    # There's a chance that the monster will get the player before they escape the monster room!
    def retreat(self):
        if self.prior_room == self.current_room:
            self.current_message = 'You cannot retreat from here.'
        if self.current_room == self.monster_rm:
            x = random.randint(1, 4)
            if x == 4:
                self.current_message = (Style.BRIGHT + ' THE MONSTER'
                                        + Style.RESET_ALL + ' caught you before you could escape!')
                self.win_condition = -1
        else:
            self.current_room = self.prior_room
            self.current_message = 'You retreated.\n' + self.current_room.__str__()

    # Print a list of all the items in inventory.
    # If inventory has no items, then print that it's empty.
    def items(self):
        if self.inventory:
            inventory_string = str('You are holding:\n')
            for item in self.inventory:
                inventory_string += 'a ' + item.get_name() + '\n'
            self.current_message = inventory_string
        else:
            self.current_message = 'You are not holding any items.'

    # Make the player move forward, and change the current room.
    # Most rooms randomly and infinitely connect, with specific odds for each connection.
    # Can only move through the monster room if the monster is dead, otherwise you die and lose.
    # Once you move past the exit room, you win!
    def move(self, direction = 'forward'):
        directions = ['forward', 'ahead', 'up', 'down', 'left', 'right', 'straight', 'on', 'escape', None]
        if not direction in directions:
            self.current_message = 'You can\'t move in that direction.'
            return
        self.prior_room = self.current_room
        if self.current_room == self.exit_rm:
            self.win_condition = 1
            return
        if not self.current_room.neighbors():
            chance = random.randint(0, 100)
            if 0 <= chance < 20:
                self.current_room = self.small_rm
            elif 20 <= chance < 25:
                self.current_room = self.monster_rm
            elif 25 <= chance < 45:
                self.current_room = self.hallway_rm
            elif 45 <= chance < 60:
                self.current_room = self.sword_rm
            elif 60 <= chance < 70:
                self.current_room = self.splithall_rm
            elif 70 <= chance < 80:
                self.current_room = self.stair_rm
            elif 80 <= chance < 100:
                self.current_room = self.large_rm
            if self.current_room == self.prior_room:
                if self.current_room == self.small_rm:
                    self.current_room = self.large_rm
                else:
                    self.current_room = self.small_rm
        elif self.current_room == self.monster_rm:
            if self.current_room.get_npc() == self.monster:
                self.win_condition = -1
                self.current_message = (Style.BRIGHT + 'THE MONSTER' + Style.RESET_ALL + ' saw and attacked you.' )
                return
            else:
                self.current_room = self.exit_rm
        self.current_message = self.current_room.__str__()

    # Search inventory for the given item,
    # and return True or False depending on if it's there or not.
    # Item names have several valid inputs.
    def search_items(self, name):
        true_name = None
        gun_names = ['nerf', 'gun']
        photo_names = ['photo', 'photograph']
        phone_names = ['cell', 'phone', 'nokia']
        note_names = ['paper', 'note', 'papernote']

        if name in gun_names:
            true_name = 'nerf gun'
        elif name in photo_names:
            true_name = 'photograph'
        elif name in phone_names:
            true_name = 'cell phone'
        elif name in note_names:
            true_name = 'paper note'
        for item in self.inventory:
            if item.get_name() == true_name:
                return item
        return None

    # This function only attacks THE MONSTER.
    # Different events happen for each attack.
    # Nokia attack is the only one that kills THE MONSTER.
    def attack(self):
        if not self.current_room.get_npc() == self.monster:
            self.current_message = 'There is no reason to attack.'
            return
        attacks = ['fists']
        gun_names = ['nerf', 'gun', 'nerf gun']
        phone_names = ['cell', 'phone', 'cell phone', 'nokia']
        for item in self.inventory:
            if item == self.gun:
                attacks.append(item.get_name())
            if item == self.phone:
                attacks.append(item.get_name())
        plr_attack = str(input(f'Pick your weapon: {attacks}>>> ')).lower()
        if not plr_attack:
            self.current_message = Fore.LIGHTGREEN_EX + 'Attack cannot be empty'
            return
        if not isinstance(plr_attack, str):
            self.current_message = Fore.LIGHTGREEN_EX + 'Attack must be a string'
            return
        if plr_attack == 'fists':
            self.current_message = ('You attack' + Style.BRIGHT +
                                    ' THE MONSTER' + Style.RESET_ALL + ' with your bare hands...and lose terribly.')
            self.win_condition = -1
        elif plr_attack in gun_names:
            if self.gun_ammo == 1:
                self.current_room = self.prior_room
                self.current_message = ('You shoot' + Style.BRIGHT + ' THE MONSTER'
                                        + Style.RESET_ALL + ', and distract it. '
                                        + 'You retreated.\n' + self.current_room.__str__())
                self.gun_ammo = 0
            elif self.gun_ammo == 0:
                self.current_message = ('You have no more ammo!' + Style.BRIGHT +
                                    ' THE MONSTER' + Style.RESET_ALL + ' gets you.')
                self.win_condition = -1
        elif plr_attack in phone_names:
            self.current_message = ('You chuck the Nokia at' + Style.BRIGHT +
                                    ' THE MONSTER' + Style.RESET_ALL + ', and it dies instantly. Yey!')
            self.win_progress += 1
            self.monster_rm.set_npc(None)
        else:
            self.current_message = Fore.LIGHTGREEN_EX + 'Not a valid attack'

    # Do a funny dance lol.
    def dance(self):
        dances = ['You smack a hard jig. Nice.', 'You groove to a tune.',
                  'You start absolutely breaking it down.', 'You dance for a solid 5 minutes.']
        self.current_message = dances[random.randint(0, len(dances) - 1)]

    # Return true if a game over condition is met, otherwise return false.
    # If you die, you get the bad ending.
    # if you exit, you get the good ending.
    # If you exit after defeating the monster and saving Krei, you get the true ending.
    def game_over(self):
        if self.win_condition == -1:
            self.current_message = (Style.BRIGHT + Fore.RED + 'BAD ENDING:'
                                    + Style.RESET_ALL + ' Congrats! You\'re ded!')
            return True
        elif self.win_condition == 1:
            if not self.win_progress == 2:
                self.current_message = (Style.BRIGHT + Fore.GREEN + 'GOOD ENDING:'
                                        + Style.RESET_ALL +
                                        ' You escaped! Now you can get back to you computer science homework!')
            else:
                self.current_message = (Style.BRIGHT + Fore.GREEN + 'TRUE ENDING:'
                                        + Style.RESET_ALL +
                                        ' You win! You escaped, defeated' + Style.BRIGHT + ' THE MONSTER'
                                        + Style.RESET_ALL + ', and saved Krei!')
            return True
        else:
            return False

    # Keep on looping until you get the nokia and kill THE MONSTER.
    # Then, escape the backrooms, and win!
    # Note that there is no 100% guarantee chance to auto-win due to THE MONSTER
    # being able to catch the player before they retreat.
    def auto_win(self):
        while self.monster_rm.get_npc() == self.monster:
            self.move(direction = 'forward')
            self.take()
            if self.current_room.get_npc() == self.krei:
                self.place('photo')
            if self.current_room.get_npc() == self.monster:
                if self.search_items('nokia'):
                    self.attack()
                else:
                    self.retreat()
        self.move()
        self.move()

if __name__ == '__main__':
     g = Game()
     g.play()














