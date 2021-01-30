'''testStates.py
This file provides several states representing various stages
in games of Backgammon.  It's intended for testing other software
on a variety of types of game boards.
Last updated: April 30, 2020, with a minor correction to the
last state.
S. Tanimoto, Univ. of Wash.
'''

from boardState import *

W = 0
R = 1

WHITE_TO_BEAR_OFF = bgstate()
WHITE_TO_BEAR_OFF.pointLists =[
[],
[],
[],
[],
[],
[],
[],
[R,R,R,R,R],
[],
[R,R,R],
[],
[],
[],
[R,R,R,R,R],
[],
[],
[],
[],
[W,W,W,W,W],
[W,W],
[W,W,W],
[W,W,W,W,W],
[],
[R,R] ]

RED_TO_BEAR_OFF = bgstate()
RED_TO_BEAR_OFF.pointLists =[
[R,R,R,R,R],
[],
[R,R,R],
[R,R],
[R,R,R,R,R],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[],
[W,W,W,W,W],
[W,W],
[W,W,W],
[W,W,W,W,W],
[] ]

# Given a state, returns an integer which represents how good the state is
# for the two players (W and R) -- more positive numbers are good for W
# while more negative numbers are good for R
def staticEval(state):
    d1 = 1
    d2 = 6
    #Following is our own eval function:
    board           = state.pointLists                      #current board state
    num_white_off   = len(state.white_off)                  #number of white checkers are born off
    num_red_off     = len(state.red_off)                    #number of red checkers are born off
    num_white_bar   = len([i == 'W' for i in state.bar])    #number of white checkers got hit
    num_red_bar     = len([i == 'R' for i in state.bar])    #number of red checkers got hit
    value           = 0                                     #our final score is a weighted sum of each evaluation factor
    WEIGHT_RACE     = 5
    WEIGHT_BEAROFF  = 10
    WEIGHT_HIT      = 4
    WEIGHT_BLOCK    = 3
    WEIGHT_STACK    = 2
    
    # Factor 1: evaluating # of checkers left outside of homebase
    # Racing strategy: encourage checkers to move as far as possible (we add weight to further checker)
    # but until we reach the homebase because we don't want to stack the checkers to the last index

    # Factor 2: encouraging stacking of 2
    white_sum = 0
    red_sum = 0
    white_stack = 0
    red_stack = 0
    for i in range(0, 24):
        lenBoard = len(board[i])
        print(board[i])
        if (board[i] != []) and (board[i][0] == W) and (i >= 0 and i <= 17):
            white_sum += i*lenBoard
            white_stack += 1 if lenBoard == 2 else 0

        if (board[i] != []) and (board[i][0] == R) and (i >= 6 and i <= 23):
            red_sum += (23-i)*lenBoard
            red_stack += 1 if lenBoard == 2 else 0

        if (board[i] != []) and (board[i][0] == W) and (i > 17):
            white_sum += 20*lenBoard
            white_stack += 1 if i == 24-d1 or i == 24-d2 else 0
            
        if (board[i] != []) and (board[i][0] == R) and (i < 6):
            red_sum += 20*lenBoard
            red_stack += 1 if i == d1 - 1 or i == d2 - 1 else 0
                
    value += (white_sum*2 - red_sum)*WEIGHT_RACE
    value += (white_stack - red_stack)*WEIGHT_STACK
    
    # Factor 2: evaluating # of checkers being born off
    value += (num_white_off**2 - num_red_off)*WEIGHT_BEAROFF

    # Factor 3: evaluating # of checkers being hit
    value += (num_red_bar*2 - num_white_bar)*WEIGHT_HIT

    # Factor 4: we reward more for blocking entrance of checkers (reward more for spreading out in homebase)
    red_col = 0
    white_col = 0
    for i in [0,5]: #red's homebase -> if red can occupy more columns
        if board[i] != [] and board[i][0] == R: red_col +=1
    for i in [18,23]:
        if board[i] != [] and board[i][0] == W: white_col += 1
    
    value += (white_col*2 - red_col)*WEIGHT_BLOCK
    
    return [white_sum, red_sum, white_stack, red_stack, white_col, red_col, value]

print("red: ", staticEval(RED_TO_BEAR_OFF))
print("white: ", staticEval(WHITE_TO_BEAR_OFF))

    