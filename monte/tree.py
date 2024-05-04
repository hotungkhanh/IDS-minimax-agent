from referee.game.constants import *
from board import Board

class TreeNode:

    '''
    Inspiration from: https://gist.github.com/kernelshreyak/d209a694ea5b4c312ab601f4dd6d7aa4
    '''

    def __init__(
        self,
        board: Board = Board(),
        score: int = 0,
        times_visited: int = 0,
        children=None,
        parent=None,
    ):
        self.board = board
        self._score = score
        self._times_visited = times_visited
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    
    def is_leaf(self):
        if len(self.children) == 0:
            return True
        return False

    def add_child(self, node: 'TreeNode'):
        node.parent = self
        self.children.append(node)

    @property
    def score(self):
        '''
        getter for score (used in UCB1)
        '''
        return self._score
    
    @score.setter
    def score(self, value):
        self._score = value