# Functions that implement the game-playing logic
# Can be called by the Agent

# Things to consider:
#   how should we store the board state (still tup/dict?) - done for now
#   implement minimax
#       design evaluation function
#   integrate with referee - check goal state etc.


from .part_a.core import PlayerColor, Coord, PlaceAction, BOARD_N
from .part_a.program import State
from .part_a.utils import render_board
from queue import PriorityQueue as pq
import time, math

def test():   
    print("test")
