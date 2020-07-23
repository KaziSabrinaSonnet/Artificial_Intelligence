''' abutenko_TTS_agent.py
Andrey Butenko (abutenko@uw.edu)
An agent that plays Toro-Tile Straight using iterative deepening,
minimax search, and alpha-beta pruning. This agent heavily prioritizes
states with many tiles in a row. The agent's personality is kind.
'''

from TTS_State import TTS_State
import math
import time
import random

data_k = 0
data_what_side_i_play = 'W'

USE_CUSTOM_STATIC_EVAL_FUNCTION = True
REMARKS = [
  'This is one koalaty game!',
  'Here\'s my move!',
  'Good play!',
  'Let\'s see how this goes!',
  'This is fun!',
  'A lot of math went into this move!',
  'Nice move! What do you think of this?',
  'This is fun!'
]

class MY_TTS_State(TTS_State):
  """ Subclass of TTS_State with custom functions for performing static evaluations
  of the state and for tracking the alpha and beta values of the state.
  """

  def static_eval(self):
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      return self.custom_static_eval()
    else:
      return self.basic_static_eval()

  def basic_static_eval(self):
    return(basic_static_eval(self))

  def custom_static_eval(self):
    return(custom_static_eval(self))

  def print(self):
    print(self.whose_turn + ' [' + str(self.get_alpha()) + ', ' + str(self.get_beta()) + ']')
    print(str(self.board).replace('], ', '],\n '))

  def get_alpha(self):
    if not hasattr(self, 'alpha'):
      self.alpha = -1000.0
    return self.alpha

  def get_beta(self):
    if not hasattr(self, 'beta'):
      self.beta = +1000.0
    return self.beta

  def set_alpha(self, alpha):
    self.alpha = alpha

  def set_beta(self, beta):
    self.beta = beta
  
  def copy(self):
    clone = super().copy()
    clone.__class__ = MY_TTS_State
    clone.set_alpha(self.get_alpha())
    clone.set_beta(self.get_beta())
    return clone


def parameterized_minimax(current_state = None, max_ply = 2, use_alpha_beta = False, use_basic_static_eval = True):
  """ Given a state and configurable parameters, performs minimax and returns the
  current state static value, the number of states expanded, the number of static
  evaluations, and the number of cutoffs that occurred in performing the minimax.
  """
  current_state.__class__ = MY_TTS_State

  DATA = {}
  DATA['CURRENT_STATE_STATIC_VAL'] = -1000.0 if current_state.whose_turn == 'W' else +1000.0
  DATA['N_STATES_EXPANDED'] = 0
  DATA['N_STATIC_EVALS'] = 0
  DATA['N_CUTOFFS'] = 0

  num_states_considered = 0

  if max_ply > 0:
    DATA['N_STATES_EXPANDED'] += 1
    should_cut_off = False
    for y in range(len(current_state.board)):
      for x in range(len(current_state.board[y])):
        piece = current_state.board[y][x]
        if piece == ' ' and not should_cut_off:
          num_states_considered += 1
          # print('Now considering @ ' + str(max_ply) + ' ==================')
          # current_state.print()
          new_state = current_state.copy()
          new_state.board[y][x] = new_state.whose_turn
          new_state.whose_turn = 'W' if new_state.whose_turn == 'B' else 'B'

          RESULT = parameterized_minimax(current_state = new_state, max_ply = max_ply - 1, use_alpha_beta = use_alpha_beta, use_basic_static_eval = use_basic_static_eval)
          DATA['N_STATES_EXPANDED'] += RESULT['N_STATES_EXPANDED']
          DATA['N_STATIC_EVALS'] += RESULT['N_STATIC_EVALS']
          DATA['N_CUTOFFS'] += RESULT['N_CUTOFFS']

          if current_state.whose_turn == 'W':
            DATA['CURRENT_STATE_STATIC_VAL'] = max(DATA['CURRENT_STATE_STATIC_VAL'], RESULT['CURRENT_STATE_STATIC_VAL'])
          else:
            DATA['CURRENT_STATE_STATIC_VAL'] = min(DATA['CURRENT_STATE_STATIC_VAL'], RESULT['CURRENT_STATE_STATIC_VAL'])
          
          if use_alpha_beta:
            if current_state.whose_turn == 'W':
              current_state.set_alpha(max(DATA['CURRENT_STATE_STATIC_VAL'], RESULT['CURRENT_STATE_STATIC_VAL']))
            else:
              current_state.set_beta(min(DATA['CURRENT_STATE_STATIC_VAL'], RESULT['CURRENT_STATE_STATIC_VAL']))

            if current_state.get_alpha() >= current_state.get_beta():
              DATA['N_CUTOFFS'] += 1
              should_cut_off = True
  
  if max_ply <= 0 or num_states_considered == 0:
    # print('Now considering @ ' + str(max_ply) + ' ==================')
    # current_state.print()

    DATA['CURRENT_STATE_STATIC_VAL'] = current_state.basic_static_eval() if use_basic_static_eval else current_state.custom_static_eval()
    DATA['N_STATIC_EVALS'] += 1
  
  if use_alpha_beta and max_ply > 0 and num_states_considered > 0:
    current_beta = current_state.get_beta()
    current_alpha = current_state.get_alpha()
    DATA['alpha'] = current_beta
    DATA['beta'] = current_alpha

    if DATA['alpha'] == 1000.0:
      DATA['alpha'] = -1000.0
    if DATA['beta'] == -1000.0:
      DATA['beta'] = -1000.0
    
    # print('Returning alpha ' + str(DATA['alpha']))
    # print('Returning beta ' + str(DATA['beta']))
  return(DATA)


def get_ready(initial_state, k, what_side_i_play, opponent_moniker):
  """ Given the initial_state and other data related to the game, stores the values for use in algorithms.
  """
  global data_k, data_what_side_i_play
  data_k = k
  data_what_side_i_play = what_side_i_play
  return('OK')

def who_am_i():
  """ Returns introduction.
  """
  return('I am Koala! I am a kind agent who loves getting multiple tiles in a row. I was developed by Andrey Butenko (abutenko@uw.edu)')

def moniker():
  """ Returns name.
  """
  return('Koala')

def _minimax(current_state = None, deadline = time.time() + 100, max_ply = 2):
  """ Given the current state, a deadline for calculations, and a ply, performs minimax
  with alpha-beta cutoffs and returns an object with the current state static value and
  the position of the best move.
  """
  current_state = current_state.copy()
  current_state.__class__ = MY_TTS_State

  DATA = {}
  DATA['CURRENT_STATE_STATIC_VAL'] = -math.inf if current_state.whose_turn == 'W' else math.inf
  DATA['BEST_MOVE'] = False

  num_states_considered = 0

  if max_ply <= 0:
    # print('Now considering @ ' + str(max_ply) + ' ==================')
    # current_state.print()

    DATA['CURRENT_STATE_STATIC_VAL'] = current_state.custom_static_eval()
  else:
    should_cut_off = False
    for i in range(len(current_state.board)):
      for j in range(len(current_state.board[0])):
        piece = current_state.board[i][j]
        if piece == ' ' and not should_cut_off and time.time() < deadline - 0.5:
          num_states_considered += 1
          # print('Now considering @ ' + str(max_ply) + ' ==================')
          # current_state.print()

          new_state = current_state.copy()
          new_state.board[i][j] = new_state.whose_turn
          new_state.whose_turn = 'W' if new_state.whose_turn == 'B' else 'B'

          RESULT = _minimax(current_state = new_state, max_ply = max_ply - 1)

          # print('debug current_state.whose_turn = ' +str(current_state.whose_turn))
          # print('debug DAT = ' +str(DATA['CURRENT_STATE_STATIC_VAL']))
          # print('debug RES = ' +str(RESULT['CURRENT_STATE_STATIC_VAL']))

          if current_state.whose_turn == 'W' and RESULT['CURRENT_STATE_STATIC_VAL'] >= DATA['CURRENT_STATE_STATIC_VAL']:
            DATA['CURRENT_STATE_STATIC_VAL'] = RESULT['CURRENT_STATE_STATIC_VAL']
            current_state.set_alpha(RESULT['CURRENT_STATE_STATIC_VAL'])
            DATA['BEST_MOVE'] = (i, j)
            # DATA['BEST_STATE'] = TTS_State(new_state.board, new_state.whose_turn)
          
          if current_state.whose_turn == 'B' and RESULT['CURRENT_STATE_STATIC_VAL'] <= DATA['CURRENT_STATE_STATIC_VAL']:
            DATA['CURRENT_STATE_STATIC_VAL'] = RESULT['CURRENT_STATE_STATIC_VAL']
            current_state.set_beta(RESULT['CURRENT_STATE_STATIC_VAL'])
            DATA['BEST_MOVE'] = (i, j)
            # DATA['BEST_STATE'] = TTS_State(new_state.board, new_state.whose_turn)
          
          if current_state.get_alpha() >= current_state.get_beta():
            should_cut_off = True
    
    if num_states_considered == 0:
      DATA['CURRENT_STATE_STATIC_VAL'] = current_state.custom_static_eval()
    
    current_beta = current_state.get_beta()
    current_alpha = current_state.get_alpha()
    DATA['alpha'] = current_beta
    DATA['beta'] = current_alpha

    if DATA['alpha'] == math.inf:
      DATA['alpha'] = -math.inf
    if DATA['beta'] == -math.inf:
      DATA['beta'] = -math.inf

  return(DATA)

def take_turn(current_state, opponents_utterance, time_limit = 3):
  """ Given a state, perform iterative deepening within the provided time limit to determine
  the best move.
  """
  # current_state.__class__ = MY_TTS_State
  new_state = MY_TTS_State(current_state.board, current_state.whose_turn)
  who = current_state.whose_turn
  deadline = time.time() + time_limit
  ply = 0
  while time.time() < deadline - 0.5:
    ply += 1
    try:
      prev_minimax_result = minimax_result
    except NameError:
      pass
    minimax_result = _minimax(current_state, deadline = deadline, max_ply = ply)
  
  if (data_what_side_i_play == 'W' and prev_minimax_result['CURRENT_STATE_STATIC_VAL'] > minimax_result['CURRENT_STATE_STATIC_VAL']) or (data_what_side_i_play == 'B' and prev_minimax_result['CURRENT_STATE_STATIC_VAL'] < minimax_result['CURRENT_STATE_STATIC_VAL']):
    minimax_result = prev_minimax_result
  move = minimax_result['BEST_MOVE']
  if move == False:
    return [[False, current_state], 'I have no-where to go!']
  # print('BEST_MOVE: ' + str(minimax_result['BEST_MOVE']))
  (i, j) = move
  # print('x = ' + str(i))
  # print('y = ' + str(y))
  new_state.board[i][j] = who
  # print('value there = ' + str(new_state.board[i][j]))
  
  new_state.whose_turn = 'W' if who == 'B' else 'B'
  # print('NEW_STATE: ' + str(new_state))

  return [[move, new_state], random.choice(REMARKS)]

def _get_piece(self, x, y):
  """ Given a state and an (x, y) position, returns piece at that toroidal
  position. Supports values outside of range of board (too low or too high).
  """
  x = x % len(self.board[0])
  y = y % len(self.board)
  return self.board[y][x]

def basic_static_eval(self):
  """ Function to calculate TWF - TBF.
  TWF: degrees of freedom for player W
  TBF: degrees of freedom for player B
  degrees of freedom: value in range 0 to 8 representing how many adjacent
    tiles are open.
  """
  twf = 0 # degrees of freedom for W
  tbf = 0 # degrees of freedom for B
  for y in range(len(self.board)):
    for x in range(len(self.board[y])):
      piece = _get_piece(self, x, y)
      # print('(' + str(x) + ', ' + str(y) + '): ' + piece)
      if piece == 'W' or piece == 'B':
        dof_change = 0
        for dy in [-1, 0, 1]:
          for dx in [-1, 0, 1]:
            # print('* (' + str(x + dx) + ', ' + str(y + dy) + '): ' + _get_piece(self, x + dx, y + dy))
            if _get_piece(self, x + dx, y + dy) == ' ':
              dof_change += 1
        if piece == 'W':
          twf += dof_change
        if piece == 'B':
          tbf += dof_change
  return(twf - tbf)

def _custom_static_eval_check_axis(self, x, y, xi_fn, yi_fn):
  """ On an axis defined by the xi_fn and yi_fn functions starting at the coordinates (x, y),
  count the number of white, black, empty, and blocked tiles as well as the number of white
  tiles in a row and the number of black tiles in a row. Using this data, produces a score for the
  current state prioritizing number of tiles in a row.
  """
  w_in_a_row = 0
  b_in_a_row = 0
  last = ' '
  num_w = 0
  num_b = 0
  num_d = 0
  num_a = 0
  debug = ''
  for i in range(-math.floor(data_k / 2), math.ceil(data_k / 2) + 1):
    if i != 0:
      piece2 = _get_piece(self, x + xi_fn(i), y + yi_fn(i))
      # print('debug ' + str(xi_fn(i) - i))
      if piece2 == 'W':
        num_w += 1
      if piece2 == 'B':
        num_b += 1
      if piece2 == '-':
        num_d += 1
      if piece2 == ' ':
        num_a += 1
      
      if last == ' ' and piece2 == 'W':
        last = piece2
        w_in_a_row = 0
      if last == ' ' and piece2 == 'B':
        last = piece2
        b_in_a_row = 0
      
      if last == 'B' and piece2 == 'W':
        last = 'W'
      if last == 'W' and piece2 == 'B':
        last = 'B'
      if piece2 == '-':
        last = ' '
      
      if piece2 == last and piece2 == 'W':
        w_in_a_row += 1
      if piece2 == last and piece2 == 'B':
        b_in_a_row += 2

      # debug += piece2 + ', '
  
  if num_w == data_k:
    return 1000000
  if num_b == data_k:
    return -1000000
  return 20 * w_in_a_row - (20 * b_in_a_row) + 15 * num_w - (15 * num_b) - (5 * num_d) + (4 * num_a)

def custom_static_eval(self):
  """ Performs a custom static evaluation of the current state using the criteria in the
  _custom_static_eval_check_axis function.
  """
  score = 0

  for x in range(len(self.board)):
    for y in range(len(self.board[0])):
      piece = _get_piece(self, x, y)
      if piece == 'W' or piece == 'B':
        score += _custom_static_eval_check_axis(self, x, y, lambda i: i, lambda i: 0)
        score += _custom_static_eval_check_axis(self, x, y, lambda i: i, lambda i: i)
        score += _custom_static_eval_check_axis(self, x, y, lambda i: 0, lambda i: i)
  return score

if __name__ == "__main__":
  board = [
        ['-','-','-','-'],
        ['-','W',' ','-'],
        ['-',' ',' ','-'],
        ['-','-','-','-'],]
  
  print('basic_static_eval should return 3: ' + str(basic_static_eval(TTS_State(board))))
  print('parameterized_minimax should return (1, 4, 6, 0): ' + str(parameterized_minimax(TTS_State(board))))
  print('parameterized_minimax alpha_beta should return (1, 4, 4, 2): ' + str(parameterized_minimax(TTS_State(board), use_alpha_beta = True)))
  # print('parameterized_minimax alpha_beta should return (1, 4, 4, 2): ' + str(parameterized_minimax(TTS_State(board), max_ply = 20, use_alpha_beta = True)))

