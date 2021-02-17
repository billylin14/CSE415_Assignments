'''Q_Learn.py
STUDENT STARTER TEMPLATE ...

Implement Q-Learning in this file by completing the implementations
of the functions whose stubs are present.
Add or change code wherever you see #*** ADD OR CHANGE CODE HERE ***

This is part of the UW Intro to AI Starter Code for Reinforcement Learning.

'''

# Edit the returned name to ensure you get credit for the assignment.
def student_name():
#*** ADD OR CHANGE CODE HERE ***
   return "Lin, Billy" # For an autograder.

STATES=None; ACTIONS=None; UQV_callback=None; Q_VALUES=None
is_valid_goal_state=None; Terminal_state = None
USE_EXPLORATION_FUNCTION = None
INITIAL_STATE = None
def setup(states, actions, q_vals_dict, update_q_value_callback,\
    goal_test, terminal, use_exp_fn=False):
    '''This method is called by the GUI the first time a Q_Learning
    menu item is selected. It may be called again after the user has
    restarted from the File menu.
    Q_VALUES starts out with all Q-values at 0.0 and a separate key
    for each (s, a) pair.'''
    global STATES, ACTIONS, UQV_callback, Q_VALUES, is_valid_goal_state
    global USE_EXPLORATION_FUNCTION, Terminal_state
    STATES = states
    ACTIONS = actions
    Q_VALUES = q_vals_dict
    UQV_callback = update_q_value_callback
    is_valid_goal_state = goal_test
    Terminal_state = terminal
    USE_EXPLORATION_FUNCTION = use_exp_fn
    if USE_EXPLORATION_FUNCTION:
#*** ADD OR CHANGE CODE HERE ***
         # Change this if you implement an exploration function:
         print("You have not implemented an exploration function")

PREVIOUS_STATE = None
LAST_ACTION = None
def set_starting_state(s):
    '''This is called by the GUI when a new episode starts.
    Do not change this function.'''
    global INITIAL_STATE, PREVIOUS_STATE
    print("In Q_Learn, setting the starting state to "+str(s))
    INITIAL_STATE = s
    PREVIOUS_STATE = s

ALPHA = 0.5
CUSTOM_ALPHA = False
EPSILON = 0.5
CUSTOM_EPSILON = False
GAMMA = 0.9
def set_learning_parameters(alpha, epsilon, gamma):
    ''' Called by the system. Do not change this function.'''
    global ALPHA, EPSILON, CUSTOM_ALPHA, CUSTOM_EPSILON, GAMMA
    ALPHA = alpha
    EPSILON = epsilon
    GAMMA = gamma
    if alpha < 0: CUSTOM_ALPHA = True
    else: CUSTOM_ALPHA = False
    if epsilon < 0: CUSTOM_EPSILON = True
    else: CUSTOM_EPSILON = False

def update_Q_value(previous_state, previous_action, new_value):
    '''Whenever your code changes a value in Q_VALUES, it should
    also call this method, so the changes can be reflected in the
    display.
    Do not change this function.'''
    UQV_callback(previous_state, previous_action, new_value)

def handle_transition(action, new_state, r):
    '''When the user drives the agent, the system will call this function,
    so that you can handle the learning that should take place on this
    transition.'''
    global PREVIOUS_STATE

#*** ADD OR CHANGE CODE HERE ***
    max_q = 0
    for a in ACTIONS:
        max_q = max(Q_VALUES[(new_state, a)], max_q)
    sample = r + GAMMA*max_q
    new_q_value = (1-ALPHA)*Q_VALUES[(PREVIOUS_STATE, action)] + ALPHA*sample
    
    # You should call update_Q_value before returning.  E.g.,
    Q_VALUES[(PREVIOUS_STATE, action)] = new_q_value
    update_Q_value(PREVIOUS_STATE, action, new_q_value)
    
    print("Transition to state: "+str(new_state)+"\n with reward "+str(r))
    PREVIOUS_STATE = new_state
    return # Nothing needs to be returned.

import random

def choose_next_action(s, r, terminated=False):
    '''When the GUI or engine calls this, the agent is now in state s,
    and it receives reward r.
    If terminated==True, it's the end of the episode, and this method
    can just return None after you have handled the transition.
    Use this information to update the q-value for the previous state
    and action pair.  
     
    Then the agent needs to choose its action and return that.
    '''
    global INITIAL_STATE, PREVIOUS_STATE, LAST_ACTION
    # Unless s is the initial state, compute a new q-value for the
    # previous state and action.
    if not (s==INITIAL_STATE):
        # Compute your update here.
        # if CUSTOM_ALPHA is True, manage the alpha values over time.
        # Otherwise go with the fixed value.
        new_qval = -99 # A bogus value for now.

        max_q = 0
        for a in ACTIONS:
            max_q = max(Q_VALUES[(s, a)], max_q)
        sample = r + GAMMA*max_q
        new_qval = (1-ALPHA)*Q_VALUES[(PREVIOUS_STATE, LAST_ACTION)] + ALPHA*sample
        # Save it in the dictionary of Q_VALUES:
        Q_VALUES[(PREVIOUS_STATE, LAST_ACTION)] = new_qval

        # Then let the Engine and GUI know about the new Q-value.
        update_Q_value(PREVIOUS_STATE, LAST_ACTION, new_qval)
         
     # Now select an action according to your Q-Learning criteria, such
     # as expected discounted future reward vs exploration.
    if is_valid_goal_state(s):
        action = "Exit"
    elif s==Terminal_state:
        action = None
    else:
        if USE_EXPLORATION_FUNCTION:
            # Change this if you implement an exploration function:
            #*** ADD OR CHANGE CODE HERE ***
            print("You have not implemented an exploration function")

        # If EPSILON > 0, or CUSTOM_EPSILON is True,
        # then use epsilon-greedy learning here.
        elif EPSILON > 0 or CUSTOM_EPSILON:
        # In order to access q-values, simply get them from the dictionary, e.g.,
        # some_qval = Q_VALUES[(some_state, some_action)] 
            if random.uniform(0, 1) < EPSILON:
                action = random.choice(ACTIONS)
            else:
                actions_available = [action for (state, action) in Q_VALUES.keys() if state == s]
                action = actions_available[0] #initialize chosen action to be the first in the list
                max_val = Q_VALUES[(s, action)] 
                for a in actions_available:
                    new_val = Q_VALUES[(s, a)]
                    if new_val > max_val:
                        max_val = new_val
                        action = a 
                        
    LAST_ACTION = action # remember this for next time
    PREVIOUS_STATE = s   #    "       "    "   "    "
    return action

Policy = {}
def extract_policy(S, A):
    '''Return a dictionary mapping states to actions. Obtain the policy
    using the q-values most recently computed.
    Ties between actions having the same (s, a) value can be broken arbitrarily.
    Reminder: goal states should map to the Exit action, and no other states
    should map to the Exit action.
    '''
    global Policy
    Policy = {}
#*** ADD OR CHANGE CODE HERE ***  
    for s in S:
        #extract all tuples (s, a) that start from the current state: state_action = [(s, a0), (s, a1), (s, a2)...]
        state_action = [(state, action) for (state, action) in Q_VALUES.keys() if state == s]
        max_sa = state_action[0] #initialize into the first state-action pair's value
        max_val = Q_VALUES[max_sa] 
        for sa in state_action:
            new_val = Q_VALUES[sa]
            if new_val > max_val:
                max_sa = sa
                max_val = new_val
        Policy[s] = max_sa[1]
    return Policy
