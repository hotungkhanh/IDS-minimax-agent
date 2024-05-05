from referee.game.constants import *
from board import Board
from math import log2

UCB1_C = 2      # constant for balancing exploration & exploitation in UCB1

class TreeNode:

    '''
    Inspiration from: https://gist.github.com/kernelshreyak/d209a694ea5b4c312ab601f4dd6d7aa4
    '''

    def __init__(
        self,
        board: Board = Board(),
        parent: Board = None,
        children: list[Board] = None,
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

    def add_child(self, node: 'TreeNode'):
        node.parent = self
        self.children.append(node)

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

    def UCB1(self):
        '''
        Calculate UCB1 value for this node
        '''
        return 

    def backpropagation(self):
        '''
        After reaching terminal state, back propagate the values up to root
        '''

        pass