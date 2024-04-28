# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, Coord, Board
from referee.game.pieces import *
from .part_a.utils import render_board
from .helpers import test

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
        match self._color:
            case PlayerColor.RED:
                print("Testing: RED is playing a PLACE action")
                return PlaceAction(
                    Coord(3, 3), 
                    Coord(3, 4), 
                    Coord(4, 3), 
                    Coord(4, 4)
                )
            case PlayerColor.BLUE:
                print("Testing: BLUE is playing a PLACE action")
                return PlaceAction(
                    Coord(2, 3), 
                    Coord(2, 4), 
                    Coord(2, 5), 
                    Coord(2, 6)
                )

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state. 
        """
        
        # There is only one action type, PlaceAction
        place_action: PlaceAction = action
        c1, c2, c3, c4 = place_action.coords

        self.board.apply_action(place_action)
            
        print(self.board.render())
        output = ""
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

        self.generate_moves()

        # Here we are just printing out the PlaceAction coordinates for
        # demonstration purposes. You should replace this with your own logic
        # to update your agent's internal game state representation.
        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")

    def generate_moves(self):
        for cell, colour in self.board._state.items():
            if colour == self._color:
                for newcell in adjacent(cell):
                    for piece in PieceType:
                        pie = create_piece(piece, newcell)
                        print(pie.coords)
                        try:
                            action = PlaceAction(** pie.coords)
                            self.board.apply_action(action)
                            print(self.board.render())
                        except:
                            continue
    
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

