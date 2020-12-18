# python.io
"python.io" is an offline version of the game Agar.io running on command line interface. In this game, the player(s) will control a python snake
and needs to make it the last python snake standing to win the game. This game supports both single player and multiplayer game modes. Below shows
more detailed information about the game.

### Executable File

The executable file "python_io.exe" is used to run the game. It is downloadable from
https://github.com/DtjiSoftwareDeveloper/python.io/blob/main/executable/python_io.exe.

### Source Code

Python code used to run the game is available in
https://github.com/DtjiSoftwareDeveloper/python.io/blob/main/code/python_io.py.

### Getting Started

Once you run the game, you will be asked whether you want to play in single player or multiplayer game mode. In single player game mode, you will
play against four CPU-controlled players. In multiplayer game mode, you will play with 2-4 other human players and the number of CPU-controlled players
will be equal to five subtracted by the total number of human players.

![Getting Started](https://github.com/DtjiSoftwareDeveloper/python.io/blob/main/images/Getting%20Started.png)

### Single Player Game Mode

At first, you will be asked to enter your name. If your name exists, a saved player data with your name will be loaded. Else, a new player data will be created.

![Entering Your Name](https://github.com/DtjiSoftwareDeveloper/python.io/blob/main/images/Entering%20Your%20Name.png)

Next, you will be shown the current board representation. You are able to move your python snake a certain number of steps depending on its weight during your turn.
If you move your python snake towards a tile with food, it will gain weight. Else if you move your python snake towards a tile with another python snake, the heavier
python snake will eat the lighter one and once your python snake is eaten, you lose. The weight the heavier python snake gains depends on the weight of the lighter one.

![Single Player Gameplay](https://github.com/DtjiSoftwareDeveloper/python.io/blob/main/images/Single%20Player%20Gameplay.png)

### Multiplayer Game Mode

Everything in this game mode will be similar to single player game mode except that this game mode requires 2 to 5 human players to be present. In this game mode, all human
players will be told to enter their names.
