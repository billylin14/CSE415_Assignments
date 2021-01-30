'''
Name(s):
UW netid(s):
'''

from game_engine import genmoves

DEFAULT_PLY = 2
W = 0
R = 1


class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.max_ply = DEFAULT_PLY
        self.specialEval = False
        self.useAlphaBeta = True
        self.statesExpanded = 0
        self.cutoffs = 0

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        return "lin14-reecep81"

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. If maxply==-1,
    # no limit is set
    def setMaxPly(self, maxply=-1):
        self.max_ply = maxply

    # indicates the program to assume uniform distribution in die rolling
    def useUniformDistribution(self):
        pass

    # indicates the program to use alpha beta pruning in determining the next move
    def useAlphaBetaPruning(self, prune=False):
        self.useAlphaBeta = prune
        self.cutoffs = 0
        self.statesExpanded = 0

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        self.specialEval = func != None
        self.specialFunc = func

    # given the current state, whose move, and the values of the two dice
    # return a move generator that generates moves for the current state.
    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)
    
    # given the current board state, whose move, depth, and the values of the two dice
    # return the expectiminimax value of the current board for the player.
    def expectiminimax(self, board, player, plyLeft, die1, die2):
        self.statesExpanded += 1
        if plyLeft == 0: return self.staticEval(board)
        self.initialize_move_gen_for_state(board, player, die1, die2)
        if player == W: provisional = -100000
        else: provisional = 100000
        move_list = self.get_all_possible_moves(board)
        successors = [move[1] for move in move_list]
        newVal = 0
        for s in successors:
            for d1 in range(1,7):
                for d2 in range(d1, 7):
                    p = 1/36 if (d1 == d2) else 1/18
                    newVal += p*self.expectiminimax(s, 1 - player, plyLeft - 1, d1, d2)
            if ((player == W and newVal > provisional) or (player == R and newVal < provisional)):
                provisional = newVal
        return provisional

    # given the current board state, whose move, depth, initial alpha, initial beta, and the values of the two dice
    # returns the alpha-beta pruning version of expecitiminimax for the current state.
    def alphabeta(self, board, plyLeft, alpha, beta, player, die1, die2):
        self.statesExpanded += 1
        if plyLeft == 0: return self.staticEval(board)
        self.initialize_move_gen_for_state(board, player, die1, die2)
        move_list = self.get_all_possible_moves(board)
        successors = [move[1] for move in move_list]
       
        if player == W:
            for s in successors: 
                alpha_sum = 0
                for d1 in range(1,7):
                    for d2 in range(d1, 7):
                        p = 1/36 if (d1 == d2) else 1/18
                        alpha_sum += p*self.alphabeta(s, plyLeft - 1, alpha, beta, 1 - player, d1, d2)
                alpha = max(alpha, alpha_sum)
                if beta <= alpha:
                    self.cutoffs += 1
                    break
            return alpha
        else:
            for s in successors:
                beta_sum = 0
                for d1 in range(1,7):
                    for d2 in range(d1, 7):
                        p = 1/36 if (d1 == d2) else 1/18
                        beta_sum = p*self.alphabeta(s, plyLeft - 1, alpha, beta, 1 - player, d1, d2)
                beta = min(beta, beta_sum)
                if beta <= alpha:
                    self.cutoffs += 1
                    break
            return beta

    # Gets all possible moves considering a certain state.
    # Returns a list of moves that are possible.
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

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move. We have one iteration of each of the algorithms
    # in the move method itself since we need acess to the move names.
    def move(self, state, die1, die2):
        player = state.whose_move
        self.initialize_move_gen_for_state(state, player, die1, die2)
        move_list = self.get_all_possible_moves(state)
        # For alpha beta search
        if (self.useAlphaBeta):
            alpha = -100000
            beta = 100000
            if player == W:
                for m in move_list:
                    alpha_sum = 0
                    # Find the expected value of a move by summing over the possible die rolls.
                    for d1 in range(1,7):
                        for d2 in range(d1, 7):
                            p = 1/36 if (d1 == d2) else 1/18
                            alpha_sum += p * self.alphabeta(m[1], self.max_ply - 1, alpha, beta, 1 - player, d1, d2)
                    if alpha_sum >= alpha:
                        alpha = alpha_sum
                        move_name = m[0]
                    if beta <= alpha:
                        self.cutoffs += 1
                        break
            else:
                for m in move_list:
                    beta_sum = 0
                    for d1 in range(1,7):
                        for d2 in range(d1, 7):
                            p = 1/36 if (d1 == d2) else 1/18
                            beta_sum += p * self.alphabeta(m[1], self.max_ply - 1, alpha, beta, 1 - player, d1, d2)
                    if beta_sum <= beta:
                        beta = beta_sum
                        move_name = m[0]
                    if beta <= alpha:
                        self.cutoffs += 1
                        break
        else:
            if player == W: provisional = -100000
            else: provisional = 100000
            newVal = 0
            if player == W:
                for m in move_list:
                    for d1 in range(1,7):
                        for d2 in range(d1, 7):
                            p = 1/36 if (d1 == d2) else 1/18
                            newVal += p*self.expectiminimax(m[1], 1 - player, self.max_ply - 1, d1, d2)
                    if ((player == W and newVal > provisional) or (player == R and newVal < provisional)):
                        provisional = newVal
                        move_name = m[0]
        return move_name


    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R
    def staticEval(self, state):

        #if using the specialEvalFunction
        if (self.specialEval):
            return self.specialFunc(state)
        #Following is our own eval function:
        board           = state.pointLists                    #current board state
        num_white_off   = len(state.white_off)                #number of white checkers are born off
        num_red_off     = len(state.red_off)                  #number of red checkers are born off
        num_white_bar   = len([i == W for i in state.bar])    #number of white checkers got hit
        num_red_bar     = len([i == R for i in state.bar])    #number of red checkers got hit
        value           = 0                                   #our final score is a weighted sum of each evaluation factor
        WEIGHT_RACE     = 1                                   #Factor 1: evaluating # of checkers left outside of homebase
        WEIGHT_BEAROFF  = 100                                 #Factor 2: encouraging bearing of checkers if possible
        WEIGHT_HIT      = 20                                  #Factor 3: encouraging hitting by checking # of checkers on the bar
        WEIGHT_STACK    = 5                                   #Factor 4: encouraging stacking by rewarding stacks of 2.
        WEIGHT_PRIME    = 60                                  #Factor 5: encouraging making primes by counting consecutive stacks
        
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
