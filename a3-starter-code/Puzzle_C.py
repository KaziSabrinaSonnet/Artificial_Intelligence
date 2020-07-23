'''puzzle3.py
An instance of the Eight Puzzle.
'''

from EightPuzzle import *

# We simply redefine the initial state.

init_state_list = [[4,5,0],[1,2,8],[3,7,6]]

CREATE_INITIAL_STATE = lambda: State(init_state_list)