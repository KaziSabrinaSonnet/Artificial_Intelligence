'''puzzle_A.py
An instance of the Eight Puzzle.
'''

from EightPuzzle import *

# We simply redefine the initial state.

init_state_list = [[3, 0, 1], 
                   [6, 4, 2], 
                   [7, 8, 5]]

CREATE_INITIAL_STATE = lambda: State(init_state_list)