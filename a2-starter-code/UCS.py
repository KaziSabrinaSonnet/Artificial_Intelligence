'''UCS.py
by Kazi Sabrina Sonnet
UWNetID: ksonnet
Student number: 1870554

Assignment 2, in CSE 415, Autumn 2019.

Uniform Cost Search Algorithm
 
'''

VERBOSE = True  # Set to True to see progress; but it slows the search.

import sys

if sys.argv==[''] or len(sys.argv)<2:
  try:
    import EightPuzzle as Problem
  except:
    print("Note that the EightPuzzle formulation will be used in Assignment 3, not Assignment 2")
    print("Try python3 UCS.py FranceWithCosts")

else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to UCS, by YOUR NAME HERE!")

COUNT = None # Number of nodes expanded.
MAX_OPEN_LENGTH = None # How long OPEN ever gets.
SOLUTION_PATH = None # List of states from initial to goal, along lowest-cost path.
TOTAL_COST = None # Sum of edge costs along the lowest-cost path.
BACKLINKS = {} # Predecessor links, used to recover the path.

# The value g(s) represents the cost along the best path found so far
# from the initial state to state s.
g = {} # We will use a global hash table to associate g values with states.

class My_Priority_Queue:
  def __init__(self):
    self.q = [] # Actual data goes in a list.


  def __contains__(self, elt):
    '''If there is a (state, priority) pair on the list
    where state==elt, then return True.'''
    #print("In My_Priority_Queue.__contains__: elt= ", str(elt))
    for pair in self.q:
      if pair[0]==elt: return True
    return False

  def delete_min(self):
    ''' Standard priority-queue dequeuing method.'''
    if self.q==[]: return [] # Simpler than raising an exception.
    temp_min_pair = self.q[0]
    temp_min_value = temp_min_pair[1]
    temp_min_position = 0
    for j in range(1, len(self.q)):
      if self.q[j][1] < temp_min_value:
        temp_min_pair = self.q[j]
        temp_min_value = temp_min_pair[1]  
        temp_min_position = j
    del self.q[temp_min_position]
    return temp_min_pair

  def insert(self, state, priority):
    '''We do not keep the list sorted, in this implementation.'''
    #print("calling insert with state, priority: ", state, priority)

    if self[state] != -1:
      print("Error: You're trying to insert an element into a My_Priority_Queue instance,")
      print(" but there is already such an element in the queue.")
      return
    self.q.append((state, priority))

  def __len__(self):
    '''We define length of the priority queue to be the
    length of its list.'''
    return len(self.q)

  def __getitem__(self, state):
    '''This method enables Pythons right-bracket syntax.
    Here, something like  priority_val = my_queue[state]
    becomes possible. Note that the syntax is actually used
    in the insert method above:  self[state] != -1  '''
    for (S,P) in self.q:
      if S==state: return P
    return -1  # This value means not found.

  def __delitem__(self, state):
    '''This method enables Python's del operator to delete
    items from the queue.'''
    #print("In MyPriorityQueue.__delitem__: state is: ", str(state))
    for count, (S,P) in enumerate(self.q):
      if S==state:
        del self.q[count]
        return

  def __str__(self):
    txt = "My_Priority_Queue: ["
    for (s,p) in self.q: txt += '('+str(s)+','+str(p)+') '
    txt += ']'
    return txt

def runUCS():
  '''This is an encapsulation of some setup before running
  UCS, plus running it and then printing some stats.'''
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH, SOLUTION_PATH
  COUNT = 0
  BACKLINKS = {}
  MAX_OPEN_LENGTH = 0
  SOLUTION_PATH = UCS(initial_state)
  print(str(COUNT)+" states expanded.")
  print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))

def UCS(initial_state):
  '''Uniform Cost Search. This is the actual algorithm.'''
  global g, COUNT, BACKLINKS, MAX_OPEN_LENGTH, CLOSED, TOTAL_COST
  CLOSED = []
  BACKLINKS[initial_state] = None
  # The "Step" comments below help relate UCS's implementation to
  # those of Depth-First Search and Breadth-First Search.

# STEP 1a. Put the start state on a priority queue called OPEN
  OPEN = My_Priority_Queue()
  OPEN.insert(initial_state, 0)
# STEP 1b. Assign g=0 to the start state.
  g[initial_state]=0.0

# STEP 2. If OPEN is empty, output “DONE” and stop.
  while OPEN.__len__() > 0: # ***STUDENTS CHANGE THIS CONDITION***
    # LEAVE THE FOLLOWING CODE IN PLACE TO INSTRUMENT AND/OR DEBUG YOUR IMPLEMENTATION
    if VERBOSE: report(OPEN, CLOSED, COUNT)
    if len(OPEN)>MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)

# STEP 3. Select the state on OPEN having lowest priority value and call it S.
#         Delete S from OPEN.
#         Put S on CLOSED.
#         If S is a goal state, output its description
    (S,P) = OPEN.delete_min()
    #print("In Step 3, returned from OPEN.delete_min with results (S,P)= ", (str(S), P))
    CLOSED.append(S)

    if Problem.GOAL_TEST(S):
      # ***STUDENTS CHANGE THE BODY OF THIS IF.***
      #HANDLE THE BACKTRACING, RECORDING THE SOLUTION AND TOTAL COST,
      # AND RETURN THE SOLUTION PATH, TOO.
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      path = backtrace(S)
      if len(path) < 2:
        TOTAL_COST = 0
      else:
        TOTAL_COST = path[0].edge_distance(path[1])
      for i in range(2, len(path)):
        TOTAL_COST += path[i-1].edge_distance(path[i])
      print('Total cost of solution path found: '+str(TOTAL_COST))
      return path
    COUNT += 1

# STEP 4. Generate each successor of S
#         and if it is already on CLOSED, delete the new instance.
    for op in Problem.OPERATORS:
      if op.precond(S):
        new_state = op.state_transf(S)
        if not (new_state in CLOSED):
          new_state_cost = g[S] + S.edge_distance(new_state)
          if new_state not in g or g[new_state] > new_state_cost:
            g[new_state] = new_state_cost
            BACKLINKS[new_state] = S 
          if OPEN.__contains__(new_state):
            if OPEN.__getitem__(new_state) > new_state_cost:
              OPEN.__delitem__(new_state)
              OPEN.insert(new_state, new_state_cost)
          else:
            OPEN.insert(new_state, new_state_cost)

   # ***STUDENTS IMPLEMENT THE GENERATION AND HANDLING OF SUCCESSORS HERE,
   # USING THE GIVEN PRIORITY QUEUE FOR THE OPEN LIST, AND
   # DETERMINING THE SHORTEST DISTANCE KNOWN SO FAR FROM THE INITIAL STATE TO
   # EACH SUCCESSOR.***

  # STEP 6. Go to Step 2.
  return None  # No more states on OPEN, and no goal reached.

def print_state_queue(name, q):
  print(name+" is now: ",end='')
  print(str(q))

def backtrace(S):
  global BACKLINKS
  path = []
  while S:
    path.append(S)
    S = BACKLINKS[S]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(s)
  return path
  
def report(open, closed, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("len(CLOSED)="+str(len(closed)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
  runUCS()

