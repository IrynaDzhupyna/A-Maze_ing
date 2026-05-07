import sys
import random
from maze_definition import Maze
from read_config_file import fill_the_dict, print_error, read_file, modif_file, modif_data
# from typing import List, Dict, Tuple
from get_output_file import write_output_file
# for BFS queue
from maze_solver import solve
from maze_displayer import display, display_hex, display_after_solve, display_with_color

WHITE = '\033[97m'
RED = '\033[31m'
BLUE = '\033[34m'
GREEN = '\033[32m'
YELLOW = '\033[33m'

RESET = '\033[0m'

def main():
    if len(sys.argv) != 2:
        return print_error("Not enough arguments")
    # should we check the name == "config.txt" ?
    
    file_name = sys.argv[1]
    content = read_file(file_name)
    
    if not content:
        return print_error("Problem with reading the file")
    
    data_dict = fill_the_dict(content)
    
    # random.seed(int(data_dict["SEED"])) # sets the random num gen starting point from seed(config.txt), maze is reproducible
    
    maze = Maze(int(data_dict["WIDTH"]), int(data_dict["HEIGHT"]), data_dict)
    seed = int(data_dict["SEED"])
    # maze.generate()  # generate a unique path throught all the cells with DFS

    print("===========================================")
    print("=== Welcome to Iryna and Gianni's Maze! ===")
    print("===========================================\n")
    
    while True:
        print("0: display configuration")
        print("1: modify configuration")
        print("2: new maze")
        print("3: show path")
        print("4: toggle imperfect")
        print("5: change color\n")
        print("q: quit")

        choice = input("> ")

        if choice == "0":
            print("=== Maze configuration ===\n")
            print(content, "\n")

        elif choice == "1":
            print("What do you want to modify ?\n")
            print("1: modify the width")
            print("2: modify the height")
            print("3: modify the entry coordinates")
            print("4: modify the exit coordinates")
            print("5: change the seed\n")
            print("q: quit")

            modif = input("> ")

            if modif == "q":
                break

            modif_data(file_name, modif, maze)

            content = read_file(file_name)
                
            if not content:
                return print_error("Problem with reading the file")
            
            data_dict = fill_the_dict(content)

            maze = Maze(int(data_dict["WIDTH"]), int(data_dict["HEIGHT"]), data_dict)
            seed = int(data_dict["SEED"])


        elif choice == "2":
            maze.generate(seed)
            display(maze)  # display the grid on the terminal
            display_hex(maze)
            
        elif choice == "3":
            path = solve(maze)
            display_after_solve(maze, path)  # display the grid on the terminal
            display_hex(maze)
            print(path)

        elif choice == "4":
            maze.perfect_maze = not maze.perfect_maze
            print("Perfect maze = ", maze.perfect_maze)
            modif_file(file_name, maze.perfect_maze)
            
            content = read_file(file_name)
            data_dict = fill_the_dict(content)

            maze = Maze(int(data_dict["WIDTH"]), int(data_dict["HEIGHT"]), data_dict)
            
            maze.generate(seed)

            display(maze)
            display_hex(maze)

        elif choice == "5":
            print("=== Pick your color ! ===\n")
            print("1: print in " + RED + "red" + RESET)
            print("2: print in " + BLUE + "blue" + RESET)
            print("3: print in " + GREEN + "green" + RESET)
            print("4: print in " + YELLOW + "yellow" + RESET)
            print("5: back to default\n")
            print("q: quit")

            color = input("> ")

            if color == "q":
                break

            display_with_color(maze, color)
        
        elif choice == "q":
            break

        # writes the hex maze && entry/exit coordinates and shortest way to file
        # write_output_file(data_dict["OUTPUT_FILE"], maze, path)


if __name__ == "__main__":
    main()
