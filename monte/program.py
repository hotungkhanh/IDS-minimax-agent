# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, coord
from referee.game.pieces import *
from .board import Board
from referee.game.exceptions import IllegalActionException
from .tree import TreeNode
import random, math, copy
from datetime import datetime, timedelta

GAME_WON = 1
GAME_NOT_WON = 0

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
        # eval, child = minimax_ab(self.board, 3, -(math.inf), math.inf, self._color)
        # action = child.last_piece    

        action = monte_carlo(self.board, self._color)
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

    
# def generate_moves(board: Board, color: PlayerColor) -> PlaceAction:
#     '''
#     Returns a list of boards with new valid moves that can be made 
#     '''
#     moves = set()          # needs to be a list of states here 
#     # no piece of player colour on board
#     # FOR TESTING PURPOSES: remove randomness of first step

#     if color == PlayerColor.RED:
#         my_cells = board.red_cells
#     else:
#         my_cells = board.blue_cells

#     # if len(my_cells) == 0:
#     #     # if len(board.red_cells) == 0 and len(board.blue_cells) == 0:            
#     #     #     action = PlaceAction(
#     #     #             Coord(3, 3), 
#     #     #             Coord(3, 4), 
#     #     #             Coord(4, 3), 
#     #     #             Coord(4, 4)
#     #     #         )

#     #     #     # place piece on board
#     #     #     # new_board = Board(board.red_cells.copy(), board.blue_cells.copy(), board._turn_color, action, board.turn_count)
#     #     #     # new_board.apply_action(action)
#     #     #     moves.add(action)
#     #     #     return moves
        
#     #     empty_coords = [
#     #         Coord(r, c)
#     #         for r in range(BOARD_N)
#     #         for c in range(BOARD_N)
#     #         if ((Coord(r, c) not in board.red_cells) and (Coord(r, c) not in board.blue_cells))
#     #     ]
#     #     for cell in empty_coords:
#     #         piece_combinations = board.generate_piece_combinations(cell)

#     #         # code for random piece 
#     #         for piece in piece_combinations:
#     #             c1, c2, c3, c4 = piece
#     #             action = PlaceAction(c1, c2, c3, c4)

#     #             # new_board = Board(board.red_cells.copy(), board.blue_cells.copy(), board._turn_color, action, board.turn_count)
#     #             # new_board.apply_action(action)
#     #             moves.add(action)

#     #     return moves

#     if board.turn_count == 0:            
#         action = PlaceAction(
#                 Coord(3, 3), 
#                 Coord(3, 4), 
#                 Coord(4, 3), 
#                 Coord(4, 4)
#             )

#         # place piece on board
#         # new_board = Board(board.red_cells.copy(), board.blue_cells.copy(), board._turn_color, action, board.turn_count)
#         # new_board.apply_action(action)
#         moves.add(action)
#         return moves
    
#     elif board.turn_count == 1:
#         if board._turn_color == PlayerColor.RED:
#             opponent_cells = board.blue_cells
#         else:
#             opponent_cells = board.red_cells
        
#         empty_coords = [
#             Coord(r, c)
#             for r in range(BOARD_N)
#             for c in range(BOARD_N)
#             if ((Coord(r, c) not in board.red_cells) and (Coord(r, c) not in board.blue_cells))
#         ]

        
#         stack = []
#         for r in range(BOARD_N):
#             for c in range(BOARD_N):
#                 current_coord = Coord(r,c)
#                 stack.append((current_coord, [current_coord]))

#         while stack:
#             current_coord, current_piece = stack.pop()
#             if len(current_piece) == 4:
#                 c1, c2, c3, c4 = current_piece
#                 action = PlaceAction(c1, c2, c3, c4)
#                 moves.add(action)
#             else:
#                 for adjacent_coord in board.adjacent(current_coord):
#                     # check if adj coord is empty and not already in curr piece
#                     if (adjacent_coord not in opponent_cells):
#                         stack.append((adjacent_coord, current_piece + 
#                                         [adjacent_coord]))
#                         for coord in current_piece:
#                             stack.append((coord, current_piece + [adjacent_coord]))

#         return moves

    
#     # board has 1+ piece of player colour
#     # FOR TESTING PURPOSES: reduce randomness
#     else:
#         for cell in my_cells:
#             # if cell does not have empty neighbours
#             #   continue

#             piece_combinations = board.generate_piece_combinations(cell)

#             # code for all pieces
#             for piece in piece_combinations:
#                 c1, c2, c3, c4 = piece
#                 action = PlaceAction(c1, c2, c3, c4)

#                 # place piece on board
#                 # new_board = Board(board.red_cells.copy(), board.blue_cells.copy(), board._turn_color, action, board.turn_count)
#                 # new_board.apply_action(action)
#                 moves.add(action)
#         return moves

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
    
def minimax_ab(board: Board, depth: int, alpha, beta, color: PlayerColor) -> tuple[int, Board]:

    if depth == 0 or board.game_over:
        return (eval(board), None)
    if color == PlayerColor.RED:
        best_child = None
        maxEval = -(math.inf)
        children = generate_moves(board, color)
        for child in children:
            val = minimax_ab(child, depth - 1, alpha, beta, PlayerColor.BLUE)
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
        children = generate_moves(board, color)
        for child in children:
            val = minimax_ab(child, depth - 1, alpha, beta, PlayerColor.RED)
            if val[0] < minEval:
                minEval = val[0]
                best_child = child
            beta = min(minEval, val[0])
            if beta <= alpha:
                break
        return (minEval, best_child)

def eval(board: Board):
    blue_count = len(board.blue_cells)
    red_count = len(board.red_cells)
    return red_count - blue_count

# Monte Carlo Implementation below ---------------------------------------------
def monte_carlo(board: Board, self_colour: PlayerColor) -> PlaceAction:
    '''
    https://www.youtube.com/watch?v=UXW2yZndl7U
    curr state = initial state
    while time remaining:
        # selection
        while curr state is not a leaf node:
            curr state = child of curr state with max UCB1 value
        if curr state (i.e. a leaf node) has times_visited = 0 then:
            (this means node has NOT been sampled before)
            rollout curr state
        else:
            (this means the node HAS BEEN sampled in previous rounds)
            # expansion
            for each action from curr state:
                add new state to tree (children of curr state)
            curr state = first new child node
            rollout curr state
        backpropagate result at currstate to root
    '''
    counter = 0
    # generate initial state i.e. root node + all its children
    root = TreeNode(board)
    actions = board.generate_moves()
    for action in actions:
        # make each action into a new TreeNode
        child = Board(board.red_cells.copy(), board.blue_cells.copy(), 
                        board._turn_color, action, board.turn_count)
        child.apply_action(action)

        child_node = TreeNode(child)
        root.add_child(child_node)


    sec_to_run = 10
    fin_time = datetime.now() + timedelta(seconds=sec_to_run)
    while True:
        # keep within time limit
        if datetime.now() >= fin_time:
            break

        # find leaf node
        curr_state = root
        while not curr_state.is_leaf():
            # calculate UCB1 value of all children LATER, don't worry about it now
            # max_UCB1 = max(child.UCB1() for child in curr_state.children)

            # just pick random child for now

            curr_state = random.choice([child for child in curr_state.children])
            print(curr_state.board.render())

        if curr_state._times_visited == 0:
            # the node has NOT been visited before in previous rollouts 
            curr_state.wins = rollout(curr_state.board, self_colour) 
            curr_state.backpropagation()
            counter += 1
            # print("counter at if curr_state._times_visited == 0: ", counter)
        else:
            # the node has been visited before i.e. in previous rollouts
            actions = curr_state.board.generate_moves()
            for action in actions:
                # make each action into a new TreeNode
                child = Board(curr_state.board.red_cells.copy(), curr_state.board.blue_cells.copy(), 
                              curr_state.board._turn_color, action, curr_state.board.turn_count)
                child.apply_action(action)

                child_node = TreeNode(child)
                curr_state.add_child(child_node)
                # print(child_node.parent)        # for testing purposes

            rand_child: TreeNode = random.choice(curr_state.children)
            rand_child.wins = rollout(rand_child.board, self_colour)
            rand_child.backpropagation()
            counter += 1
            print("counter at else :", counter)
            
    # return the direct child of root with the most wins 
    final_node: TreeNode = max(root.children, key=lambda x: x.wins)
    print("counter at final_node:", counter)
    return final_node.board.last_piece


def rollout(board: Board, self_colour: PlayerColor) -> int:
    '''
    while True:
        if state is a terminal state:
            return win percentage of state
        action = choose random action out of all possible actions
        state = simulate(action, state) i.e. apply action, update state & look again
        # remember to flip player colours 
    '''
    temp_board = Board(board.red_cells.copy(), board.blue_cells.copy(), 
                       board._turn_color, board.last_piece, board.turn_count)
    while not temp_board.game_over:
        # print("rollout while entered")
        # print("turncount = ", temp_board.turn_count, " turncolor = ", temp_board._turn_color)
        actions = temp_board.generate_moves()
        # print(temp_board.render())
        # print(temp_board.turn_count)
        # print(temp_board._turn_color)

        action = random.choice(list(actions))
        temp_board.apply_action(action)
    
    winner = temp_board.winner_color
    if winner is None:
        return GAME_NOT_WON
    elif winner == self_colour:
        return GAME_WON
    else:
        return GAME_NOT_WON


