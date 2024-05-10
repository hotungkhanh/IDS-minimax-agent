# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, coord
from referee.game.pieces import *
from .part_a.utils import render_board
from .board import Board
from referee.game.exceptions import IllegalActionException
import random, math, copy
import time

CUT_OFF = 30

class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """
        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")
        
        # initialise internal rep of board
        self.board: Board = Board()
        self.children_dict: dict[int, set[Board]] = {}
        self.boards_dict: dict[int, float] = {}

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """

        if self.board.turn_count == 0:
            action = PlaceAction(
                    Coord(3, 3), 
                    Coord(3, 4), 
                    Coord(4, 3), 
                    Coord(4, 4)
                )
        elif self.board.turn_count < 10:
            eval, child = self.minimax_ab(self.board, 1, -(math.inf), math.inf, self._color)
            action = child.last_piece

        elif self.board.turn_count < CUT_OFF:
            eval, child = self.minimax_ab(self.board, 2, -(math.inf), math.inf, self._color)
            action = child.last_piece

        else:
            eval, child = self.minimax_ab(self.board, 3, -(math.inf), math.inf, self._color)
            action = child.last_piece

        match self._color:
            case PlayerColor.RED:
                print("Testing: RED is playing a PLACE action")
                return action
                
            case PlayerColor.BLUE:
                print("Testing: BLUE is playing a PLACE action")
                return action

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state. 
        """
        
        # There is only one action type, PlaceAction
        place_action: PlaceAction = action
        c1, c2, c3, c4 = place_action.coords

        self.board.apply_action(place_action)

        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")

    def minimax_ab(self, board: Board, depth: int, alpha, beta, colour: PlayerColor) -> tuple[int, Board]:

        if depth == 0 or board.game_over:
            return (eval(board), None)
        
        if colour == PlayerColor.RED:
            best_child = None
            maxEval = -(math.inf)

            # print(board.render())
            # print("hash(board) =", hash(board))

            # TODO: make into helper function
            # check if board has been generated in previous turns 
            # if hash(board) in self.children_dict:
            #     print("children = self.children_dict[board]")
            #     children = self.children_dict[hash(board)]
            #     # dictcount += 1

            #     for child in children:
            #         print("child:")
            #         print(child.render())
            #         break
            # else:
            #     # print("children = board.generate_all_children()")
            #     children = board.generate_all_children()
                
            #     self.children_dict[hash(board)] = children
            
            # TODO: make into helper function

            valid_moves = board.generate_all_moves()

            # ordered_children = []
            # for child in children:
            #     if hash(child) in self.boards_dict:
            #         # print("board is in board_dict")
            #         ordered_children.append((self.boards_dict[hash(child)], child))
            #     else:
            #         # print("shouldn't happen for depth = 2")
            #         ordered_children.append((0, child))
            # # sort children based on their eval from PREVIOUS turn's eval of them
            # ordered_children.sort(key=lambda x: x[0], reverse=True)

            # for prev_eval, child in ordered_children:
            for move in valid_moves:

                child = board.__copy__()
                child.apply_action(move)

                val, minimax_board = self.minimax_ab(child, depth - 1, alpha, beta, PlayerColor.BLUE)

                if val >= maxEval:
                    maxEval = val
                    best_child = child
                alpha = max(alpha, val)
                if beta <= alpha:
                    break

            return (maxEval, best_child)
        
        else:
            best_child = None
            minEval = math.inf

            # print(board.render())
            # print("hash(board) =", hash(board))
            # if hash(board) in self.children_dict:
            #     print("children = self.children_dict[board]")
            #     children = self.children_dict[hash(board)]
            #     # dictcount += 1

            #     for child in children:
            #         print("child:")
            #         print(child.render())
            #         break
            # else:
            #     # print("children = board.generate_all_children()")
            #     children = board.generate_all_children()
                
            #     self.children_dict[hash(board)] = children

            valid_moves = board.generate_all_moves()


            # ordered_children = []
            # for child in children:
            #     if hash(child) in self.boards_dict.keys():
            #         # print("board is in board dict")
            #         ordered_children.append((self.boards_dict[hash(child)], child))
            #     else:
            #         ordered_children.append((0, child))
            # # sort children based on their eval from PREVIOUS turn's eval of them
            # ordered_children.sort(key=lambda x: x[0])

            # for prev_eval, child in ordered_children:
            for move in valid_moves:

                child = board.__copy__()
                child.apply_action(move)

                val, minimax_board = self.minimax_ab(child, depth - 1, alpha, beta, PlayerColor.RED)

                if val <= minEval:
                    minEval = val
                    best_child = child
                beta = min(beta, val)
                if beta <= alpha:
                    break

            return (minEval, best_child)


def eval(board: Board):
    if board.winner_color == PlayerColor.RED:
        return math.inf
    if board.winner_color == PlayerColor.BLUE:
        return -math.inf

    # print("evaling")
    blue_count = len(board.blue_cells)
    red_count = len(board.red_cells)

    bad_red_lines = 0
    bad_blue_lines = 0
    for r in range(BOARD_N):
        red = sum(1 for cell in board.red_cells if cell.r == r)
        blue = sum(1 for cell in board.blue_cells if cell.r == r)
        if red >= 6:
            bad_red_lines += 1
        if blue >= 6:
            bad_blue_lines += 1
    
    for c in range(BOARD_N):
        red = sum(1 for cell in board.red_cells if cell.c == c)
        blue = sum(1 for cell in board.blue_cells if cell.c == c)
        if red >= 6:
            bad_red_lines += 1
        if blue >= 6:
            bad_blue_lines += 1

    return red_count - blue_count - bad_red_lines + bad_blue_lines