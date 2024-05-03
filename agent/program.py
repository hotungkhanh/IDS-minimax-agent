# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, coord
from referee.game.pieces import *
from .part_a.utils import render_board
from .helpers import test
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
        # print("done")
        eval, child = minimax(self.board, 2, self._color)
        print(hash(child))
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

    
def generate_moves(board: Board, color: PlayerColor):
    '''
    Returns a list of boards with new valid moves that can be made 
    '''
    moves = set()          # needs to be a list of states here 
    # no piece of player colour on board
    # FOR TESTING PURPOSES: remove randomness of first step

    if color == PlayerColor.RED:
        my_cells = board.red_cells
    else:
        my_cells = board.blue_cells

    if len(my_cells) == 0:
        if len(board.red_cells) == 0 and len(board.blue_cells) == 0:            
            action = PlaceAction(
                    Coord(3, 3), 
                    Coord(3, 4), 
                    Coord(4, 3), 
                    Coord(4, 4)
                )

            # place piece on board
            new_board = Board(board.red_cells.copy(), board.blue_cells.copy(), board._turn_color, action, board.turn_count)
            new_board.apply_action(action)
            moves.add(new_board)
            return moves
        
        empty_coords = [
            Coord(r, c)
            for r in range(BOARD_N)
            for c in range(BOARD_N)
            if ((Coord(r, c) not in board.red_cells) or (Coord(r, c) not in board.blue_cells))
        ]
        for cell in empty_coords:
            piece_combinations = board.generate_piece_combinations(cell)

            # code for random piece 
            # for piece in piece_combinations:
            #     c1, c2, c3, c4 = piece
            #     action = PlaceAction(c1, c2, c3, c4)
            #     board.apply_action(action)
            #     new_board = copy.deepcopy(board)
            #     board.undo_action()
            #     moves.append(new_board)

            # code for less random piece
            for i in range(20):
                if len(piece_combinations) == 0:
                    # print('ooops')
                    break
                piece = random.choice(list(piece_combinations))
                piece_combinations.remove(piece)
                c1, c2, c3, c4 = piece
                action = PlaceAction(c1, c2, c3, c4)

                # place piece on board
                new_board = Board(board.red_cells.copy(), board.blue_cells.copy(), board._turn_color, action, board.turn_count)
                new_board.apply_action(action)
                moves.add(new_board)

        return moves
    
    # board has 1+ piece of player colour
    # FOR TESTING PURPOSES: reduce randomness
    else:
        for cell in my_cells:
            # if cell does not have empty neighbours
            #   continue

            piece_combinations = board.generate_piece_combinations(cell)

            # code for less random piece
            for i in range(20):
                if len(piece_combinations) == 0:
                    # print('ooops')
                    break
                piece = random.choice(list(piece_combinations))
                piece_combinations.remove(piece)
                c1, c2, c3, c4 = piece
                action = PlaceAction(c1, c2, c3, c4)

                # place piece on board
                new_board = Board(board.red_cells.copy(), board.blue_cells.copy(), board._turn_color, action, board.turn_count)
                new_board.apply_action(action)
                moves.add(new_board)
        return moves

def empty_neighbours(board: Board, coord: Coord) -> list[Coord]:
    neighbours = [coord.down(), coord.up(), coord.left(), coord.right()]
    output = []
    for neighbour in neighbours:
        if (neighbour not in board.blue_cells) and (neighbour not in board.red_cells):
            output.append(neighbour)
    
    return output


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
        return (eval(board), board)
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
    blue_count = len(board.blue_cells)
    red_count = len(board.red_cells)
    return red_count - blue_count