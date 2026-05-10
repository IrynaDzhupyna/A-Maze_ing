WHITE = '\033[97m'
RED = '\033[31m'
BLUE = '\033[34m'
GREEN = '\033[32m'
YELLOW = '\033[33m'

RESET = '\033[0m'


def display(maze):  # display 2 lines for every row
    # of the grid : top one ( horizontal walls)
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

    print("+---" * maze.width + "+")  # print the very last row of the grid


def display_hex(maze):  # displays the hexadecimal maze
    print("\n=== Hexadecimal Maze ===\n")
    line = ""
    x = 0
    y = 0
    for y in range(maze.height):
        for x in range(maze.width):
            line += maze.grid[y][x].cell_to_hex()
        line += "\n"
    print(line)


def display_after_solve(maze, path):

    print("\n=== Solved Maze Terminal Visualization ===\n")
    # print(path)

    x, y = maze.entry.x, maze.entry.y
    solved_path = [(x, y)]

    for direction in path:
        if direction == "N":
            y -= 1
        elif direction == "E":
            x += 1
        elif direction == "S":
            y += 1
        elif direction == "W":
            x -= 1
        solved_path.append((x, y))

    # print(solved_path)

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
            elif (cell.x, cell.y) in solved_path:
                middle += " O "
            else:
                middle += "   "

        print(top + "+")
        print(middle + "|")

    print("+---" * maze.width + "+")


def display_with_color(maze, color):
    print("\n=== Colored Maze Terminal Visualization ===\n")

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

        if color == "1":
            print(RED + top + "+")
            print(middle + "|")

        elif color == "2":
            print(BLUE + top + "+")
            print(middle + "|")

        elif color == "3":
            print(GREEN + top + "+")
            print(middle + "|")

        elif color == "4":
            print(YELLOW + top + "+")
            print(middle + "|")

        elif color == "5":
            print(WHITE + top + "+")
            print(middle + "|")

    print("+---" * maze.width + "+" + RESET)
