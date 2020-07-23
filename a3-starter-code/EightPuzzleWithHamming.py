'''EightPuzzleWithHamming.py
This file augments EightPuzzles.py with heuristic information,
so that it can be used by an A* implementation.
'''
from EightPuzzle import *
TILES_LIST= ([[0,1,2],[3,4,5],[6,7,8]])

def h(S): 
    if goal_test(S): #if S is a goal state then no need to calculate hamming distance
        return 0
    else:
        dist=0
        for i in range(3):
            for j in range(3):
                if S.b[i][j]==0: 
                    continue
                elif S.b[i][j] != TILES_LIST[i][j]:
                    dist = dist+1
        return dist


