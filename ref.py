from referee.game import PlayerColor, Action, PlaceAction, coord
from monte.board import Board
from monte.tree import TreeNode
import random
import math
import copy
from datetime import datetime, timedelta
import time

# contestants
from agent.program import Agent as minimax
from monte.program import Agent as monte
from randy.program import Agent as randy

import cProfile
import pstats
import io
from pstats import SortKey

MAX_TURNS = 150
BOARD_N = 11


def play():
    start_time = time.time()
    agent1 = minimax(PlayerColor.RED)
    agent2 = randy(PlayerColor.BLUE)
    players = {
        PlayerColor.RED: agent1,
        PlayerColor.BLUE: agent2
    }
    game_board = Board()

    prof = cProfile.Profile()
    prof.enable()

    while game_board.turn_count < MAX_TURNS:
        print()
        print(game_board.turn_color, "playing turn", game_board.turn_count + 1)

        try:
            action: Action = players[game_board.turn_color].action()

            game_board.apply_action(action)
            print("game board turn colour:", game_board.turn_color)
            print(game_board.render())
            print("RED and BLUE board after applying action")
            agent1.board.apply_action(action)
            print(agent1.board.render())
            agent2.board.apply_action(action)
            print(agent2.board.render())
        except:
            print("total runtime:", time.time() - start_time)
            print("something bad happened :( OR game is over)")
            print("player 1 board:")
            print(agent1.board.render())
            print("player 2 board:")
            print(agent2.board.render())
            break

    prof.disable()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(prof).sort_stats(sortby)
    ps.dump_stats("out.prof")
    ps.print_stats()

    print("GAME OVER")


# cProfile.run('play()', filename="out.prof")
play()
