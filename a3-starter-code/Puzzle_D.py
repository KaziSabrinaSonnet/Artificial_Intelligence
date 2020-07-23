'''puzzle3.py
An instance of the Eight Puzzle.
'''

from EightPuzzle import *

# We simply redefine the initial state.

init_state_list = [[0,8,2],[1,7,4],[3,6,5]]

CREATE_INITIAL_STATE = lambda: State(init_state_list)