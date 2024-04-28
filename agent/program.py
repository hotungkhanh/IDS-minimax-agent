# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, coord
from referee.game.pieces import *
from .part_a.utils import render_board
from .helpers import test
from .board import Board
from referee.game.exceptions import IllegalActionException

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
        action = self.generate_moves()

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
            
        # print(self.board.render())
        # output = ""
        # for r in range(11):
        #     for c in range(11):
        #         if self.board.get(Coord(r, c), None):
        #             color = self.board[Coord(r, c)]
        #             color = "r" if color == PlayerColor.RED else "b"
        #             text = f"{color}"
        #             output += text
        #         else:
        #             output += "."
        #         output += " "
        #     output += "\n"
        # print(output)

        

        # Here we are just printing out the PlaceAction coordinates for
        # demonstration purposes. You should replace this with your own logic
        # to update your agent's internal game state representation.
        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")

    def generate_moves(self):
        if self.board._player_token_count(self._color) == 0:
            empty_coords = set(filter(self.board._cell_empty, self.board._state.keys()))
            for piece_type in PieceType: 
                for coord in empty_coords:
                    try:
                        piece_coords = set(create_piece(piece_type, coord).coords)

                        self.board.apply_action(PlaceAction(*piece_coords))
                        self.board.undo_action()

                        return PlaceAction(*piece_coords)
                    
                    except (ValueError, IllegalActionException):
                        pass
        for cell, colour in self.board._state.items():
            if colour.player == None:
                continue
            if colour.player == self._color:
                print(cell)
                piece_combinations = self.generate_piece_combinations(cell)
                if cell == Coord(4, 3):
                    print(piece_combinations)
                for piece in piece_combinations:
                    print(piece)
                    try:
                        c1, c2, c3, c4 = piece
                        action = PlaceAction(c1, c2, c3, c4)
                        print(action)
                        self.board.apply_action(action)
                        self.board.undo_action()
                        print(self.board.render())
                        return action
                    except:
                        print("error")
                        continue
    
    def generate_piece_combinations(self, touched_coord) -> list:
        """
        Generate all possible piece combinations touching a given coordinate.
        """

        piece_combinations = set()
        stack = [(touched_coord, [])]

        while stack:
            current_coord, current_piece = stack.pop()
            if len(current_piece) == PIECE_N:
                # if touched_coord == Coord(4, 3):
                #     print(current_piece)
                piece_combinations.add(tuple(sorted(current_piece)))
            else:
                for adjacent_coord in adjacent(current_coord):
                    # check if adj coord is empty and not already in curr piece
                    if ((self.board._state[adjacent_coord].player == None) and 
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

