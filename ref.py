from referee.game import PlayerColor, Action, PlaceAction, coord
from monte.board import Board
from monte.tree import TreeNode
import random, math, copy
from datetime import datetime, timedelta

# contestants
from monte.program import Agent as monte
from randy.program import Agent as randy

import cProfile, pstats, io
from pstats import SortKey

MAX_TURNS = 150
BOARD_N = 11

def play():
    agent1 = monte(PlayerColor.RED)
    agent2 = randy(PlayerColor.BLUE)
    players = {
        PlayerColor.RED: agent1,
        PlayerColor.BLUE: agent2
    }
    game_board = Board()

    prof = cProfile.Profile()
    prof.enable()
    
    while game_board.turn_count < MAX_TURNS - 140:
        print()
        print(game_board._turn_color, "playing turn", game_board.turn_count + 1)

        action = players[game_board._turn_color].action()

        try:
            game_board.apply_action(action)
            print(game_board.render())
            agent1.update(game_board._turn_color, action)
            agent2.update(game_board._turn_color, action)
        except:
            print("something bad happened :( OR game is over)")
            break

    prof.disable()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(prof).sort_stats(sortby)
    ps.dump_stats("out.prof")
    ps.print_stats()

    print("GAME OVER")
    
# cProfile.run('play()', filename="out.prof")
play()