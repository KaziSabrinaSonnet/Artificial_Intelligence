'''EightPuzzleWithManhattan.py
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
                current = S.b[i][j]
                goal= TILES_LIST[i][j]
                x1, y1= translate_x_y(current)
                x2, y2= translate_x_y(goal)
                dist += abs(x1-x2)
                dist += abs(y1-y2)
        return dist

def translate_x_y(num): 
    y= num//3
    x= num%3
    return x, y
        
