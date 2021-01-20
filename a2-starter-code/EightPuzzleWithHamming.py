''' EightPuzzleWithHamming.py
by Reece Peters, Billy Lin
UWNetID: reecep81, lin14
Student number: 1866651, 1765327

Assignment 2, Part 2, in CSE 415, Winter 2021.
 
This file contains our formulation for the eight puzzle hamming heuristic.
'''

from EightPuzzle import *

def h(s):
    '''We return the amount of tiles currently out of place in the puzzle
between S and the goal state'''
    
    # This is perfect
    # [0,1,2;
    #  3,4,5;
    #  6,7,8]
    
    mat = s.b
    perfect = [[0,1,2],[3,4,5],[6,7,8]]
    c = 0
    
    for i in range(3):
        for j in range(3):
            #If the tile isn't in the same place as the perfect matrix and it's not the empty space
            if (perfect[i][j] != mat[i][j] and (mat[i][j] != 0)):
                c = c + 1
    return c
