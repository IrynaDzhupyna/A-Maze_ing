import random
from cell_definitions import Cell


class Maze:
    def __init__(self, width, height, data_dict):
        if width < 9 or width >= 429:
            raise ValueError("Width must be at least 9 and at most 429")

        elif height < 7 or height >= 429:
            raise ValueError("Height must be at least 7 and at most 429")

        elif height*width >= 32000:
            raise ValueError("Grid cannot have more than 32000 cells")

        self.width = width
        self.height = height

        self.grid = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
            ]

        self.pattern_42 = self.generate_pattern_42()

        self.perfect_maze = data_dict["PERFECT"]

        entry_x, entry_y = map(int, data_dict["ENTRY"].split(","))
        exit_x, exit_y = map(int, data_dict["EXIT"].split(","))

        if (entry_x, entry_y) == (exit_x, exit_y):
            raise ValueError("Entry and exit cannot share the same location")

        if (entry_x, entry_y) in self.pattern_42:
            raise ValueError("Entry cannot be inside pattern 42")

        if (exit_x, exit_y) in self.pattern_42:
            raise ValueError("Exit cannot be inside pattern 42")

        self.entry = self.get_cell(entry_x, entry_y)
        self.exit = self.get_cell(exit_x, exit_y)

    def get_cell(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"Invalid coordinates : ({x}, {y})")
        return self.grid[y][x]

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

    # Do we have two same functions or they are for different purpose
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

        # self.entry.walls["N"] = False
        # self.exit.walls["S"] = False

        if self.perfect_maze == "False":
            print("Imperfect maze")

            nb_walls_to_break = int((self.width * self.height) * 0.1)
            print("number of walls to remove :", nb_walls_to_break)

            removed_wall = 0

            while removed_wall < nb_walls_to_break:
                cell = self.get_cell(
                    random.randint(0, self.width - 1),
                    random.randint(0, self.height - 1)
                )
                # print(cell.x, cell.y)

                # directions = ["N", "S", "W", "E"]
                # direction = random.choice(directions)
                # print(direction)

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
