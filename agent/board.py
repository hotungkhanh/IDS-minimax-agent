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
from copy import copy

import random

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
        self.turn_color: PlayerColor = initial_player

        self.turn_count = turn_count

    def __eq__(self, other: 'Board'):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash((frozenset(self.red_cells), frozenset(self.blue_cells), self.turn_color))

    def __copy__(self) -> 'Board':
        return Board(self.red_cells.copy(), self.blue_cells.copy(), self.turn_color, self.last_piece, self.turn_count)
    
    def __lt__(self, other: 'Board'):
        return self.__hash__() < other.__hash__()
    # @property
    # def hashable_value(self):
    #     return (frozenset(self.red_cells), frozenset(self.blue_cells), self.turn_color)

    def apply_action(self, action: Action):
        # used to return BoardMutation
        """
        Apply an action to a board, mutating the board state. 
        Action should be guaranteed to be legal
        """
        
        # add action to board 
        if self.turn_color == PlayerColor.RED:
            for cell in action.coords:
                self.red_cells.add(cell)
        else:
            for cell in action.coords:
                self.blue_cells.add(cell)

        self.last_piece = action
        self.line_removal()
        
        self.turn_color = self.turn_color.opponent

        self.turn_count += 1

        return

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
            # blue_candidate = list(cell for cell in self.blue_cells if cell.r == r)
            # red_candidate = list(cell for cell in self.red_cells if cell.r == r)
            blue_candidate = sum(1 for cell in self.blue_cells if cell.r == r)
            red_candidate = sum(1 for cell in self.red_cells if cell.r == r)

            # if the row is not filled 
            if blue_candidate + red_candidate != BOARD_N:
                continue
            
            # print("row filled:", r)
            
            # otherwise if the row is filled
            to_remove.update([Coord(r, x) for x in range(BOARD_N)])

        # check and remove columns
        for c in check_col:
            # find entries in that col across the 2 player sets
            blue_candidate = sum(1 for cell in self.blue_cells if cell.c == c)
            red_candidate = sum(1 for cell in self.red_cells if cell.c == c)

            # if the col is not filled 
            if blue_candidate + red_candidate != BOARD_N:
                continue

            # otherwise if the col is filled
            to_remove.update([Coord(x, c) for x in range(BOARD_N)])

        self.blue_cells = self.blue_cells.difference(to_remove)
        self.red_cells = self.red_cells.difference(to_remove)

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
    
    def generate_all_children(self) -> set['Board']:
        '''
        Returns a set of valid moves that can be made 
        '''
        children = set()

        if self.turn_color == PlayerColor.RED:
            my_cells = self.red_cells
            opponent_cells = self.blue_cells
        else:
            my_cells = self.blue_cells
            opponent_cells = self.red_cells

        # for the very first move, placing any piece anywhere has same effect
        # due to toroidal board
        if self.turn_count == 0:            
            for piece_type in PieceType:
                piece_coords = set(create_piece(piece_type, Coord(0,0)).coords)

                action = (PlaceAction(*piece_coords))
                child = Board(self.red_cells.copy(), self.blue_cells.copy(), self.turn_color, action, self.turn_count)
                child.apply_action(action)
                children.add(child)

            return children
        
        # for the second move, 
        elif self.turn_count == 1:

            empty_coords = [
                Coord(r, c)
                for r in range(BOARD_N)
                for c in range(BOARD_N)
                if (Coord(r, c) not in opponent_cells)
            ]

            piece_found = False
            while not piece_found:
                random_coord: Coord = random.choice(empty_coords)
                random_piece_type: PieceType = random.choice(list(PieceType))
                new_piece = set(create_piece(random_piece_type, random_coord).coords)
                for coord in new_piece:
                    if coord not in empty_coords:
                        continue
                piece_found = True

                action = (PlaceAction(*new_piece))
                child = Board(self.red_cells.copy(), self.blue_cells.copy(), self.turn_color, action, self.turn_count)
                child.apply_action(action)
                children.add(child)

            # children should only have 1 child in it - reduces unnecessary computation time at start
            return children

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

                    child = Board(self.red_cells.copy(), self.blue_cells.copy(), self.turn_color, action, self.turn_count)
                    child.apply_action(action)
                    children.add(child)
            return children
        
    # def adjacent_empty():


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
        
        if self.turn_count in (0,1):
            return False
        
        if self.turn_color == PlayerColor.RED:
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
            return self.turn_color.opponent

    @property
    def turn_limit_reached(self) -> bool:
        """
        True iff the maximum number of turns has been reached.
        """
        return self.turn_count >= MAX_TURNS
