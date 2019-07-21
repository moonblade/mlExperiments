# mouse cheese game

a mouse in a grid with cheese and cats.

## Game.py
Game definition. running game class directly gives human playable version of the game.

### Classes

- Grid
Grid of the mouse cheese game

- Mouse
Movements are transferred to mouse and state is updated by it.

- Game
Main class, with movement, score tracking, display and interconnections

## Table.py
Implementation with qtable, python dict is used to store qtable values

### Classes

- Brain
Stores and retrieves q values based on each move and uses epsilon greedy approach to train

## neasy.py
Using keras-rl inbuilt functions to learn to play the game
Copy pasted code, haven't studied it after it started working.

## nerual.py
uncompleted Implementation, eventually to be an exact replica of table.py with nerual networks, it might not work which would prompt using two neural networks instead of one.
Need to research more.