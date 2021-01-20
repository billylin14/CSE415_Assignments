''' EightPuzzleWithManhattan.py
by Reece Peters, Billy Lin
UWNetID: reecep81, lin14
Student number: 1866651, 1765327

Assignment 2, Part 2, in CSE 415, Winter 2021.
 
This file contains our formulation for the eight puzzle manhattan heuristic.
'''

from EightPuzzle import *

def h(s):
    '''We return the amount of tiles currently out of place in the puzzle
between S and the goal state'''
    mat = s.b
    summ = 0
    
    for i in range(3):
        for j in range(3):
            if (mat[i][j] != 0):
                # The division gives us the row  
                x = mat[i][j] // 3
                # The modulo gives us the column
                y = mat[i][j] % 3
                difx = abs(i - x)
                dify = abs(j - y)
                summ += difx + dify
    return summ
