from referee.game import PlayerColor, Action, PlaceAction, Coord
from agent.board import Board
from agent.program import Agent as minimax
import math


BOARD_N = 11

mini = minimax(PlayerColor.RED)
a = '''
r r r . b b . r r b b 
r r r b b b r r r r . 
r r r r b . b r r . r 
. . r r r b b b b r r 
. . . . . . . . . . . 
r b b b . r b b . r r 
r . b b b r r b b r r 
. . b . r r r . b . b 
b b b . r r . . b b b 
. r . r r . r b b b b 
. r r r b b r r . b b
'''
a = a.replace(" ", "").strip("\n").split("\n")

red = set()
blue = set()

for i in range(BOARD_N):
    for j in range(BOARD_N):
        if a[i][j] == 'r':
            red.add(Coord(i, j))
        elif a[i][j] == 'b':
            blue.add(Coord(i, j))

board = Board(red, blue, PlayerColor.RED)
board.turn_count = 30
# putting turn count to be 0 or 1 here doesnt work because they have different generate_moves()
print(board.render())

valid_moves_dict: dict[int, set[PlaceAction]] = {}
valid_moves_dict[hash(mini.board)] = mini.board.generate_all_moves()

depth = 4
print("minimax depth =", depth)
eval, action = mini.minimax_ab(board, depth, -math.inf, math.inf, valid_moves_dict)
board.apply_action(action)
print("minimax eval = ", eval)
print(board.render())