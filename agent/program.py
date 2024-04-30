# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, coord
from referee.game.pieces import *
from .part_a.utils import render_board
from .helpers import test
from .board import Board
from referee.game.exceptions import IllegalActionException
import random, math, copy

PIECE_N = 4

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

        # Below we have hardcoded two actions to be played depending on whether
        # the agent is playing as BLUE or RED. Obviously this won't work beyond
        # the initial moves of the game, so you should use some game playing
        # technique(s) to determine the best action to take.
        eval, child = minimax(self.board, 2, self._color)
        action = child._history[-1].action

        # RUN MINIMAX HERE

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

    
def generate_moves(board: Board, color: PlayerColor):
    '''
    Returns a list of boards with new valid moves that can be made 
    '''
    moves = []          # needs to be a list of states here 
    # no piece of player colour on board
    # FOR TESTING PURPOSES: remove randomness of first step 
    if board._player_token_count(color) == 0:
        empty_coords = set(filter(board._cell_empty, board._state.keys()))
        for i in range(5):
            coord = random.choice(list(empty_coords))
            for piece_type in PieceType: 
                try:
                    piece_coords = set(create_piece(piece_type, coord).coords)
                    
                    board.apply_action(PlaceAction(*piece_coords))
                    new_board = copy.deepcopy(board)
                    board.undo_action()

                    moves.append(new_board)
                
                except (ValueError, IllegalActionException):
                    pass
        return moves
    
    # board has 1+ piece of player colour
    # FOR TESTING PURPOSES: remove randomness
    for cell, colour in board._state.items():
        if colour.player == None:
            continue
        if colour.player == color:
            piece_combinations = generate_piece_combinations(board, cell)

            # for random piece 
            # for piece in piece_combinations:
            #     c1, c2, c3, c4 = piece
            #     action = PlaceAction(c1, c2, c3, c4)
            #     board.apply_action(action)
            #     new_board = copy.deepcopy(board)
            #     board.undo_action()
            #     moves.append(new_board)

            # for less random piece
            for i in range(20):
                if len(piece_combinations) == 0:
                    # print('ooops')
                    break
                piece = random.choice(list(piece_combinations))
                piece_combinations.remove(piece)
                c1, c2, c3, c4 = piece
                action = PlaceAction(c1, c2, c3, c4)
                board.apply_action(action)
                new_board = copy.deepcopy(board)
                board.undo_action()
                moves.append(new_board)
    return moves


def generate_piece_combinations(board: Board, touched_coord) -> list:
    """
    Generate all possible piece combinations touching a given coordinate.
    """

    piece_combinations = set()
    stack = [(touched_coord, [])]

    while stack:
        current_coord, current_piece = stack.pop()
        if len(current_piece) == PIECE_N:
            piece_combinations.add(tuple(sorted(current_piece)))
        else:
            for adjacent_coord in adjacent(current_coord):
                # check if adj coord is empty and not already in curr piece
                if ((board._state[adjacent_coord].player == None) and 
                    (adjacent_coord not in current_piece)):
                    stack.append((adjacent_coord, current_piece + 
                                    [adjacent_coord]))
                    for coord in current_piece:
                        stack.append((coord, current_piece + [adjacent_coord]))

    return piece_combinations

def adjacent(
    coord: Coord
):
    """
    Computes all 4 possible adjacent coordinates

    Parameters:
        `coord`: a `Coord` instance that represents the coordinate that we want
        to find adjacent coordinates for

    Returns:
        An array of adjacent coordinates on the board
    """

    return [coord.down(), coord.up(), coord.left(), coord.right()]


def minimax(board: Board, depth: int, color: PlayerColor) -> tuple[int, Board]:
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
            minEval = min(minEval, eval)
        return minEval
    '''  

    if depth == 0 or board.game_over:
        return (eval(board), None)
    if color == PlayerColor.RED:
        best_child = None
        maxEval = -(math.inf)
        children = generate_moves(board, color)
        for child in children:
            val = minimax(child, depth - 1, PlayerColor.BLUE)
            if val[0] > maxEval:
                maxEval = val[0]
                best_child = child
        return (maxEval, best_child)
    else:
        best_child = None
        minEval = math.inf
        children = generate_moves(board, color)
        for child in children:
            val = minimax(child, depth - 1, PlayerColor.RED)
            if val[0] < minEval:
                minEval = val[0]
                best_child = child
        return (minEval, best_child)


def eval(board: Board):
    blue_count = board._player_token_count(PlayerColor.BLUE)
    red_count = board._player_token_count(PlayerColor.RED)
    return red_count - blue_count