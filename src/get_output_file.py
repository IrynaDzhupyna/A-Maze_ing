def write_output_file(file_name, maze, path):
    with open(file_name, 'w') as file:
        for y in range(maze.height):
            line = ""
            for x in range(maze.width):
                line += maze.grid[y][x].cell_to_hex()
            file.write(line + "\n")

        file.write("\n")
        file.write(f"{maze.entry.x},{maze.entry.y}\n")
        file.write(f"{maze.exit.x},{maze.exit.y}\n")
        file.write(f"{path}\n")