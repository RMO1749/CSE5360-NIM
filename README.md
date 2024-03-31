# CSE5360-NIM Nim Game with Minimax Algorithm
Name: Richard Olu Jordan
UTA ID: 1002101749

Assignment: Nim Game with Minimax Algorithm and Alpha-Beta Pruning

Introduction:

This project implements the classic game of Nim using the Minimax algorithm with alpha-beta pruning for optimal move selection. Nim is a  game of strategy where players take turns removing objects (such as marbles) from distinct piles. The player who removes the last object wins or loses depending on what version of the game is played.

Programming Language:

Python

File Structure:

File Name: nim.py
Description: Implementation of the Nim game with the Minimax algorithm.
Execution: Run the script with Python from the terminal or command prompt.

Classes:

PickMarble:
Description: Represents the Nim game environment.
Methods:
__init__(self, initial_state, game_version): Initializes the game with the initial state and game version (standard or misere).

actions(self, state): Generates all possible moves from the current state.

result(self, state, action): Computes the result of taking a specific action from the current state.

utility(self, state, player): Computes the utility value of a terminal state for a given player.

display(self, state): Displays the current state of the game.

terminal_test(self, state): Checks if the current state is a terminal state.

evaluation_fn(self, state, depth, player): Evaluates non-terminal game states based on a heuristic function.

human(self, state): Enables human player interaction through a GUI.

computer(self, state): Implements the Minimax algorithm with alpha-beta pruning for computer player move selection.

computerWithDepth(self, state, eval_fn=None): Implements Minimax algorithm with depth limitation for computer player move selection.

play_game(self): Initiates the Nim game and controls the game flow.

Functions:
validateFirstPlayer(firstPlayer): Validates the first player input.

validateGameVersion(gameVersion): Validates the game version input.

validateDepth(depth): Validates the depth limit input.

main(): Entry point of the program. Handles command-line arguments and initializes the Nim game.
Execution:
Standard Version:
python nim.py 8 8 standard computer
This command starts a standard Nim game with 8 red and 8 blue marbles, and the computer plays first.

Misere Version:
python nim.py 8 8 misere human
This command starts a misere Nim game with 8 red and 8 blue marbles, and the human player plays first.

Conclusion:

This project provides a comprehensive implementation of the Nim game using the Minimax algorithm with alpha-beta pruning. By running the provided commands, users can experience playing Nim against the computer or another human player, exploring different strategies and decision-making processes.
