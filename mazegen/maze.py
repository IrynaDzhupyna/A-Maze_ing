from .cell import Cell
import random

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
        pattern_42 (list): list of (x, y) tuples marking
        the cell that form the "42" pattern.
    """

    def __init__(self, width: int,
                 height: int,
                 entry_pos: tuple[int, int],
                 exit_pos: tuple[int, int],
                 perfect: bool = True) -> None:
        """Represents a rectangular maze with entry and exit points.
            The maze checks that its width and
            height are within allowed limits,
            and that the entry and exit positions
            are valid (inside the maze and properly formatted).

           Args:
            width (int): amound of colums in maze
            height (int): amound of rows in maze
            entry_pos (tuple[int, int]): x, y position of entry point
            exit_pos(tuple[int, int]): x, y position of exit point
            perfect (bool): specifies that only one way of solving is possible
        """
        self._validate_dimensions(width, height)
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

        if (self.width >= MIN_WIDTH_FOR_PATTERN
                and self.height >= MIN_HEIGHT_FOR_PATTERN):
            self.pattern_42 = self.generate_pattern_42()
        else:
            print("Maze is too small to fit the 42 pattern")
            self.pattern_42 = []

        entry_x, entry_y = entry_pos
        exit_x, exit_y = exit_pos
        self.entry = self.get_cell(entry_x, entry_y)
        self.exit = self.get_cell(exit_x, exit_y)

    def get_cell(self, x: int, y: int) -> Cell:
        """Returns the value of the ell at the given coordinates.

            Args:
                x (int): Column index (0-based)
                y (int): Row index (0-based)

            Returns:
                Cell

            Raises:
                ValueError: if the coordinates
                are outside of the maze bounds"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"Invalid coordinates : ({x}, {y})")
        return self.grid[y][x]

    def _validate_dimensions(self, width, height) -> None:
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

    def _validate_position(self,
                           pos: tuple[int, int],
                           name: str, width: int,
                           height: int) -> None:
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
            raise ValueError(f"{name} must be a tuple (x, y)")

        if not all(isinstance(coord, int) for coord in pos):
            raise ValueError(f"{name} must be integers")

        x, y = pos
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(f"{name} must be inside maze bounds")

    def get_neighbors(self, cell):  # get the neighbor cell of the current cell
        neighbors = []

        directions = [  # pick one of the 4 directions
            (0, -1, "N"),
            (1, 0, "E"),
            (0, 1, "S"),
            (-1, 0, "W")
        ]

        for dx, dy, direction in directions:
            nx = cell.x + dx
            ny = cell.y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.grid[ny][nx]

                if not neighbor.visited and (nx, ny) not in self.pattern_42:
                    neighbors.append((neighbor, direction))

        return neighbors

    def get_all_neighbors(self, cell):
        neighbors = []

        directions = [
            (0, -1, "N"),
            (1, 0, "E"),
            (0, 1, "S"),
            (-1, 0, "W")
        ]

        for dx, dy, direction in directions:
            nx = cell.x + dx
            ny = cell.y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.grid[ny][nx]
                neighbors.append((neighbor, direction))

        return neighbors

    def generate(self):
        stack = []
        current = self.entry  # start at the entry coordinate
        current.visited = True

        while True:
            neighbors = self.get_neighbors(current)

            if neighbors:
                next_cell, direction = random.choice(neighbors)

                stack.append(current)

                self.remove_wall(current, next_cell, direction)

                next_cell.visited = True  # set the next cell as 'visited'
                current = next_cell  # set the next cell as the current one

            elif stack:
                current = stack.pop()

            else:
                break

        if not self.perfect:
            print("Imperfect maze")

            nb_walls_to_break = int((self.width * self.height) * 0.1)
            print("number of walls to remove :", nb_walls_to_break)

            removed_wall = 0

            while removed_wall < nb_walls_to_break:
                cell = self.get_cell(
                    random.randint(0, self.width - 1),
                    random.randint(0, self.height - 1)
                )

                neighbors = self.get_all_neighbors(cell)

                valid_neighbors = [
                    (n, d) for (n, d) in neighbors
                    if cell.walls[d]
                    and (cell.x, cell.y) not in self.pattern_42
                    and (n.x, n.y) not in self.pattern_42
                ]

                if not valid_neighbors:
                    continue

                neighbor, direction = random.choice(valid_neighbors)

                if cell == self.entry or cell == self.exit:
                    continue

                if not (self.is_corridor(cell) or self.is_corridor(neighbor)):
                    continue

                else:
                    self.remove_wall(cell, neighbor, direction)
                    removed_wall += 1
                    # print("wall removed")

    def is_corridor(self, cell):
        open_walls = sum(not w for w in cell.walls.values())
        return open_walls <= 2

    def remove_wall(self, current, next_cell, direction):
        # remove a wall from a cell
        # and the wall from the other (opposite) cell
        opposite = {"N": "S", "S": "N", "W": "E", "E": "W"}

        current.walls[direction] = False
        # destroys one wall of the current cell
        next_cell.walls[opposite[direction]] = False
        # destroys the opposite wall of the next cell

    def generate_pattern_42(self):
        center_x = self.width // 2
        center_y = self.height // 2

        return [
            (center_x - 3, center_y - 2),
            (center_x - 3, center_y - 1),
            (center_x - 3, center_y),
            (center_x - 2, center_y),
            (center_x - 1, center_y - 2),
            (center_x - 1, center_y - 1),
            (center_x - 1, center_y),
            (center_x - 1, center_y + 1),
            (center_x - 1, center_y + 2),
            # '4'

            (center_x + 1, center_y - 2),
            (center_x + 1, center_y),
            (center_x + 1, center_y + 1),
            (center_x + 1, center_y + 2),
            (center_x + 2, center_y - 2),
            (center_x + 2, center_y),
            (center_x + 2, center_y + 2),
            (center_x + 3, center_y - 2),
            (center_x + 3, center_y - 1),
            (center_x + 3, center_y),
            (center_x + 3, center_y + 2),
            # '2'
        ]
