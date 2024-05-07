from referee.game.constants import *
from .board import Board
import math

UCB1_C = 1      # constant for balancing exploration & exploitation in UCB1

class TreeNode:

    '''
    Inspiration from: https://gist.github.com/kernelshreyak/d209a694ea5b4c312ab601f4dd6d7aa4
    '''

    def __init__(
        self,
        board: Board = Board(),
        parent: 'TreeNode' = None,
        children: list['TreeNode'] = None,
        wins: int = 0,
        times_visited: int = 0,
    ):
        self.board = board
        self.parent = parent
        self.children = []
        self._wins = wins
        self._times_visited = times_visited

        if children is not None:
            for child in children:
                self.add_child(child)
    
    def is_root(self):
        if self.parent is None:
            return True
        return False

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        return False

    def add_child(self, child: 'TreeNode'):
        child.parent = self
        self.children.append(child)

    @property
    def wins(self):
        '''
        getter for wins (used in UCB1)
        '''
        return self._wins
    
    @wins.setter
    def wins(self, value):
        self._wins = value

    @property
    def times_visited(self):
        return self._times_visited
    
    @times_visited.setter
    def times_visited(self, value):
        self._times_visited = value

    def UCB1(self) -> float:
        '''
        Calculate UCB1 value for this node
        '''
        try:
            ucb1 = ((self.wins/self.times_visited) + 
                    UCB1_C*math.sqrt(math.log(self.parent.times_visited)/self.times_visited))
        except ZeroDivisionError:
            return math.inf
        # print("wins, visited, ucb1:", self.wins, self.times_visited, ucb1)
        return ucb1

    def backpropagation(self):
        '''
        After rollout, back propagate the values up to root
        '''
        self._times_visited += 1
        curr_node = self
        while not curr_node.is_root():
            curr_node.parent._times_visited += 1
            curr_node.parent._wins += curr_node.wins
            curr_node = curr_node.parent
        # print("root times visited:", curr_node.times_visited)