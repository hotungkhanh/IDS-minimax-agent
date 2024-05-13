# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction
from referee.game.pieces import BOARD_N
from .board import Board
import math
import random
from datetime import datetime, timedelta

# Eval for a winning state, ensuring it is bigger
# than any eval calculated by formula, but smaller than inf
WINNING_SCORE = 999

# Avoid placing this many cells on one line if possible
BAD_LINE = 6

# If a board has this many possible moves, it is safe to
# call minimax at depth of only 1.
LARGE_BRANCH_FACTOR = 200

# The time limit given to decide a move using ID minimax
DECIDING_TIME = 0.5


class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
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

        valid_moves_dict: dict[int, set[PlaceAction]] = {}
        valid_moves_dict[hash(self.board)] = self.board.generate_all_moves()

        if self.board.turn_count in [0, 1]:
            action = random.choice(list(valid_moves_dict[hash(self.board)]))

        else:
            action = self.determine_move(valid_moves_dict)

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
        turn.
        """

        # There is only one action type, PlaceAction
        place_action: PlaceAction = action
        c1, c2, c3, c4 = place_action.coords

        self.board.apply_action(place_action)

        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")

    def minimax_ab(self, board: Board, depth: int, alpha, beta, valid_moves_dict) -> tuple[int, PlaceAction]:
        """
        Minimax algorithm with alpha-beta pruning on the given Board.

        Returns the best move to play accordingly with its eval.

        Code adapted from: https://www.youtube.com/watch?v=l-hh51ncgDI&t=2s
        """

        if depth == 0 or board.game_over:
            return (eval(board), None)

        if board.turn_color == PlayerColor.RED:
            best_move = None
            maxEval = -(math.inf)

            if hash(board) not in valid_moves_dict:
                valid_moves = board.generate_all_moves()
                valid_moves_dict[hash(board)] = valid_moves
            else:
                valid_moves = valid_moves_dict[hash(board)]

            for move in valid_moves:
                child = board.__copy__()
                child.apply_action(move)
                val = self.minimax_ab(
                    child, depth - 1, alpha, beta, valid_moves_dict)[0]

                if maxEval < val:
                    maxEval = val
                    best_move = move

                alpha = max(alpha, maxEval)
                if alpha >= beta:
                    break

            return (maxEval, best_move)

        else:
            best_move = None
            minEval = math.inf

            if hash(board) not in valid_moves_dict:
                valid_moves = board.generate_all_moves()
                valid_moves_dict[hash(board)] = valid_moves
            else:
                valid_moves = valid_moves_dict[hash(board)]

            for move in valid_moves:
                child = board.__copy__()
                child.apply_action(move)
                val = self.minimax_ab(
                    child, depth - 1, alpha, beta, valid_moves_dict)[0]

                if minEval > val:
                    minEval = val
                    best_move = move

                beta = min(beta, minEval)
                if beta <= alpha:
                    break

            return (minEval, best_move)

    def id_minimax(self, time: float, valid_moves_dict):
        """
        Caller function for iterative deepening minimax.        
        If it still within the time limit given for deciding a move,
        do minimax with one extra depth.

        Returns the best move to play accordingly.
        """

        depth = 1
        start_time = datetime.now()
        fin_time = start_time + timedelta(seconds=time)

        while datetime.now() < fin_time:
            value, action = self.minimax_ab(
                self.board, depth, -(math.inf), math.inf, valid_moves_dict)
            depth += 1

        return action

    def determine_move(self, valid_moves_dict):
        dict_len = len(valid_moves_dict[hash(self.board)])

        if dict_len > LARGE_BRANCH_FACTOR:
            move = self.minimax_ab(
                self.board, 1, -(math.inf), math.inf, valid_moves_dict)[1]
        else:
            time = DECIDING_TIME
            move = self.id_minimax(time, valid_moves_dict)
        return move


def eval(board: Board):
    """
    Evaluation function to decide the value of a board.

    Returns a heuristic value by formula for a non-terminal state and a 
    constant for a terminal state.
    """

    if board.winner_color == PlayerColor.RED:
        return WINNING_SCORE
    if board.winner_color == PlayerColor.BLUE:
        return -WINNING_SCORE

    blue_count = len(board.blue_cells)
    red_count = len(board.red_cells)

    # penalty if board has lines that are filled with too many of our colour
    bad_red_lines = 0
    bad_blue_lines = 0
    for r in range(BOARD_N):
        red = sum(1 for cell in board.red_cells if cell.r == r)
        blue = sum(1 for cell in board.blue_cells if cell.r == r)
        if red >= BAD_LINE:
            bad_red_lines += 1
        if blue >= BAD_LINE:
            bad_blue_lines += 1

    for c in range(BOARD_N):
        red = sum(1 for cell in board.red_cells if cell.c == c)
        blue = sum(1 for cell in board.blue_cells if cell.c == c)
        if red >= BAD_LINE:
            bad_red_lines += 1
        if blue >= BAD_LINE:
            bad_blue_lines += 1

    return red_count - blue_count - (bad_red_lines - bad_blue_lines)
