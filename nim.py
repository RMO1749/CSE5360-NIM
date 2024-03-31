import numpy as np
from tkinter import *
from tkinter.ttk import Combobox
import sys
import copy

class PickMarble:
    def __init__(self, gameVersion, firstPlayer, depthLimit = None):
        self.initial_state = {
                'red': int(sys.argv[1]), 
                'blue': int(sys.argv[2]),
                'player': firstPlayer             
                }
        self.gameVersion = gameVersion #instance attribute
        self.user_action = None
        self.depthLimit = depthLimit

    def actions(self, state):
       if self.gameVersion == 'standard':
            moves = []
            if state['red'] >= 2:
                    moves.append(('red', 2)) 
            if state['blue'] >= 2:
                    moves.append(('blue', 2))
            if state['red'] >= 1:
                    moves.append(('red', 1))
            if state['blue'] >= 1:
                    moves.append(('blue', 1))
            return moves
       if self.gameVersion == 'misere':
            moves = []
            if state['blue'] >= 1:
                    moves.append(('blue', 1)) 
            if state['red'] >= 1:
                    moves.append(('red', 1))
            if state['blue'] >= 2:
                    moves.append(('blue', 2))
            if state['red'] >= 2:
                    moves.append(('red', 2))
            return moves


    def result(self, state, action):
        new_state = copy.deepcopy(state)
        if action == (('red', 1)) or action == 'red 1':
            new_state['red'] -= 1 
        elif action == (('red', 2)) or action == 'red 2':
            new_state['red'] -= 2
        elif action == (('blue', 1)) or action == 'blue 1':
            new_state['blue'] -= 1
        elif action == (('blue', 2)) or action == 'blue 2':
            new_state['blue'] -= 2
        new_state['player'] = 'human' if state['player'] == 'computer' else 'computer'
        return new_state 

    def utility(self, state, player):
       score = 2 * state['red'] + 3 * state['blue'] 
       if self.gameVersion == 'standard':

        if player == 'max_player':
            return -score # assign negative scores because max_player(computer) would lose and we don't want that 
        else: 
            return score

       if self.gameVersion == 'misere':

           if player == 'max_player':
               return score 
           else:
               return -score

    def display(self, state):
        print(f"Red: {state['red']}, Blue: {state['blue']}")
    
    def terminal_test(self, state):
        return state['red'] <= 0 or state['blue'] <= 0

    def evaluation_fn(self, state, depth, player):
        total_red_marbles = state['red']
        total_blue_marbles = state['blue']
        marble_difference = abs(total_red_marbles - total_blue_marbles)
        balancing_score = 50 - marble_difference
        score = 2 * state['red'] + 3 * state['blue'] 

        if self.gameVersion == 'standard':
        
            if state['red'] <= 2 or state['blue'] <= 2:
                if player == 'max_player':
                    return score
                else:
                    return -score
            else:
                if player == 'max_player':
                    return -balancing_score
                else:
                    return balancing_score

        elif self.gameVersion == 'misere':
            
            if state['red'] <= 2 or state['blue'] <= 2:
                if player == 'max_player':
                    return -score
                else:
                    return score
            else:
                if player == 'max_player':
                    return -balancing_score
                else:
                    return balancing_score

    def human(self, state):
        def clicked():
            self.user_action = action.get() # here is where the instance attribute actually gets updated
            root.destroy() #Close the GUI window     
        
        root = Tk()
        root.title("Game Playing Interface")
        root.geometry('400x200') 

        available_moves = self.actions(state)
        action = Combobox(root, values= available_moves, width=20)
        action.grid(column=1, row=0, padx=10, pady=10)
        action.current(0)

        submit_btn = Button(root, text="Submit", command=clicked)
        submit_btn.grid(column=2, row=0, padx=10, pady=10)

        root.mainloop()


    def computer(self, state):

        max_player = 'max_player'
        min_player = 'min_player'

        def max_fn(state, alpha, beta):
            if self.terminal_test(state):
                return self.utility(state, max_player)
            value = -np.inf
            for action in self.actions(state):
                value = max(value, min_fn(self.result(state, action), alpha, beta))
                if value >= beta:
                    return value #here is where pruning occurs
                alpha = max(alpha, value)
            return value

        def min_fn(state, alpha, beta):
            if self.terminal_test(state):
                return self.utility(state, min_player) 
            value = np.inf
            for action in self.actions(state):
                value = min(value, max_fn(self.result(state, action), alpha, beta))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        best_value = -np.inf
        beta = np.inf
        best_move = None

        for action in self.actions(state):
            value = min_fn(self.result(state, action), best_value, beta)
            if value > best_value:
                best_value = value
                best_move = action
        return best_move

    def computerWithDepth(self, state, eval_fn=None):
        
        max_player = 'max_player'
        min_player = 'min_player'

        def cutoff_fn(depth):
            return depth >= self.depthLimit or self.terminal_test(state)
            

        def local_eval_fn(state, depth, player):

            if self.terminal_test(state):
                return self.utility(state, player)
            elif eval_fn is not None:
                return eval_fn(state, depth, player)
            else:
                return self.utility(state, player)
                

        def max_fn(state, alpha, beta, currentDepth):
     
            if cutoff_fn(currentDepth):
                return local_eval_fn(state, currentDepth, max_player)

            value = -np.inf
            for action in self.actions(state):
                value = max(value, min_fn(self.result(state, action), alpha, beta, currentDepth + 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)   
            return value

        def min_fn(state, alpha, beta, currentDepth):
           
            if cutoff_fn(currentDepth):
                return local_eval_fn(state, currentDepth, min_player)

            value = np.inf
            for action in self.actions(state):
                
                value = min(value, max_fn(self.result(state, action), alpha, beta, currentDepth + 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        best_value = -np.inf
        beta = np.inf
        best_move = None
        for action in self.actions(state):
            value = min_fn(self.result(state, action), best_value, beta, 1)
            if value > best_value:
                best_value = value
                best_move = action
        return best_move

    def play_game(self):
        state = self.initial_state.copy()
        
        print("Initial State: ")
        print(f"Red: {state['red']}, Blue: {state['blue']}")

        while not self.terminal_test(state):

            if state['player'] == 'computer':

                if self.depthLimit is not None:
                    action = self.computerWithDepth(state, self.evaluation_fn)
                else:
                     action = self.computer(state)
                print(f"Computer picked {action}")

            elif state['player'] == 'human': # human
                self.human(state) #here, the GUI is setup when the human function is called.

                while self.user_action is None:
                    pass
                action = self.user_action
                print(f"Human picked {action}")
                self.user_action = None #here, we want to reset the GUI (for the next turn)

            state = self.result(state, action)
            self.display(state)

        final_score = 2 * state['red'] + 3 * state['blue']

        if self.gameVersion == 'standard':
            print(f"{state['player']} lost the game by {final_score} points.")
        elif self.gameVersion == 'misere':
            print(f"{state['player']} won the game by {final_score} points.")

        print("GAME OVER!")

def validateFirstPlayer(firstPlayer):
    if firstPlayer == 'computer' or  firstPlayer == 'human':
        return firstPlayer
    else:
        raise ValueError("Please input correct first player either as 'human' or 'computer'") 

def validateGameVersion(gameVersion):
    if gameVersion == 'standard' or gameVersion == 'misere':
        return gameVersion
    else:
        raise ValueError("Please input correct game version of format 'standard' or 'misere")

def validateDepth(depth):
    if isinstance(depth, int):
          return depth
    else:
        raise ValueError("Please enter a valid integer as the depth limit")

def main():
    try:
        print("Script started with args:", sys.argv)
        if len(sys.argv) == 5:
            gameVersion = sys.argv[3]
            firstPlayer = sys.argv[4]

            finalgameVersion = validateGameVersion(gameVersion)
            finalFirstPlayer = validateFirstPlayer(firstPlayer)

            print(f"Initializing game with {finalgameVersion}, {finalFirstPlayer}")

            gameState = PickMarble(finalgameVersion, finalFirstPlayer)
            print("Starting game...")
            gameState.play_game()

        elif len(sys.argv) == 6:


            gameVersion = sys.argv[3]
            firstPlayer = sys.argv[4]
            depth = int(sys.argv[5])

            finalgameVersion = validateGameVersion(gameVersion)
            finalFirstPlayer = validateFirstPlayer(firstPlayer)
            finalDepth = validateDepth(depth)

            print(f"Initializing game with {finalgameVersion}, {finalFirstPlayer}, {finalDepth}")

            gameStateWithDepth = PickMarble(finalgameVersion, finalFirstPlayer, finalDepth)
            print("Starting game...")
            gameStateWithDepth.play_game()

        else:
            print("Incorrect number of arguments.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    main()