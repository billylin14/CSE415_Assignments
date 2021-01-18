'''Farmer_Fox.py
by Billy Lin
UWNetID: lin14
Student number: 1765327

Assignment 2, in CSE 415, Winter 2021.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name, uwnetid, and 7-digit student number are given above in 
# the format shown.

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Farmer_Fox"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Billy Lin']
PROBLEM_CREATION_DATE = "16-JAN-2021"
PROBLEM_DESC=\
'''This formulation of the Towers of Hanoi problem uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.
'''
#</METADATA>

class State:
  def __init__(self, d):
    self.d = d

  def __eq__(self,s2):
    for side in ['left', 'right']:
      self.d[side]
      s2.d[side].sort()
      if self.d[side] != s2.d[side]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    # Might not be needed in normal operation with GUIs.
    return "\n" + '[' + ' '.join(self.d['left']) + " || " + ' '.join(self.d['right']) + ']' + "\n"

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    for side in ['left','right']:
      news.d[side]=self.d[side][:]
    return news

  def can_move(self,items,From):
    '''Tests whether it's legal to move a disk in state s
       from the From peg to the To peg.'''
    # print("To move = ", items)
    # print("original = ", self.d[From])
    try:
        #check if items exist in From
        if any(item not in self.d[From] for item in items): 
          # print("selected item does not exist\n")
          return False
        #check if trying to move without moving the Farmer together
        elif any(item == 'Farmer' for item in items): 
          #check if the result state is illegal: (1) Grain+Chicken (2) Fox+Chichen (3) Fox+Chicken+Grain (4) Farmer+Grain (5) Farmer+Fox (6) Farmer
          result = [x for x in self.d[From] if x not in items] #removes elements in items
          # print("After removal = ", result)
          illegal = [['Grain', 'Chicken'], ['Fox', 'Chicken'], ['Fox', 'Chicken', 'Grain'], ['Farmer', 'Grain'], ['Farmer', 'Fox'], ['Farmer']]
          result.sort()
          for state in illegal:
              state.sort()
              if result==state: 
                # print("this is illegal\n")
                return False
          # print("this is valid\n")
          return True
    except (Exception) as e:
      print(e)

  def move(self,items,From,To):
    '''Assuming it's legal to make the move, this computes
       the new state resulting from moving at most 2 items from one side to another'''
    news = self.copy() # start with a deep copy.
    for item in items:
        news.d[From].remove(item)
        news.d[To].append(item)
        news.d[From].sort()
        news.d[To].sort()
    return news # return new state
  
def goal_test(s):
  '''If every item is on the right, then s is a goal state.'''
  s.d['right'].sort()
  goal = ['Farmer', 'Fox', 'Chicken', 'Grain']
  goal.sort()
  return s.d['left']==[] and s.d['right']==goal

def goal_message(s):
  return "You have solved the puzzle!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

#</COMMON_CODE>

#<INITIAL_STATE>
INITIAL_DICT = {'left': ['Farmer', 'Fox', 'Chicken', 'Grain'], 'right':[] }
CREATE_INITIAL_STATE = lambda: State(INITIAL_DICT)
#DUMMY_STATE =  {'peg1':[], 'peg2':[], 'peg3':[] }
#</INITIAL_STATE>

#<OPERATORS>
combinations = [(['Farmer'], 'left'), (['Farmer', 'Chicken'], 'left'), (['Farmer', 'Fox'], 'left'), (['Farmer', 'Grain'], 'left'),
                  (['Farmer'], 'right'), (['Farmer', 'Chicken'], 'right'), (['Farmer', 'Fox'], 'right'), (['Farmer', 'Grain'], 'right')]
OPERATORS = [Operator("Move "+ " and ".join(items) +" from "+ direction,
                      lambda s,items=items,From=direction: s.can_move(items,From),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,items=items,From=direction,To='right' if direction=='left' else 'left': s.move(items,From,To) )
             for (items, direction) in combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>


