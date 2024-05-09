# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, coord
from referee.game.pieces import *
from .part_a.utils import render_board
from .board import Board
from referee.game.exceptions import IllegalActionException
import random, math, copy

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

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """
        # print("board in action()")
        # print(self.board.render(True, True))

        eval, child = minimax_ab(self.board, 2, -(math.inf), math.inf, self._color)
        # action should never be None
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

        # Here we are just printing out the PlaceAction coordinates for
        # demonstration purposes. You should replace this with your own logic
        # to update your agent's internal game state representation.
        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")


def empty_neighbours(board: Board, coord: Coord) -> list[Coord]:
    neighbours = [coord.down(), coord.up(), coord.left(), coord.right()]
    output = []
    for neighbour in neighbours:
        if (neighbour not in board.blue_cells) and (neighbour not in board.red_cells):
            output.append(neighbour)
    
    return output

def minimax_ab(board: Board, depth: int, alpha, beta, colour: PlayerColor) -> tuple[int, Board]:
    # print("in minimax")
    if depth == 0 or board.game_over:
        print(board.render())
        print("eval =", eval(board))
        return (eval(board), None)
    
    if colour == PlayerColor.RED:
        best_child = None
        maxEval = -(math.inf)

        children = board.generate_all_children()
        # print("all children generated")
        for child in children:
            val = minimax_ab(child, depth - 1, alpha, beta, PlayerColor.BLUE)
            # print("here:", val)
            if val[0] > maxEval:
                maxEval = val[0]
                best_child = child
            alpha = max(alpha, val[0])
            if beta <= alpha:
                break

        return (maxEval, best_child)
    
    else:
        best_child = None
        minEval = math.inf
        children = board.generate_all_children()

        for child in children:
            val = minimax_ab(child, depth - 1, alpha, beta, PlayerColor.RED)
            if val[0] < minEval:
                minEval = val[0]
                best_child = child
            beta = min(beta, val[0])
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

    red_score = 0
    blue_score = 0
    for r in range(BOARD_N):
        red = len([cell for cell in board.red_cells if cell.r == r])
        blue = len([cell for cell in board.blue_cells if cell.r == r])
        if red >= 6:
            red_score += 1
        if blue >= 6:
            blue_score += 1
    
    for c in range(BOARD_N):
        red = len([cell for cell in board.red_cells if cell.c == c])
        blue = len([cell for cell in board.blue_cells if cell.c == c])
        if red >= 6:
            red_score += 1
        if blue >= 6:
            blue_score += 1

    return red_count - blue_count + red_score - blue_score