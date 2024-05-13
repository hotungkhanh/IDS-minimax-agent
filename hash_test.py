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
print(a)

red = set()
blue = set()

for i in range(BOARD_N):
    for j in range(BOARD_N):
        if a[i][j] == 'r':
            red.add(Coord(i, j))
        elif a[i][j] == 'b':
            blue.add(Coord(i, j))

board = Board(red.copy(), blue.copy(), PlayerColor.RED, turn_count=148)
print(board.render())

value = mini.minimax_ab(board, 3, -math.inf, math.inf, PlayerColor.RED)
print(value[0])
print("Board:")
print(value[1].render())



# board1 = Board(set((Coord(1, 2), Coord(2, 2))), 
#                set((Coord(3, 4), Coord(4, 4))), 
#                PlayerColor.RED,
#                )

# board2 = Board(set((Coord(1, 2), Coord(2, 2))), 
#                set((Coord(3, 4), Coord(4, 4))), 
#                PlayerColor.RED,
             
#                )

# print(hash(board1))
# print(hash(board2))
