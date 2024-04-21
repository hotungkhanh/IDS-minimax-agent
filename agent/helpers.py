# Functions that implement the game-playing logic
# Can be called by the Agent

# Things to consider:
#   how should we store the board state (still tup/dict?)
#   implement minimax
#       design evaluation function
#   integrate with referee - check goal state etc.


from .part_a.core import PlayerColor, Coord, PlaceAction, BOARD_N
from .part_a.program import State
from .part_a.utils import render_board
from queue import PriorityQueue as pq
import time

def test():   
    print("test")

def minimax(state: State, depth: int, maximisingPlayer: bool):
    ''' 
    recursive pseudocode:

    if depth == 0 or game over in state then:
        return static eval of state

    if maximisingPlayer then:
        maxEval = -infinity
        for each child of state:
            eval = minimax(child, depth - 1, false)
            maxEval = max(maxEval, eval)
        return maxEval
    else:
        minEval = +infinity
        for each child of state:
            eval = minimax(child, depth - 1, true)
            maxEval = min(minEval, eval)
        return minEval
    '''  
    
    return

