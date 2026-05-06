import sys
from maze_definition import Maze
from read_config_file import fill_the_dict, print_error, read_file
# from typing import List, Dict, Tuple
from get_output_file import write_output_file
# for BFS queue
from maze_solver import solve
from maze_displayer import display, display_hex


def main():
    if len(sys.argv) != 2:
        return print_error("Not enough arguments")
    # should we check the name == "config.txt" ?
    
    file_name = sys.argv[1]
    content = read_file(file_name)
    
    if not content:
        return print_error("Problem with reading the file")
    
    data_dict = fill_the_dict(content)
    
    print("=== Maze configuration ===\n")
    print(content)
    
    # random.seed(int(data_dict["SEED"])) # sets the random num gen starting point from seed(config.txt), maze is reproducible
    
    maze = Maze(int(data_dict["WIDTH"]), int(data_dict["HEIGHT"]), data_dict)
    # maze.generate()  # generate a unique path throught all the cells with DFS

    while True:
        print("1: new maze")
        print("2: show path")
        print("3: toggle imperfect")
        print("q: quit")

        choice = input("> ")

        if choice == "1":
            maze.generate()

        elif choice == "2":
            # maze.solve()
            path = solve(maze)

        elif choice == "3":
            maze.perfect_maze = not maze.perfect_maze

        elif choice == "q":
            break

        # writes the hex maze && entry/exit coordinates and shortest way to file
        # write_output_file(data_dict["OUTPUT_FILE"], maze, path)
        display(maze)  # display the grid on the terminal
        display_hex(maze)

if __name__ == "__main__":
    main()
