import sys
import importlib
import TTS_State
import traceback

#check file input is sufficient
if len(sys.argv) < 2:
  print("Usage: python3 agent_checker.py <agent module>")
  print("  for example:")
  print("python3 agent_checker.py robthomp_TTS_agent")
  exit(0)

#try to import agent  
try:
	user_player = sys.argv[1]
	Player = importlib.import_module(user_player)
except Exception as e:
	print("An exception happened when trying to import your agent:")
	print(e)
	exit(0) 

#start checking
print("""This file will check that your agent has the correct function definitions and can perform
basic operations. Passing this checker does not guarantee your agent will get full points 
during grading but it is a good start.""")

board = [
        ['-','-','-','-'],
        ['-','W',' ','-'],
        ['-',' ',' ','-'],
        ['-','-','-','-'],]

#check static eval methods
print("1. Checking Static Eval")

#basic eval
try:
	state = TTS_State.TTS_State(board)
	state.__class__ = Player.MY_TTS_State
	val = state.basic_static_eval()
	assert(val == 3)
	print(" 1.1 basic static eval worked and returned the expected value ✓")	
except Exception:
	print(" 1.2 an exception happened when trying to call your basic static eval:")
	traceback.print_exc()

#custom eval
try:
	state = TTS_State.TTS_State(board)
	state.__class__ = Player.MY_TTS_State
	val = state.custom_static_eval()
	print(" 1.2 custom static eval returned a value without error ✓")	
except Exception:
	print(" 1.2 an exception happened when trying to call your custom static eval:")
	traceback.print_exc()

print("2. Agent Personality")

#who_am_i
try:
	result = Player.who_am_i()
	assert(not result == '')
	print(" 2.1 Agent defines non-empty who_am_i() ✓")
except Exception:
	print(" 2.1 Exception when checking who_am_i()")
	traceback.print_exc()

#moniker
try:
	result = Player.moniker()
	assert(not result == '')
	print(" 2.2 Agent defines non-empty moniker() ✓")
except Exception:
	print(" 2.2 Exception when checking moniker()")
	traceback.print_exc()

print("3. Agent Search")

#get ready
try:
	state = TTS_State.TTS_State(board)
	Player.get_ready(state, 3, 'W', 'player2')
	print(" 3.1 Agent runs get_ready() without error ✓")
except Exception:
	print(" 3.1 Exception when running get_ready()")
	traceback.print_exc()

#parameterized minimax
try:
	state = TTS_State.TTS_State(board)
	results = Player.parameterized_minimax(current_state=state)
	assert("CURRENT_STATE_STATIC_VAL" in results.keys())
	assert("N_STATES_EXPANDED" in results.keys())
	assert("N_STATIC_EVALS" in results.keys())
	assert("N_CUTOFFS" in results.keys())
	print(" 3.2 Agent runs basic parameterized_minimax() without error and returns correct format ✓")
except Exception:
	print(" 3.2 Exception when running parameterized_minimax()")
	traceback.print_exc()

#alpha beta
try:
	state = TTS_State.TTS_State(board)
	results = Player.parameterized_minimax(current_state=state, max_ply=2, use_alpha_beta=True, use_basic_static_eval=True)
	assert(results["CURRENT_STATE_STATIC_VAL"] == 1)
	assert(results["N_STATES_EXPANDED"] == 4)
	assert(results["N_STATIC_EVALS"] == 4)
	assert(results["N_CUTOFFS"] == 2)
	print(" 3.3 Agent returned correct values for a (simple) alpha-beta test ✓")
except Exception:
	print(" 3.3 Exception when running parameterized_minimax() with alpha beta")
	traceback.print_exc()