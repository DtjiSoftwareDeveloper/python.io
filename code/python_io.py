"""
This file contains code for the game "python.io".
Author: DtjiSoftwareDeveloper
"""


# Importing necessary libraries


import sys
import uuid
import pickle
import copy
import random
import os
from mpmath import *

mp.pretty = True


# Creating static functions to be used throughout the game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def generate_random_name() -> str:
    name: str = ""  # initial value
    letters: str = "abcdefghijklmnopqrstuvwxyz"
    length: int = random.randint(6, 20)
    for i in range(length):
        name += letters[random.randint(0, len(letters) - 1)]

    name = name.capitalize()
    return name


def load_player_data(file_name):
    # type: (str) -> Player
    return pickle.load(open(file_name, "rb"))


def save_player_data(player_data, file_name):
    # type: (Player, str) -> None
    pickle.dump(player_data, open(file_name, "wb"))


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes.


class Player:
    """
    This class contains attributes of the player in this game.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.player_id: str = str(uuid.uuid1())  # Generating random player ID
        self.name: str = name
        self.level: int = 1
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = mpf("1e6")
        self.python: Python = Python(name)  # initial value

    def level_up(self):
        # type: () -> None
        while self.exp >= self.required_exp:
            self.level += 1
            self.required_exp *= mpf("10") ** self.level

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Player ID: " + str(self.player_id) + "\n"
        res += "Name: " + str(self.name) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "EXP: " + str(self.exp) + "\n"
        res += "Required EXP to have to reach next level: " + str(self.required_exp) + "\n"
        res += "Python snake being used: " + str(self.python) + "\n"
        return res

    def clone(self):
        # type: () -> Player
        return copy.deepcopy(self)


class Python:
    """
    This class contains attributes of a python snake in this game.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = str(name.upper())
        self.weight: int = 1
        self.player: Player or None = None  # initial value
        self.x: int = 0
        self.y: int = 0
        self.is_eaten: bool = False

    def move_up(self, board):
        # type: (Board) -> bool
        if self.y > 0:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_python()
            self.y -= 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_python(self)
            return True
        return False

    def move_down(self, board):
        # type: (Board) -> bool
        if self.y < board.BOARD_HEIGHT - 1:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_python()
            self.y += 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_python(self)
            return True
        return False

    def move_left(self, board):
        # type: (Board) -> bool
        if self.x > 0:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_python()
            self.x -= 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_python(self)
            return True
        return False

    def move_right(self, board):
        # type: (Board) -> bool
        if self.x < board.BOARD_WIDTH - 1:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_python()
            self.x += 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_python(self)
            return True
        return False

    def eat_food(self, food):
        # type: (Food) -> None
        self.weight += food.weight

    def eat_python(self, python):
        # type: (Python) -> None
        if self.weight >= python.weight:
            self.weight += python.weight
            python.is_eaten = True
        else:
            python.weight += self.weight
            self.is_eaten = True

    def restore(self):
        # type: () -> None
        self.weight = 1

    def __str__(self):
        # type: () -> str
        return str(self.name)

    def add_player(self, player):
        # type: (Player) -> bool
        if self.player is None:
            self.player = player
            return True
        return False

    def remove_player(self):
        # type: () -> None
        self.player = None

    def get_max_steps(self):
        # type: () -> int
        if self.weight < 100:
            return 5
        elif 100 <= self.weight < 1000:
            return 4
        elif 1000 <= self.weight < 10000:
            return 3
        elif 10000 <= self.weight < 100000:
            return 2
        else:
            return 1

    def clone(self):
        # type: () -> Python
        return copy.deepcopy(self)


class Food:
    """
    This class contains attributes of food for python snakes to eat.
    """

    def __init__(self, weight):
        # type: (int) -> None
        self.name: str = "FOOD"
        self.weight: int = weight
        self.x: int = 0
        self.y: int = 0

    def move_up(self, board):
        # type: (Board) -> bool
        if self.y > 0:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_food()
            self.y -= 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_food(self)
            return True
        return False

    def move_down(self, board):
        # type: (Board) -> bool
        if self.y < board.BOARD_HEIGHT - 1:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_food()
            self.y += 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_food(self)
            return True
        return False

    def move_left(self, board):
        # type: (Board) -> bool
        if self.x > 0:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_food()
            self.x -= 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_food(self)
            return True
        return False

    def move_right(self, board):
        # type: (Board) -> bool
        if self.x < board.BOARD_WIDTH - 1:
            old_tile: Tile = board.get_tile_at(self.x, self.y)
            old_tile.remove_food()
            self.x += 1
            new_tile: Tile = board.get_tile_at(self.x, self.y)
            new_tile.add_food(self)
            return True
        return False

    def __str__(self):
        # type: () -> str
        return str(self.name)

    def clone(self):
        # type: () -> Food
        return copy.deepcopy(self)


class Board:
    """
    This class contains attributes of the board in this game.
    """

    BOARD_HEIGHT: int = 10
    BOARD_WIDTH: int = 10

    def __init__(self):
        # type: () -> None
        self.__tiles: list = []  # initial value
        for i in range(self.BOARD_HEIGHT):
            new: list = []  # initial value
            for j in range(self.BOARD_WIDTH):
                new.append(Tile())

            self.__tiles.append(new)

    def num_pythons(self):
        # type: () -> int
        pythons: int = 0  # initial value
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                curr_tile: Tile = self.get_tile_at(x, y)
                if isinstance(curr_tile.python1, Python):
                    pythons += 1

                if isinstance(curr_tile.python2, Python):
                    pythons += 1

        return pythons

    def num_food(self):
        # type: () -> int
        food: int = 0  # initial value
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                curr_tile: Tile = self.get_tile_at(x, y)
                if isinstance(curr_tile.food, Food):
                    food += 1

        return food

    def spawn_python(self, python):
        # type: (Python) -> None
        python_x: int = random.randint(0, self.BOARD_WIDTH - 1)
        python_y: int = random.randint(0, self.BOARD_HEIGHT - 1)
        python_tile: Tile = self.__tiles[python_y][python_x]
        while python_tile.python1 is not None or python_tile.python2 is not None:
            python_x = random.randint(0, self.BOARD_WIDTH - 1)
            python_y = random.randint(0, self.BOARD_HEIGHT - 1)
            python_tile = self.__tiles[python_y][python_x]

        python_tile.add_python(python)
        python.x = python_x
        python.y = python_y

    def spawn_food(self, food):
        # type: (Food) -> None
        food_x: int = random.randint(0, self.BOARD_WIDTH - 1)
        food_y: int = random.randint(0, self.BOARD_HEIGHT - 1)
        food_tile: Tile = self.__tiles[food_y][food_x]
        while food_tile.food is not None:
            food_x = random.randint(0, self.BOARD_WIDTH - 1)
            food_y = random.randint(0, self.BOARD_HEIGHT - 1)
            food_tile = self.__tiles[food_y][food_x]

        food_tile.add_food(food)
        food.x = food_x
        food.y = food_y

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        for y in range(self.BOARD_HEIGHT):
            curr: str = "| "
            for x in range(self.BOARD_WIDTH):
                curr += str(self.get_tile_at(x, y)) + " | "

            res += str(curr) + "\n"

        return res

    def get_tile_at(self, x, y):
        # type: (int, int) -> Tile or None
        if x < 0 or x >= self.BOARD_WIDTH or y < 0 or y >= self.BOARD_HEIGHT:
            return None
        return self.__tiles[y][x]

    def clone(self):
        # type: () -> Board
        return copy.deepcopy(self)


class Tile:
    """
    This class contains attributes of a tile on the board.
    """

    def __init__(self):
        # type: () -> None
        self.python1: Python or None = None
        self.python2: Python or None = None
        self.food: Food or None = None

    def __str__(self):
        # type: () -> str
        if self.python1 is None and self.food is None:
            return "NONE"
        res: str = ""  # initial value
        if isinstance(self.python1, Python):
            res += str(self.python1)

        if isinstance(self.python2, Python):
            if self.python1 is not None:
                res += ", " + str(self.python2)
            else:
                res += str(self.python2)

        if isinstance(self.food, Food):
            if self.python1 is not None or self.python2 is not None:
                res += ", " + str(self.food)
            else:
                res += str(self.food)

        return res

    def add_python(self, python):
        # type: (Python) -> bool
        if self.python1 is None:
            self.python1 = python
            return True
        elif self.python2 is None:
            self.python2 = python
            return True
        return False

    def remove_python(self):
        # type: () -> None
        if self.python2 is not None:
            self.python2 = None
        else:
            self.python1 = None

    def add_food(self, food):
        # type: (Food) -> bool
        if self.food is None:
            self.food = food
            return True
        return False

    def remove_food(self):
        # type: () -> None
        self.food = None

    def clone(self):
        # type: () -> Tile
        return copy.deepcopy(self)


# Creating the main function used to run the game.


def main():
    """
    This main function is used to run the game.
    :return: None
    """

    print("Welcome to 'python.io' by 'DtjiSoftwareDeveloper'.")
    print("This game is an offline version of Agar.io running on command line interface.")

    allowed_game_modes: list = ["SINGLE PLAYER", "MULTIPLAYER"]
    print("Enter 'SINGLE PLAYER' to play in single player game mode.")
    print("Enter 'MULTIPLAYER' to play in multiplayer game mode.")
    game_mode: str = input("Which game mode do you want to play in? ")
    while game_mode not in allowed_game_modes:
        print("Enter 'SINGLE PLAYER' to play in single player game mode.")
        print("Enter 'MULTIPLAYER' to play in multiplayer game mode.")
        game_mode = input("Sorry, invalid input! Which game mode do you want to play in? ")

    if game_mode == "SINGLE PLAYER":
        # Clearing the command line window
        clear()

        player: Player
        player_name: str = input("Enter your name: ")

        # Loading saved player data
        try:
            player = load_player_data("PYTHON.IO SAVED DATA " + str(player_name.upper()))
        except FileNotFoundError:
            player = Player(player_name)

        player.python.add_player(player)
        cpu_players: list = []  # initial value

        # Adding 4 CPU players.
        for i in range(4):
            new_player: Player = Player(generate_random_name())
            new_player.level = player.level
            new_player.exp = player.exp
            new_player.required_exp = player.required_exp
            new_player.python.add_player(new_player)
            cpu_players.append(new_player)

        # Initialising the board and starting the game.
        board: Board = Board()
        game_over: bool = False
        while board.num_food() < 5:
            food: Food = Food(random.randint(1, 999999))
            board.spawn_food(food)

        board.spawn_python(player.python)
        for cpu_player in cpu_players:
            board.spawn_python(cpu_player.python)

        while not game_over:
            allowed: list = ["UP", "DOWN", "LEFT", "RIGHT"]
            for i in range(player.python.get_max_steps()):
                # Clearing the command line window
                clear()

                print("Below is the current representation of the board.\n" + str(board))
                print("Current coordinates of your python snake: (" + str(player.python.x) + ", " +
                      str(player.python.y) + ").")
                print("Your score: " + str(player.python.weight))
                print("Enter 'UP' to move box up.")
                print("Enter 'DOWN' to move box down.")
                print("Enter 'LEFT' to move box left.")
                print("Enter 'RIGHT' to move box right.")
                direction: str = input("Where do you want to move your python snake to? ")
                while direction not in allowed:
                    print("Enter 'UP' to move box up.")
                    print("Enter 'DOWN' to move box down.")
                    print("Enter 'LEFT' to move box left.")
                    print("Enter 'RIGHT' to move box right.")
                    direction = input("Sorry, invalid input! Where do you want to move your python snake to? ")

                if direction == "UP":
                    player.python.move_up(board)
                elif direction == "DOWN":
                    player.python.move_down(board)
                elif direction == "LEFT":
                    player.python.move_left(board)
                else:
                    player.python.move_right(board)

                player_python_tile: Tile = board.get_tile_at(player.python.x, player.python.y)
                if player.python == player_python_tile.python1:
                    if isinstance(player_python_tile.python2, Python):
                        player.python.eat_python(player_python_tile.python2)
                        if player.python.is_eaten:
                            temp: Python = player_python_tile.python2.clone()
                            player_python_tile.remove_python()
                            player_python_tile.python1 = temp
                            game_over = True
                        else:
                            player_python_tile.remove_python()
                elif player.python == player_python_tile.python2:
                    if isinstance(player_python_tile.python1, Python):
                        player.python.eat_python(player_python_tile.python1)
                        if player.python.is_eaten:
                            player_python_tile.remove_python()
                            game_over = True
                        else:
                            temp: Python = player_python_tile.python2.clone()
                            player_python_tile.remove_python()
                            player_python_tile.python1 = temp

                if player_python_tile.food is not None:
                    player.python.eat_food(player_python_tile.food)
                    player_python_tile.remove_food()
                    board.spawn_food(Food(random.randint(1, 999999)))

            for cpu_player in cpu_players:
                cpu_python: Python = cpu_player.python
                if not cpu_python.is_eaten:
                    for i in range(cpu_python.get_max_steps()):
                        cpu_python_direction: str = allowed[random.randint(0, len(allowed) - 1)]

                        if cpu_python_direction == "UP":
                            cpu_python.move_up(board)
                        elif cpu_python_direction == "DOWN":
                            cpu_python.move_down(board)
                        elif cpu_python_direction == "LEFT":
                            cpu_python.move_left(board)
                        else:
                            cpu_python.move_right(board)

                        cpu_python_tile: Tile = board.get_tile_at(cpu_python.x, cpu_python.y)
                        if cpu_python == cpu_python_tile.python1:
                            if isinstance(cpu_python_tile.python2, Python):
                                cpu_python.eat_python(cpu_python_tile.python2)
                                if cpu_python.is_eaten:
                                    temp: Python = cpu_python_tile.python2.clone()
                                    cpu_python_tile.remove_python()
                                    cpu_python_tile.python1 = temp
                                    break
                                else:
                                    cpu_python_tile.remove_python()
                        elif cpu_python == cpu_python_tile.python2:
                            if isinstance(cpu_python_tile.python1, Python):
                                cpu_python.eat_python(cpu_python_tile.python1)
                                if cpu_python.is_eaten:
                                    cpu_python_tile.remove_python()
                                    break
                                else:
                                    temp: Python = cpu_python_tile.python2.clone()
                                    cpu_python_tile.remove_python()
                                    cpu_python_tile.python1 = temp

                        if player.python.is_eaten:
                            game_over = True

                        if cpu_python_tile.food is not None:
                            cpu_python.eat_food(cpu_python_tile.food)
                            cpu_python_tile.remove_food()
                            board.spawn_food(Food(random.randint(1, 999999)))

            player_wins: bool = True  # initial value
            for cpu_player in cpu_players:
                if not cpu_player.python.is_eaten:
                    player_wins = False

            if player_wins:
                game_over = True

        if not player.python.is_eaten:
            print("YOU WIN! Your score is " + str(player.python.weight) + ".")
            player.exp += player.python.weight
            player.python.restore()
            player.level_up()
        else:
            print("YOU LOSE! Your score is " + str(player.python.weight) + ".")
            player.exp += player.python.weight
            player.python.restore()
            player.level_up()

        # Clearing command line window
        string: str = input("Enter anything to proceed: ")

        # Saving player data
        save_player_data(player, "PYTHON.IO SAVED DATA " + str(player.name.upper()))
    else:
        # Clearing the command line window
        clear()

        number_of_human_players: int = int(input("How many human players are playing (2 - 5)? "))
        while number_of_human_players < 2 or number_of_human_players > 5:
            number_of_human_players = int(input("Sorry, invalid input! How many human players are playing (2 - 5)? "))

        number_of_cpu_players: int = 5 - number_of_human_players
        human_players: list = []  # initial value
        cpu_players: list = []  # initial value
        for i in range(number_of_human_players):
            player: Player
            player_name: str = input("Enter your name: ")

            # Loading saved player data
            try:
                player = load_player_data("PYTHON.IO SAVED DATA " + str(player_name.upper()))
            except FileNotFoundError:
                player = Player(player_name)

            player.python.add_player(player)
            human_players.append(player)

        player_with_highest_level: Player = human_players[0]  # initial value
        for human_player in human_players:
            if human_player.level > player_with_highest_level.level:
                player_with_highest_level = human_player

        for i in range(number_of_cpu_players):
            new_cpu_player: Player = Player(generate_random_name())
            new_cpu_player.level = player_with_highest_level.level
            new_cpu_player.exp = player_with_highest_level.exp
            new_cpu_player.required_exp = player_with_highest_level.required_exp
            new_cpu_player.python.add_player(new_cpu_player)
            cpu_players.append(new_cpu_player)

        # Initialising the board and starting the game.
        board: Board = Board()
        while board.num_food() < 5:
            food: Food = Food(random.randint(1, 999999))
            board.spawn_food(food)

        for human_player in human_players:
            board.spawn_python(human_player.python)
        for cpu_player in cpu_players:
            board.spawn_python(cpu_player.python)

        while board.num_pythons() > 1:
            allowed: list = ["UP", "DOWN", "LEFT", "RIGHT"]
            for human_player in human_players:
                if not human_player.python.is_eaten:
                    for i in range(human_player.python.get_max_steps()):
                        # Clearing the command line window
                        clear()

                        print("Below is the current representation of the board.\n" + str(board))
                        print("Current coordinates of your python snake: (" + str(human_player.python.x) + ", " +
                              str(human_player.python.y) + ").")
                        print("Your score: " + str(human_player.python.weight))
                        print("Enter 'UP' to move box up.")
                        print("Enter 'DOWN' to move box down.")
                        print("Enter 'LEFT' to move box left.")
                        print("Enter 'RIGHT' to move box right.")
                        direction: str = input("Where do you want to move your python snake to? ")
                        while direction not in allowed:
                            print("Enter 'UP' to move box up.")
                            print("Enter 'DOWN' to move box down.")
                            print("Enter 'LEFT' to move box left.")
                            print("Enter 'RIGHT' to move box right.")
                            direction = input("Sorry, invalid input! Where do you want to move your python snake to? ")

                        if direction == "UP":
                            human_player.python.move_up(board)
                        elif direction == "DOWN":
                            human_player.python.move_down(board)
                        elif direction == "LEFT":
                            human_player.python.move_left(board)
                        else:
                            human_player.python.move_right(board)

                        player_python_tile: Tile = board.get_tile_at(human_player.python.x, human_player.python.y)
                        if human_player.python == player_python_tile.python1:
                            if isinstance(player_python_tile.python2, Python):
                                human_player.python.eat_python(player_python_tile.python2)
                                if human_player.python.is_eaten:
                                    temp: Python = player_python_tile.python2.clone()
                                    player_python_tile.remove_python()
                                    player_python_tile.python1 = temp
                                    break
                                else:
                                    player_python_tile.remove_python()
                        elif human_player.python == player_python_tile.python2:
                            if isinstance(player_python_tile.python1, Python):
                                human_player.python.eat_python(player_python_tile.python1)
                                if human_player.python.is_eaten:
                                    player_python_tile.remove_python()
                                    break
                                else:
                                    temp: Python = player_python_tile.python2.clone()
                                    player_python_tile.remove_python()
                                    player_python_tile.python1 = temp

                        if player_python_tile.food is not None:
                            human_player.python.eat_food(player_python_tile.food)
                            player_python_tile.remove_food()
                            board.spawn_food(Food(random.randint(1, 999999)))

            # Iterating through each CPU player in the game
            for cpu_player in cpu_players:
                cpu_python: Python = cpu_player.python
                if not cpu_python.is_eaten:
                    for i in range(cpu_python.get_max_steps()):
                        cpu_python_direction: str = allowed[random.randint(0, len(allowed) - 1)]

                        if cpu_python_direction == "UP":
                            cpu_python.move_up(board)
                        elif cpu_python_direction == "DOWN":
                            cpu_python.move_down(board)
                        elif cpu_python_direction == "LEFT":
                            cpu_python.move_left(board)
                        else:
                            cpu_python.move_right(board)

                        cpu_python_tile: Tile = board.get_tile_at(cpu_python.x, cpu_python.y)
                        if cpu_python == cpu_python_tile.python1:
                            if isinstance(cpu_python_tile.python2, Python):
                                cpu_python.eat_python(cpu_python_tile.python2)
                                if cpu_python.is_eaten:
                                    temp: Python = cpu_python_tile.python2.clone()
                                    cpu_python_tile.remove_python()
                                    cpu_python_tile.python1 = temp
                                    break
                                else:
                                    cpu_python_tile.remove_python()
                        elif cpu_python == cpu_python_tile.python2:
                            if isinstance(cpu_python_tile.python1, Python):
                                cpu_python.eat_python(cpu_python_tile.python1)
                                if cpu_python.is_eaten:
                                    cpu_python_tile.remove_python()
                                    break
                                else:
                                    temp: Python = cpu_python_tile.python2.clone()
                                    cpu_python_tile.remove_python()
                                    cpu_python_tile.python1 = temp

                        if cpu_python_tile.food is not None:
                            cpu_python.eat_food(cpu_python_tile.food)
                            cpu_python_tile.remove_food()
                            board.spawn_food(Food(random.randint(1, 999999)))

        # Checking who wins the game
        winner: Player or None = None
        for player in human_players:
            if not player.python.is_eaten:
                winner = player
                break

        if winner is None:
            for player in cpu_players:
                if not player.python.is_eaten:
                    winner = player
                    break

        assert isinstance(winner, Player), "Glitch detected! There is no winner!"
        print(str(winner.name) + " WINS with score " + str(winner.python.weight) + "!!!")
        
        # Clearing command line window
        string: str = input("Enter anything to proceed: ")

        for player in human_players:
            player.exp += player.python.weight
            player.python.restore()
            player.level_up()

            # Saving player data
            save_player_data(player, "PYTHON.IO SAVED DATA " + str(player.name.upper()))

    sys.exit()


if __name__ == '__main__':
    main()
