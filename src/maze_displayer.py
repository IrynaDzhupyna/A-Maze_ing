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
