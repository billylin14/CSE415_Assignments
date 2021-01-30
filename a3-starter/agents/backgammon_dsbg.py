'''
Name(s): Billy Lin, Reece Peters
UW netid(s): lin14, reecep81
'''

from game_engine import genmoves

DEFAULT_PLY = 4
W = 0
R = 1

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.max_ply = DEFAULT_PLY
        self.specialEval = False
        self.useAlphaBeta = False
        self.statesExpanded = 0
        self.cutoffs = 0
        self.d1 = 1
        self.d2 = 6

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        return "lin14-reecep81"

    # If prune==True, changes the search algorthm from minimax
    # to Alpha-Beta Pruning
    def useAlphaBetaPruning(self, prune=False):
        self.useAlphaBeta = prune
        self.cutoffs = 0
        self.statesExpanded = 0

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        return (self.statesExpanded, self.cutoffs)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. If maxply==-1,
    # no limit is set
    def setMaxPly(self, maxply=-1):
        self.max_ply = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        self.specialEval = func != None
        self.specialFunc = func

    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
        
    def move(self, state, die1=2, die2=3):
        # Does one step of the minimax or alpha beta pruning algorithm just to be able to access the move names
        # Then enters the recursive method
        self.d1 = die1
        self.d2 = die2
        player = state.whose_move
        self.initialize_move_gen_for_state(state, player, die1, die2)
        move_list = self.get_all_possible_moves(state)
        
        if (self.useAlphaBeta):
            alpha = -100000
            beta = 100000
            if player == W:
                for m in move_list:
                    new_alpha = self.alphabeta(m[1], self.max_ply - 1, alpha, beta, 1 - player, die1, die2)
                    if new_alpha >= alpha:
                        alpha = new_alpha
                        move_name = m[0]
                    if beta <= alpha:
                        self.cutoffs += 1
                        break
            else:
                for m in move_list:
                    new_beta = self.alphabeta(m[1], self.max_ply - 1, alpha, beta, 1 - player, die1, die2)
                    if new_beta <= beta:
                        beta = new_beta
                        move_name = m[0]
                    if beta <= alpha:
                        self.cutoffs += 1
                        break
        else:
            if player == W: provisional = -100000
            else: provisional = 100000
            for m in move_list:
                newVal = self.minimax(m[1], 1 - state.whose_move, self.max_ply - 1, die1, die2)
                if ((player == W and newVal > provisional) or (player == R and newVal < provisional)):
                    provisional = newVal
                    move_name = m[0]
        return move_name

    def alphabeta(self, board, plyLeft, alpha, beta, player, die1, die2):
        self.statesExpanded += 1
        if plyLeft == 0: return self.staticEval(board)
        self.initialize_move_gen_for_state(board, player, die1, die2)
        move_list = self.get_all_possible_moves(board)
        successors = [move[1] for move in move_list]
        if player == W:
            for s in successors:
                alpha = max(alpha, self.alphabeta(s, plyLeft - 1, alpha, beta, 1 - player, die1, die2))
                if beta <= alpha:
                    self.cutoffs += 1
                    break
            return alpha
        else:
            for s in successors:
                beta = min(beta, self.alphabeta(s, plyLeft - 1, alpha, beta, 1 - player, die1, die2))
                if beta <= alpha:
                    self.cutoffs += 1
                    break
            return beta

    def minimax(self, board, player, plyLeft, die1, die2):
        self.statesExpanded += 1
        if plyLeft == 0: return self.staticEval(board)
        self.initialize_move_gen_for_state(board, player, die1, die2)
        if player == W: provisional = -100000
        else: provisional = 100000
        move_list = self.get_all_possible_moves(board)
        successors = [move[1] for move in move_list]
        
        for s in successors:
            newVal = self.minimax(s, 1 - player, plyLeft - 1, die1, die2)
            if ((player == W and newVal > provisional) or (player == R and newVal < provisional)):
                provisional = newVal
        return provisional

    def get_all_possible_moves(self, state):
        """Uses the mover to generate all legal moves. Returns an array of move commands"""
        move_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_list.append(m)    # Add the move to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list.append(('p',state))
        return move_list
        
    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R
    def staticEval(self, state):
        #if using the specialEvalFunction
        if (self.specialEval):
            return self.specialFunc(state)

        #Following is our own eval function:
        board           = state.pointLists                      #current board state
        num_white_off   = len(state.white_off)                  #number of white checkers are born off
        num_red_off     = len(state.red_off)                    #number of red checkers are born off
        num_white_bar   = len([i == W for i in state.bar])    #number of white checkers got hit
        num_red_bar     = len([i == R for i in state.bar])    #number of red checkers got hit
        value           = 0                                     #our final score is a weighted sum of each evaluation factor
        WEIGHT_RACE     = 1
        WEIGHT_BEAROFF  = 100
        WEIGHT_HIT      = 20
        WEIGHT_STACK    = 5
        WEIGHT_PRIME    = 10
        
        # Factor 1: evaluating # of checkers left outside of homebase
        # Racing strategy: encourage checkers to move as far as possible (we add weight to further checker)
        # but until we reach the homebase because we don't want to stack the checkers to the last index
        # Factor 2: encouraging stacking of 2
        white_sum = 0
        red_sum = 0
        white_stack = 0
        red_stack = 0
        white_prime_count = 0
        red_prime_count = 0
        for i in range(0, 24):
            lenBoard = len(board[i])
            if (board[i] != []) and (board[i][0] == W) and (i >= 0 and i <= 17):
                white_sum += i*lenBoard
                white_stack += 1 if lenBoard == 2 else 0
                white_stack += 1 if lenBoard >= 2 and i >= 16 else 0
                #priming
                if i >= 16 and lenBoard >= 2:
                    white_prime_count += 1
                else:
                    white_prime_count = 0

            if (board[i] != []) and (board[i][0] == R) and (i >= 6 and i <= 23):
                red_sum += (23-i)*lenBoard
                red_stack += 1 if lenBoard == 2 else 0
                red_stack += 1 if lenBoard >= 2 and i <= 7 else 0
                #priming
                if i <= 7 and lenBoard >= 2:
                    red_prime_count += 1
                else:
                    red_prime_count = 0

            if (board[i] != []) and (board[i][0] == W) and (i > 17):
                white_sum += 20*lenBoard
                white_stack += 1 if lenBoard == 2 else 0 # if i == 24-self.d1 or i == 24-self.d2 else 0
                white_stack += 1 if lenBoard >= 2 and i <= 21 else 0
                #priming
                if lenBoard >= 2:
                    white_prime_count += 1
                else:
                    white_prime_count = 0

            if (board[i] != []) and (board[i][0] == R) and (i < 6):
                red_sum += 20*lenBoard
                red_stack += 1 if lenBoard == 2 else 0 # if i == self.d1 - 1 or i == self.d2 - 1 else 0
                red_stack += 1 if lenBoard >= 2 and i >= 2 else 0
                #priming
                if lenBoard >= 2:
                    red_prime_count += 1
                else:
                    red_prime_count = 0

        value += ((white_sum+num_white_off*WEIGHT_BEAROFF) - (red_sum+num_red_off*WEIGHT_BEAROFF))*WEIGHT_RACE
        value += (white_stack - red_stack)*WEIGHT_STACK
        value += (num_red_bar - num_white_bar)*WEIGHT_HIT
        if white_prime_count >= 5:
            value += white_prime_count*WEIGHT_PRIME
        if red_prime_count >= 5:
            value += red_prime_count*WEIGHT_PRIME
        
        return value