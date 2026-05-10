import random
from .maze import Maze
# MazeGenerator class here
# the things the user interacts with:
#   - takes parameters, kicks off generation, exposes the result

class MazeGenerator:
    # describes the object
    #   what class represents, what used for, what it stores (attributes)
    """
        Generates a maze based on given parameters such as size,
        entry/exit positions, and generation type(perfect/imperfect).
         
        Attributes:
            width (int): width of maze
            height (int): height of maze
            entry_pos (tuple[int, int]): entry position as (x,y)
            exit_pos(tuple[int, int]): exit position as (x,y)
            perfect (bool, optional): whether the maze is perfect
            seed (int|None): random seed
         """
    def __init__(self, width, height, entry_pos, exit_pos, perfect=True, seed=None) -> None:
        # describes initalization (inputs)
        #   what you passed in and what they mean
        """
        Initializes a MazeGenerator with configuration parameters.

        Args:
            width (int): amount of colums in maze
            height (int): amount of rows in maze
            entry_pos (tuple[int, int]): entry position as (x,y)
            exit_pos(tuple[int, int]): exit position as (x,y)
            perfect (bool, optional): if True, generates a perfect maze
                                        (no loops, only one way path between two points).
                                        Defaults to True
                                    
            seed (int|None): random seed for reproducible maze generation. If None, randomness is not fixed"""
        # stores the parameters
        self.width = width
        self.height = height
        self.entry_pos = entry_pos
        self.exit_pos = exit_pos
        self.seed = seed
        self.perfect = perfect
        self.maze = None # not created yet


    def generate(self) -> None:
        """
            Generates a new maze instance using the current configuration.

            This method initializes the random seed, creates a Maze object with the provided parameters,
            and generates the maze structure.

            Returns:
                None
        """
        random.seed(self.seed)
        self.maze = Maze(self.width, self.height, self.entry_pos, self.exit_pos, self.perfect)
        self.maze.generate()


    def get_maze(self) -> Maze:
        """
        Returns the generated maze object

        Returns: The generated maze

        Raises:
            ValueError if generate() has not been called yet. 
        """
        if self.maze is None:
            raise ValueError("Maze hasn't been generated yet. Call generate() first")
        return self.maze
        
        