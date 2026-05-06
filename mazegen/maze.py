from .cell import Cell

MIN_WIDTH_FOR_PATTERN = 7
MIN_HEIGHT_FOR_PATTERN = 5

class Maze:
    """Represents 2D maze grid composted of Cell objects
        
        Attributes:
        width (int): amount of colums in maze
        height (int): amount of rows in maze
        entry_pos (tuple[int, int]): x, y position of entry point
        exit_pos(tuple[int, int]): x, y position of exit point
        perfect (bool): specifies that only one way of solving is possible
        grid (list): 2D list of Cell objects
        pattern_42 (list): list of (x, y) tuples marking the cell that form the "42" pattern.
    """
    def __init__(self, width: int, height: int, entry_pos: tuple[int, int], exit_pos: tuple[int, int], perfect: bool=True) -> None:
        """Represents a rectangular maze with entry and exit points.
            The maze checks that its width and height are within allowed limits, 
            and that the entry and exit positions are valid (inside the maze and properly formatted).
        
            Atributes:
            width (int): amound of colums in maze
            height (int): amound of rows in maze
            entry_pos (tuple[int, int]): x, y position of entry point
            exit_pos(tuple[int, int]): x, y position of exit point
            perfect (bool): specifies that only one way of solving is possible
        """
        self._validate_dimentions(width, height)
        self._validate_position(entry_pos, "entry_pos", width, height)
        self._validate_position(exit_pos, "exit_pos", width, height)

        if entry_pos == exit_pos:
            raise ValueError("entry_pos and exit_pos cannot be the same")
        
        self.width = width
        self.height = height
        self.entry_pos = entry_pos
        self.exit_pos = exit_pos
        self.perfect = perfect

        self.grid = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
            ]
        
        if self.width >= MIN_WIDTH_FOR_PATTERN and self.height >= MIN_HEIGHT_FOR_PATTERN:
            self.pattern_42 = self.generate_pattern_42()
        else:
            print("Maze is too small to fit the 42 pattern")
            self.pattern_42 = []

        entry_x, entry_y = entry_pos
        exit_x, exit_y = exit_pos
        self.entry = self.get_cell(entry_x, entry_y)
        self.exit = self.get_cell(exit_x, exit_y)


        def get_cell(self, x, y) -> Cell:
            """Returns the value of the ell at the given coordinates.
                
                Args:
                    x (int): Column index (0-based)
                    y (int): Row index (0-based)
                    
                Returns:
                    Cell
                    
                Raises:
                    ValueError: if the coordinates are outside of the maze bounds"""
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise ValueError(f"Invalid coordinates : ({x}, {y})")
            return self.grid[y][x]


        def _validate_dimensions(self, width, height)-> None:
            """Validate maze dimensions.
                Args:
                    width (int): Width of the maze
                    height (int): Height of the maze
                    
                Raises:
                    ValueError: if dimensions are out of allowed bounds.
            """
            if width <= 0 or height <= 0:
                raise ValueError("Width and height must be positive")

            if height*width >= 32000:
                raise ValueError("Grid cannot have more than 32000 cells")


        def _validate_position(self, pos: tuple[int, int], name: str, width: int, height: int) -> None:
            """Validates a position inside the maze.
            
                Args:
                    pos (tuple[int, int]): Position to validate
                    name (str): Name of the position (for error message)
                    width (int): Maze width
                    height (int): Maze height
                    
                Raises:
                    ValueError; if position is invalid or out of bounds.
            """
            if not isinstance(pos, tuple) or len(pos) != 2:
                raise ValueError(f"{name} must be a tuple {x, y}")
            
            if not all(isinstance(coord, int) for coord in pos):
                raise ValueError(f"{name} must be integers")
            
            x, y = pos
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(f"{name} must be inside maze bounds")