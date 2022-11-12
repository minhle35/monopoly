# Author: Minh Thao Le
# GitHub username: minhle35
# Date: 02/06/2022
# Description:
# Portfolio project:
# write a class called RealEstateGame that allows two or more people to
# play a very simplified version of the game Monopoly.
# code for the game must define the class and methods described below, but you are encouraged to define other methods or classes that may be useful for the game. All data members must be **private**
#MUST INCLUDE THESE METHODS
# create_spaces()
# create_player()
# get_player_account_balance ()
# get_player_current_position()
# buy_space()
# move_player()
# check_game_over()

class PlayerAlreadyExistError(Exception):
    """
    Defines exception class for case when input of player name is already in use
    """
    pass

class InvalidNumberOfMoveSteps(Exception):
    """
    Defines exception class for case when invalid number out of range (1,7)
    """
    pass

class PlayerNotExist(Exception):
    """
    Defines exception class for case when there is search result of account balance for an input of player name
    """
    pass

class Player:
    """
    Defines a class to represents a player of a game
    """
    def __init__(self, player_name, player_acc_balance):
        """
        Initializes private data members of Player
        :param player_name:
        :param player_acc_balance:
        """
        self._player_name = player_name
        self._player_acc_balance = player_acc_balance
        self._curr_pos = 0
        self._is_bankrupted = False  # boolean

    def get_position(self):
        #returns position of player
        return self._curr_pos

    def get_account_balance(self):
        #returns account balance of player
        return self._player_acc_balance

    def update_acc_balance(self, amount):
        #updates new values of acc balance
        self._player_acc_balance += amount

    def set_current_pos(self, new_pos):
        # updates new position
        self._curr_pos = new_pos

    def set_bankrupted(self):
        #sets to bankrupted
        self._is_bankrupted = True

    def get_bankruptcy_status(self):
        #returns status of bankruptcy as boolean value
        return self._is_bankrupted

    def get_player_name(self):
        # returns name of the player
        return self._player_name


class Space:
    """
    represents a space of the game
    """
    def __init__(self, name, go_money, rent_amount):
        """
        initializes private data member of a space: name, go_money,rent_amount:
        """
        self._name = name
        self._go_money = go_money
        self._rent_amount = rent_amount
        self._owner = None

    def get_space_dict(self):
        # returns space dict for access from other classes
        return self._space_dict

    def get_rent_amount(self):
        # returns rent amount
        return self._rent_amount

    def get_owner(self):
        # returns owners
        return self._owner

    def set_owner(self, player_name):
        # updates new owners
        self._owner = player_name

    def get_space_name(self):
        # returns name of the space
        return self._name

    def get_go_money(self):
        #returns go money
        return self._go_money

class RealEstateGame:
    """
    represents a monopoly game
    """
    def __init__(self):
        # initializes private data members
        self._player_dict = {}  # keeps a record of each player
        self._space_list = []  # initializes list of all objects of spaces
        self._space_ownership = {}

    def game_space(self):
        # list of spaces in simplified version of US/Canada monopoly for this assignment
        return ["1.Mediterranean Avenue", "2.Baltic Avenue", "3.Oriental Avenue", "4.Vermont Avenue","5.Connecticut Avenue","6.St. Charles Place", "7.States Avenue", "8.Virginia Avenue", "9.St. James Place","10.Tennessee Avenue","11.New York Avenue", "12.Kentucky Avenue","13.Indiana Avenue", "14.Illinois Avenue","15.Atlantic Avenue", "16.Ventnor Avenue", "17.Marvin Gardens", "18.Pacific Avenue", "19.North Carolina Avenue","20.Pennsylvania Avenue","21.Park Place", "22.Boardwalk", "space_23", "space_24"]

    def update_space_ownership(self, space_name, player_name):
        # adds space as key and owners as value
        self._space_ownership[space_name] = (space_name, player_name)

    def get_space_ownership(self):
        # TESTING PURPOSE: returns self._space_ownership
        return self._space_ownership

    def get_space_list(self):
        # TESTING PURPOSE: prints values of self._space_list
        return self._space_list

    def get_player_dict(self):
        # TESTING PURPOSE: prints values of self._player_dict
        return self._player_dict

    def get_bankruptcy_status(self, player_name):
        #returns bankruptcy status
        if player_name in self._player_dict:
            return self._player_dict[player_name].get_bankruptcy_status()
        else:
            raise PlayerNotExist

    def create_spaces(self, go_money, rent_amount_list):
        """
        creates all spaces for a game with passed in 2 params
        :param go_money:the amount of money given to players when they land on or pass the "GO" space
         :param rent_amount_list: array of 24 integers(rent amount)
        """
        go_space = Space("Go", go_money, rent_amount=0)
        self._space_list.append(go_space)

        game_space = self.game_space()                       #monopoly spaces list
        for rent, name in zip(rent_amount_list, game_space):
            self._space_list.append(
                Space(name, go_money, rent))

    def create_player(self, player_name, go_balance):
        """
        creates a player for the game
        players always starts at the GO space
        :param player_name: unique name
        :param go_balance:
        """
        # updates dictionary of player
        if player_name not in self._player_dict:
            self._player_dict[player_name] = Player(player_name, go_balance)
        else:
            raise PlayerAlreadyExistError

    def get_player_account_balance(self, player_name):
        """
        takes as a parameter the name of the player and returns the player's account balance
        """

        if player_name not in self._player_dict:
            raise PlayerNotExist
        return self._player_dict[player_name].get_account_balance()

    def get_player_current_position(self, player_name):
        """
        finds current position of the player
        :param player_name:
        :return: the player's current position on the board as an integer
        """
        if player_name not in self._player_dict:
            raise PlayerNotExist
        return self._player_dict[player_name].get_position()

    def buy_space(self, player_name):
        """
        conducts purchase of space for player_name
        :param player_name:
        :return: True/False
        """
        current_pos = self.get_player_current_position(player_name)
        has_owner = self._space_list[current_pos].get_owner()
        account_bal = self._player_dict[player_name].get_account_balance()
        purchase_price = self._space_list[current_pos].get_rent_amount() * 5
        current_pos_name = self.get_space_list()[current_pos].get_space_name()

        if account_bal > purchase_price and has_owner is None and current_pos_name != "Go":
            self._player_dict[player_name].update_acc_balance(-purchase_price)
            self._space_list[current_pos].set_owner(player_name)
            self.update_space_ownership(str(current_pos),player_name)
            return True

        else:
            print(f"Already owned by {self._space_list[current_pos].get_owner()} or not enough money if owned by None")
            return False

    def move_player(self, player_name, move_steps):
        """
        this method moves current position of a player and adjusts account balance with several condition checking
        """
        player_obj = self._player_dict[player_name]
        curr_balance = player_obj.get_account_balance()
        current_pos = self.get_player_current_position(player_name)
        if curr_balance == 0:
            return
        else:
            if 1 <= move_steps <= 6:  # number of spaces to move between 1 and 6
                new_pos = (current_pos + move_steps) % 25  # since players moving in circular board, new position should be the modulo from 25 (there are 25 spaces in the board including GO)
                #Ex: arriving at Go space. new position being 25,  25 % 25 = 0

                player_obj.set_current_pos(new_pos)
                #AWARDED NEW GO MONEY if player moves pass Go in a new round
                if current_pos + move_steps >= 25:
                    player_obj.update_acc_balance(self._space_list[0].get_go_money())

                # No rent will be paid if the player is occupying the "GO" space, or if the space has no owner, or if the owner is the player
                if self._space_list[new_pos].get_owner() is None or self._space_list[new_pos].get_owner() == player_name:
                    return

                # NEEDS TO PAY:checks if current balance is greater than rents need paying
                if curr_balance < self._space_list[new_pos].get_rent_amount():
                    player_obj.update_acc_balance(-curr_balance)                # resets that player 's acc balance to 0
                    space_owner = self._space_list[new_pos].get_owner()         #the owner of the current space receives whatever left in the acc balance of the other player
                    self._player_dict[space_owner].update_acc_balance(curr_balance)
                else:
                    deducted_amount = self._space_list[new_pos].get_rent_amount()
                    player_obj.update_acc_balance(-deducted_amount)

                    space_owner = self._space_list[new_pos].get_owner()
                    self._player_dict[space_owner].update_acc_balance(deducted_amount)

                # CHECKS if account balance is 0 to flag as bankrupted
                inactive_player_target = ""
                for player in self._player_dict:
                    if self._player_dict[player].get_account_balance() == 0:
                        inactive_player_target = player #str
                        self._player_dict[player].set_bankrupted()
                #SET NONE to space_owner in space_list
                for space_obj in range(len(self._space_list) - 1, -1, -1):
                    if self._space_list[space_obj].get_owner() == inactive_player_target:
                        self._space_list[space_obj].set_owner(None)
            else:
                raise InvalidNumberOfMoveSteps


    def check_game_over(self):
        """
        checks if game is over when all but 1 has account balance as 0
        return the name of the winner
        """
        winner = ""
        inactive_player_count = 0
        for player in self._player_dict:
            if self._player_dict[player].get_bankruptcy_status():
                inactive_player_count += 1
            else:
                winner = player
        if len(self._player_dict) - inactive_player_count == 1:
            return winner
        return ""

