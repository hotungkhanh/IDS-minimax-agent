# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game.coord import Coord
from referee.game.player import PlayerColor
from referee.game.actions import Action, PlaceAction
from referee.game.constants import *
from referee.game.pieces import *

import random

PIECE_N = 4


class Board:
    """
    A class representing a game board i.e. game state. 

    """

    def __init__(
        self,
        red_cells: set[Coord] = set(),
        blue_cells: set[Coord] = set(),
        initial_player: PlayerColor = PlayerColor.RED,

        turn_count=0,
    ):
        """
        Create a new board. It is optionally possible to specify an initial
        board state (in practice this is only used for testing).
        """
        self.red_cells = red_cells
        self.blue_cells = blue_cells

        # Colour of the player that will play next
        self.turn_color: PlayerColor = initial_player

        # Number of turns that have been played,
        # which is 1 less than the turn number
        self.turn_count = turn_count

    def __eq__(self, other: 'Board'):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash((frozenset(self.red_cells), frozenset(self.blue_cells), self.turn_color))

    def __copy__(self) -> 'Board':
        return Board(self.red_cells.copy(), self.blue_cells.copy(), self.turn_color, self.turn_count)

    def __lt__(self, other: 'Board'):
        return self.__hash__() < other.__hash__()

    def apply_action(self, action: Action):
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

        self.line_removal(action)

        self.turn_color = self.turn_color.opponent
        self.turn_count += 1

        return

    def line_removal(self, action):
        """
        Checks if any rows or columns should be removed on the board
        with the line-removal mechanic
        """

        to_remove = set()

        check_row = set()
        check_col = set()

        if action == None:
            return

        for cell in action.coords:
            check_row.add(cell.r)
            check_col.add(cell.c)

        # check and remove rows
        for r in check_row:
            # find entries in the row across the 2 player sets
            blue_candidate = sum(1 for cell in self.blue_cells if cell.r == r)
            red_candidate = sum(1 for cell in self.red_cells if cell.r == r)

            # if the row is not filled
            if blue_candidate + red_candidate != BOARD_N:
                continue

            # otherwise if the row is filled
            to_remove.update([Coord(r, x) for x in range(BOARD_N)])

        # check and remove columns
        for c in check_col:
            # find entries in the col across the 2 player sets
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
        Computes the 4 possible adjacent Coords from the given Coord

        Returns a list of coordinates.
        """

        return [coord.down(), coord.up(), coord.left(), coord.right()]

    def generate_piece_combinations(self, touched_coord) -> set[list[Coord]]:
        """
        Generate all possible piece combinations touching a given coordinate.

        Returns a set of a list of coordinates, each list represents the
        coordinates in a PlaceAction.
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
                            stack.append(
                                (coord, current_piece + [adjacent_coord]))

        return piece_combinations

    def generate_all_moves(self) -> set[PlaceAction]:
        """
        Generate all possible moves for the current board.

        Returns a set of PlaceAction representing valid moves that can be made.
        """

        moves = set()

        if self.turn_color == PlayerColor.RED:
            my_cells = self.red_cells
            opponent_cells = self.blue_cells
        else:
            my_cells = self.blue_cells
            opponent_cells = self.red_cells

        # First red move
        if self.turn_count == 0:
            for piece_type in PieceType:
                piece_coords = set(create_piece(
                    piece_type, Coord(0, 0)).coords)

                action = (PlaceAction(*piece_coords))
                moves.add(action)

            return moves

        # First blue move
        elif self.turn_count == 1:
            opponent_adj = []
            for my_cell in opponent_cells:
                opponent_adj += self.adjacent(my_cell)

            empty_coords = [
                Coord(r, c)
                for r in range(BOARD_N)
                for c in range(BOARD_N)
                if (Coord(r, c) not in opponent_cells) and (Coord(r, c) not in opponent_adj)
            ]

            piece_found = False
            while not piece_found:
                random_coord: Coord = random.choice(empty_coords)
                random_piece_type: PieceType = random.choice(list(PieceType))
                new_piece = set(create_piece(
                    random_piece_type, random_coord).coords)

                invalid_coords = sum(
                    1 for c in new_piece if c not in empty_coords)
                if invalid_coords > 0:
                    continue
                else:
                    piece_found = True

            action = (PlaceAction(*new_piece))
            moves.add(action)

            return moves

        # Turn 3 onwards
        else:
            for my_cell in my_cells:
                piece_combinations = self.generate_piece_combinations(my_cell)

                for piece in piece_combinations:
                    c1, c2, c3, c4 = piece
                    action = PlaceAction(c1, c2, c3, c4)

                    moves.add(action)
            return moves

    def render(self, use_color: bool = False, use_unicode: bool = False) -> str:
        """
        Desgined to pretty-print a board.

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

        if self.turn_count in [0, 1]:
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
            red_count = len(self.red_cells)
            blue_count = len(self.blue_cells)
            balance = red_count - blue_count

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
