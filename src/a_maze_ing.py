import random
import sys
from typing import List, Dict, Tuple
from get_output_file import write_output_file


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y  # x and y are the position of the cell in the maze
        self.visited = False
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }

    # From subject:    
    #     Bit 0(LSB) = North
    #     Bit 1 = East
    #     Bit 2 = South
    #     Bit 3 = West
    #
    # So ?:

    def cell_to_hex(self):
        cell_hex = 0
        if self.walls["N"] == True:
            cell_hex += 2**0
        if self.walls["E"] == True:
            cell_hex += 2**1
        if self.walls["S"] == True:
            cell_hex += 2**2
        if self.walls["W"] == True:
            cell_hex += 2**3
        cell_hex = format(cell_hex, "X")
        return cell_hex
    # old version
    # def cell_to_hex(self):
    #     cell_hex = 0
    #     if self.walls["N"] == True:
    #         cell_hex += 2**3
    #     if self.walls["E"] == True:
    #         cell_hex += 2**2
    #     if self.walls["S"] == True:
    #         cell_hex += 2**1
    #     if self.walls["W"] == True:
    #         cell_hex += 2**0
    #     cell_hex = format(cell_hex, "X")
    #     # print(cell_hex)
    #     return cell_hex


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

    def get_cell(self, x ,y):
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

            nb_walls_to_break = 10 #for example
            
            for _ in range(nb_walls_to_break):
                cell = self.get_cell(
                    random.randint(0, self.width - 1),
                    random.randint(0, self.height - 1)
                )
                print(cell.x, cell.y)

                # directions = ["N", "S", "W", "E"]
                # direction = random.choice(directions)
                # print(direction)

                neighbors = self.get_all_neighbors(cell)

                valid_neighbors = [
                    (n, d) for (n, d) in neighbors if cell.walls[d]
                ]

                if not valid_neighbors:
                    continue

                neighbor, direction = random.choice(valid_neighbors)

                if cell in self.pattern_42 or neighbor in self.pattern_42:
                    continue

                if cell == self.entry or cell == self.exit:
                    continue

                self.remove_wall(cell, neighbor, direction)
                print("wall removed")

    def remove_wall(self, current, next_cell, direction):  # remove a wall from a cell
        # and the wall from the other (opposite) cell
        opposite = {"N": "S", "S": "N", "W": "E", "E": "W"}

        current.walls[direction] = False  # destroys one wall of the current cell
        next_cell.walls[opposite[direction]] = False  # destroys the opposite wall of the next cell

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

def display(maze):  # display 2 lines for every row of the grid : top one ( horizontal walls)
    # and middle one (vertical wall and cell)

    print("\n=== Maze Terminal Visualization ===\n")
    for row in maze.grid:
        top = ""
        middle = ""

        for cell in row:
            if cell.walls["N"]:
                top += "+---"
            elif cell == maze.entry:
                top += "+---"
            else:
                top += "+   "

            if cell.walls["W"]:
                middle += "|"
            else:
                middle += " "

            if cell == maze.entry:
                middle += " A "
            elif cell == maze.exit:
                middle += " B "
            elif (cell.x, cell.y) in maze.pattern_42:
                middle += "XXX"
            else:
                middle += "   "
            # middle += "|   " if cell.walls["W"] else "    "

        print(top + "+")  # print the end of the top line
        print(middle + "|")  # print the end of the middle line

    print("+---" * maze.width + "+")  # print the very last row of the grid (the sourthmost walls)


def display_hex(maze): # displays the hexadecimal maze
    print("\n=== Hexadecimal Maze ===\n")
    line = ""
    x = 0
    y = 0
    # print(maze.grid[0][0].cell_to_hex()) # print the hexadecimal of the first cell
    # print(maze.grid[maze.height - 1][maze.width - 1].cell_to_hex()) # print the hexadecimal of the last cell
    for y in range(maze.height):
        for x in range(maze.width):
            line += maze.grid[y][x].cell_to_hex()
        print(line)
        line = ""


def read_file(file_name):
    try:
        with open(file_name, 'r') as f:
            content = f.read()
    except (FileNotFoundError, NotADirectoryError, IsADirectoryError):
        print(f"Error opening file '{file_name}': "
              f"[Errno 2] No such file or directory: '{file_name}'")
    except PermissionError:
        print(f"Error opening file '{file_name}': "
              f"[Errno 13] Permission denied: {file_name}'")
    else:
        return content
    

def fill_the_dict(content):
    lines = content.split("\n")

    data_dict = {}

    try:
        for line in lines:
            if line.strip() and not line.strip().startswith("#"):
                key, value = line.split("=", 1)
                data_dict[key.strip()] = value.strip()
    except ValueError:
        return print_error("not enough values to unpack")
    else:
        return data_dict


def print_error(message):
    print(f"{message}", file=sys.stderr)


def main():
    if len(sys.argv) != 2:
        return print_error("Not enough arguments")
    # should we check the name == "config.txt"
    file_name = sys.argv[1]
    content = read_file(file_name)
    if not content:
        return print_error("Problem with reading the file")
    data_dict = fill_the_dict(content)
    print("=== Maze configuration ===\n")
    print(content)
    maze = Maze(int(data_dict["WIDTH"]), int(data_dict["HEIGHT"]), data_dict)  # create a width x height grid with the class Maze
    random.seed(int(data_dict["SEED"])) # sets the random num gen starting point from seed(config.txt), maze is reproducible
    maze.generate()  # generate a unique path throught all the cells with DFS
    display(maze)  # display the grid on the terminal
    display_hex(maze)
    write_output_file(data_dict["OUTPUT_FILE"], maze) #writes the hex maze && entry/exit coordinates to file


if __name__ == "__main__":
    main()
