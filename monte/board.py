# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

# Copied from referee Board class

from dataclasses import dataclass

from referee.game.coord import Coord, Direction
from referee.game.player import PlayerColor
from referee.game.actions import Action, PlaceAction
from referee.game.exceptions import IllegalActionException
from referee.game.constants import *
from referee.game.pieces import *

PIECE_N = 4

class Board:

    def __init__(
        self, 
        red_cells: set[Coord] = set(),
        blue_cells: set[Coord] = set(),
        initial_player: PlayerColor = PlayerColor.RED,
        
        piece: PlaceAction = None,
        turn_count = 0,
    ):
        """
        Create a new board. It is optionally possible to specify an initial
        board state (in practice this is only used for testing).
        """
        self.red_cells = red_cells
        self.blue_cells = blue_cells

        self.last_piece = piece
        self._turn_color: PlayerColor = initial_player

        self.turn_count = turn_count

    def __eq__(self, other: 'Board'):
        return self.hashable_value == other.hashable_value

    def __hash__(self):
        return hash(self.hashable_value)

    @property
    def hashable_value(self):
        return (frozenset(self.red_cells), frozenset(self.blue_cells))

    def apply_action(self, action: Action):
        # used to return BoardMutation
        """
        Apply an action to a board, mutating the board state. 
        Action should be guaranteed to be legal
        """
        
        # add action to board 
        if self._turn_color == PlayerColor.RED:
            for cell in action.coords:
                self.red_cells.add(cell)
        else:
            for cell in action.coords:
                self.blue_cells.add(cell)

        # TODO: perform line removal if required (new function)
        self.last_piece = action
        self.line_removal()
        
        self._turn_color = self._turn_color.opponent

        self.turn_count += 1

        return

    # def check_legal_move(self, action: Action) -> bool:
    #     '''
    #     Checks if a move can be legally placed on board
    #     Does not mofify board 
    #     Throws an IllegalActionException if the action is invalid.
    #     '''
    #     for coord in action.coords:
    #         if len(self.empty_neighbours(coord)) == 0:

    #     return True
    #     # TODO


    def line_removal(self):
        '''
        Checks if any rows or columns should be removed on the board

        Done, not tested
        '''
        to_remove = set()
        # use last_piece to determine which rows & cols to check for 
        # line removal (reduces search space)
        check_row = set()
        check_col = set()

        if self.last_piece == None:
            return
            
        for cell in self.last_piece.coords:
            check_row.add(cell.r)
            check_col.add(cell.c)

        # check and remove rows
        for r in check_row:
            # find entries in that row across the 2 player sets
            blue_candidate = list(cell for cell in self.blue_cells if cell.r == r)
            red_candidate = list(cell for cell in self.red_cells if cell.r == r)

            # if the row is not filled 
            if (len(blue_candidate) + len(red_candidate)) != BOARD_N:
                continue
            
            # print("row filled:", r)
            
            # otherwise if the row is filled
            # print("Before: ")
            # print(self.render())
            for candidate in blue_candidate:
                to_remove.add(candidate)
                # self.blue_cells.remove(candidate)
            for candidate in red_candidate:
                to_remove.add(candidate)
                # self.red_cells.remove(candidate)
            # print("After:")
            # print(self.render())

        # check and remove columns
        for c in check_col:
            # find entries in that col across the 2 player sets
            blue_candidate = list(cell for cell in self.blue_cells if cell.c == c)
            red_candidate = list(cell for cell in self.red_cells if cell.c == c)

            # if the col is not filled 
            if (len(blue_candidate) + len(red_candidate)) != BOARD_N:
                continue

            # print("col filled:", c)
            # print("Before: ")
            # print(self.render())
            # otherwise if the col is filled
            for candidate in blue_candidate:
                to_remove.add(candidate)
            for candidate in red_candidate:
                to_remove.add(candidate)
            # print("After:")
            # print(self.render())
        
        for item in to_remove:
            self.blue_cells.discard(item)
            self.red_cells.discard(item)

    def adjacent(self, coord: Coord):
        """
        Computes all 4 possible adjacent coordinates

        Parameters:
            `coord`: a `Coord` instance that represents the coordinate that we want
            to find adjacent coordinates for

        Returns:
            An array of adjacent coordinates on the board
        """

        return [coord.down(), coord.up(), coord.left(), coord.right()]

    def generate_piece_combinations(self, touched_coord) -> list:
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
                for adjacent_coord in self.adjacent(current_coord):
                    # check if adj coord is empty and not already in curr piece
                    if ((adjacent_coord not in self.red_cells) and (adjacent_coord not in self.blue_cells) and
                        (adjacent_coord not in current_piece)):
                        stack.append((adjacent_coord, current_piece + 
                                        [adjacent_coord]))
                        for coord in current_piece:
                            stack.append((coord, current_piece + [adjacent_coord]))

        return piece_combinations
    
    def generate_all_moves(self) -> PlaceAction:
        '''
        Returns a list of boards with new valid moves that can be made 
        '''
        moves = set()          # needs to be a list of states here 
        # no piece of player colour on board
        # FOR TESTING PURPOSES: remove randomness of first step

        if self._turn_color == PlayerColor.RED:
            my_cells = self.red_cells
        else:
            my_cells = self.blue_cells

        if self.turn_count == 0:            
            for piece_type in PieceType:
                piece_coords = set(create_piece(piece_type, Coord(0,0)).coords)

                action = (PlaceAction(*piece_coords))
                moves.add(action)

            return moves
        
        elif self.turn_count == 1:
            if self._turn_color == PlayerColor.RED:
                opponent_cells = self.blue_cells
            else:
                opponent_cells = self.red_cells
            
            empty_coords = [
                Coord(r, c)
                for r in range(BOARD_N)
                for c in range(BOARD_N)
                if ((Coord(r, c) not in self.red_cells) and (Coord(r, c) not in self.blue_cells))
            ]

            
            stack = []
            for r in range(BOARD_N):
                for c in range(BOARD_N):
                    current_coord = Coord(r,c)
                    stack.append((current_coord, [current_coord]))

            while stack:
                current_coord, current_piece = stack.pop()
                if len(current_piece) == 4:
                    c1, c2, c3, c4 = current_piece
                    action = PlaceAction(c1, c2, c3, c4)
                    moves.add(action)
                else:
                    for adjacent_coord in self.adjacent(current_coord):
                        # check if adj coord is empty and not already in curr piece
                        if (adjacent_coord not in opponent_cells):
                            stack.append((adjacent_coord, current_piece + 
                                            [adjacent_coord]))
                            for coord in current_piece:
                                stack.append((coord, current_piece + [adjacent_coord]))

            return moves

        
        # board has 1+ piece of player colour
        # FOR TESTING PURPOSES: reduce randomness
        else:
            for cell in my_cells:
                # if cell does not have empty neighbours
                #   continue

                piece_combinations = self.generate_piece_combinations(cell)

                # code for all pieces
                for piece in piece_combinations:
                    c1, c2, c3, c4 = piece
                    action = PlaceAction(c1, c2, c3, c4)

                    # place piece on board
                    # new_board = Board(board.red_cells.copy(), board.blue_cells.copy(), board._turn_color, action, board.turn_count)
                    # new_board.apply_action(action)
                    moves.add(action)
            return moves

    def render(self, use_color: bool=False, use_unicode: bool=False) -> str:
        """
        Returns a visualisation of the game board as a multiline string, with
        optional ANSI color codes and Unicode characters (if applicable).
        """
        def apply_ansi(str, bold=True, color=None):
            bold_code = "\033[1m" if bold else ""
            color_code = ""
            if color == "r":
                color_code = "\033[31m"
            if color == "b":
                color_code = "\033[34m"
            return f"{bold_code}{color_code}{str}\033[0m"

        output = ""
        for r in range(BOARD_N):
            for c in range(BOARD_N):
                if (Coord(r, c) in self.red_cells):
                    color = "r"
                    text = f"{color}"
                    if use_color:
                        output += apply_ansi(text, color=color, bold=False)
                    else:
                        output += text
                elif (Coord(r, c) in self.blue_cells):
                    color = "b"
                    text = f"{color}"
                    if use_color:
                        output += apply_ansi(text, color=color, bold=False)
                    else:
                        output += text
                else:
                    output += "."
                output += " "
            output += "\n"
        return output
    
    @property
    def game_over(self) -> bool:
        """
        True iff the game is over.
        """
        
        if self.turn_limit_reached:
            return True
        

        if self._turn_color == PlayerColor.RED:
            my_cells = self.red_cells
        else:
            my_cells = self.blue_cells

        for cell in my_cells:
            piece_combinations = self.generate_piece_combinations(cell)
            
            if len(piece_combinations) > 0:
                return False

        # Tried all possible moves and none were legal.
        return True
    
    @property
    def winner_color(self) -> PlayerColor | None:
        """
        The player (color) who won the game, or None if no player has won.
        """
        if not self.game_over:
            return None
        
        if self.turn_limit_reached:
            # In this case the player with the most tokens wins, or if equal,
            # the game ends in a draw.
            red_count  = len(self.red_cells)
            blue_count = len(self.blue_cells)
            balance    = red_count - blue_count

            if balance == 0:
                return None
            
            return PlayerColor.RED if balance > 0 else PlayerColor.BLUE

        else:
            # Current player cannot place any more pieces. Opponent wins.
            return self._turn_color.opponent

    @property
    def turn_limit_reached(self) -> bool:
        """
        True iff the maximum number of turns has been reached.
        """
        return self.turn_count >= MAX_TURNS
