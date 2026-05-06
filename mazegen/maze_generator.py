import random
from .maze import Maze
# MazeGenerator class here
# the things the user interacts with:
#   - takes parameters, kicks off generation, exposes the result

class MazeGenerator:
    def __init__(self, width, height, entry_pos, exit_pos, perfect=True, seed=None)
        # stores the parameters
        self.width = width
        self.height = height
        self.entry_pos = entry_pos
        self.exit_pos = exit_pos
        self.seed = seed
        self.perfect = perfect
        self.maze = None # not created yet

# having generate() separated allows:
#   - to set extra options before generating
#   - or generate multiple mazes with the same generator 

    def generate(self):
        # makes randomness reproducible
        random.seed(self.seed)
        # builds the maze
        self.maze = Maze(self.width, self.height, )
