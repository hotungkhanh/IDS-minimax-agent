# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, coord
from referee.game.pieces import *
from .board import Board
from referee.game.exceptions import IllegalActionException
from .tree import TreeNode
import random, math, copy
from datetime import datetime, timedelta

import cProfile

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


def empty_neighbours(board: Board, coord: Coord) -> list[Coord]:
    neighbours = [coord.down(), coord.up(), coord.left(), coord.right()]
    output = []
    for neighbour in neighbours:
        if (neighbour not in board.blue_cells) and (neighbour not in board.red_cells):
            output.append(neighbour)
    
    return output

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
    actions = board.generate_all_moves()
    # cProfile.Profile.runctx("actions = board.generate_all_moves()", globals(), locals())
    for action in actions:
        # make each action into a new TreeNode
        child = Board(board.red_cells.copy(), board.blue_cells.copy(), 
                        board._turn_color, action, board.turn_count)
        child.apply_action(action)

        child_node = TreeNode(child)
        root.add_child(child_node)
    # correctly adding children & their parent (root)

    sec_to_run = 5
    fin_time = datetime.now() + timedelta(seconds=sec_to_run)
    while datetime.now() < fin_time:
        print("NEW ITERATION -------------------------------------------------")
        curr_state: TreeNode = root
        # find leaf node
        while not curr_state.is_leaf():
            # calculate UCB1 value of all children
            max_ucb1 = max([child.UCB1() for child in curr_state.children])
            print(max_ucb1)
            curr_state = random.choice([child for child in curr_state.children if child.UCB1() == max_ucb1])
            # curr_state = max(curr_state.children, key=lambda x: x.UCB1())
            # print("curr state board:")
            # print(curr_state.board.render())

            # just pick random child for now
            # curr_state = random.choice([child for child in curr_state.children])
        # print("curr state is now a leaf --------------------------------------")
        if curr_state.times_visited == 0:
            print("curr state has never been visited before, times visited = 0")
            # the node has NOT been visited before in previous rollouts 
            curr_state.wins = rollout(curr_state.board, self_colour) 
            curr_state.backpropagation()
            counter += 1
            # print("counter at if curr_state._times_visited == 0: ", counter)
        else:
            print("curr state has times visited > 0")
            # the node has been visited before i.e. in previous rollouts
            actions = curr_state.board.generate_all_moves()
            if len(actions) == 0:
                # debugging here: runs if curr state is a terminal state?
                continue
            for action in actions:
                # make each action into a new TreeNode
                child = Board(curr_state.board.red_cells.copy(), curr_state.board.blue_cells.copy(), 
                              curr_state.board._turn_color, action, curr_state.board.turn_count)
                child.apply_action(action)

                child_node = TreeNode(child)
                curr_state.add_child(child_node)
                # print(child_node.parent)        # for testing purposes
            try:
                rand_child: TreeNode = random.choice(curr_state.children)
                rand_child.wins = rollout(rand_child.board, self_colour)
                rand_child.backpropagation()
                # print(rand_child.board.render())
                # print("times visited in else:", curr_state.times_visited)
                counter += 1
            except:
                print(curr_state.board.render())
                print("children: ", curr_state.children)
            # print("counter at else :", counter)
            
    # return the direct child of root with the most wins 
    final_node: TreeNode = max(root.children, key=lambda x: x.wins)
    print("rollout counter at final_node:", counter)
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
        # print(temp_board.render())
        # print(temp_board.turn_count)
        # print(temp_board._turn_color)

        action = temp_board.generate_rand_move()
        temp_board.apply_action(action)
    
    winner = temp_board.winner_color
    if winner is None:
        return GAME_NOT_WON
    elif winner == self_colour:
        return GAME_WON
    else:
        return GAME_NOT_WON


