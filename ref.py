from referee.game import PlayerColor, Action, PlaceAction, coord
from monte.board import Board
from monte.tree import TreeNode
import random, math, copy
from datetime import datetime, timedelta
from monte.program import Agent

from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator

MAX_TURNS = 150
BOARD_N = 11

def play():
    agent1 = Agent(PlayerColor.RED)
    agent2 = Agent(PlayerColor.BLUE)
    players = {
        PlayerColor.RED: agent1,
        PlayerColor.BLUE: agent2
    }
    game_board = Board()
    
    while game_board.turn_count < MAX_TURNS:
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
        
        game_board.turn_count += 1

    print("GAME OVER")
    
play()