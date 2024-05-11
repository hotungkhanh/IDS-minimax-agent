# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction
from referee.game.pieces import *
from .board import Board
from referee.game.exceptions import IllegalActionException
import random, math

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

        valid_moves_dict: dict[int, set[PlaceAction]] = {}
        valid_moves_dict[hash(self.board)] = self.board.generate_all_moves()

        if self.board.turn_count in [0, 1]:
            action = random.choice(list(valid_moves_dict[hash(self.board)]))

        else:
            action = self.determine_minimax_depth(valid_moves_dict)

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

    def minimax_ab(self, board: Board, depth: int, alpha, beta, valid_moves_dict) -> tuple[int, PlaceAction]:

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

                val, minimax_move = self.minimax_ab(child, depth - 1, alpha, beta, valid_moves_dict)

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

                val, minimax_move = self.minimax_ab(child, depth - 1, alpha, beta, valid_moves_dict)

                if minEval > val:
                    minEval = val
                    best_move = move

                beta = min(beta, minEval)
                if beta <= alpha:
                    break

            return (minEval, best_move)

    def determine_minimax_depth(self, valid_moves_dict):
        dict_len = len(valid_moves_dict[hash(self.board)])
        if dict_len < 2:
            depth = 4
        elif dict_len < 70:
            depth = 3
        elif dict_len < 200:
            depth = 2
        else:
            depth = 1
        eval, move = self.minimax_ab(self.board, depth, -(math.inf), math.inf, valid_moves_dict)
        return move



def eval(board: Board):
    if board.winner_color == PlayerColor.RED:
        return 999
    if board.winner_color == PlayerColor.BLUE:
        return -999

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

    return red_count - blue_count - 0.2*(bad_red_lines - bad_blue_lines)