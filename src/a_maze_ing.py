import sys
from mazegen import MazeGenerator
from read_config_file import fill_the_dict, print_error, read_file, modif_file, modif_data, validate_config
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

def make_generator(data_dict: dict[str, str]) -> MazeGenerator:
    """
    Creates a MazeGenerator from parsed config dictionary. 

    Args:
        data_dict (dict[str, str]): dictionary of key:values configurations

    Returns: 
        MazeGenerator: A new MazeGenerator instance
    """
    
    entry_x, entry_y = data_dict["ENTRY"].split(",")
    exit_x, exit_y = data_dict["EXIT"].split(",")

    generator = MazeGenerator(
        width = int(data_dict["WIDTH"]),
        height = int(data_dict["HEIGHT"]),
        entry_x = int(entry_x),
        entry_y = int(entry_y),
        exit_x = int(exit_x),
        exit_y = int(exit_y),
        perfect = data_dict["PERFECT"] == "True",
        seed = int(data_dict["SEED"])
    )
    return generator


def main():

    if len(sys.argv) != 2:
        return print_error("Not enough arguments")
    
    file_name = sys.argv[1]
    content = read_file(file_name)
    
    if not content:
        return print_error("Problem with reading the file")
    
    data_dict = fill_the_dict(content)
    if not data_dict or not validate_config(data_dict):
        return

    generator = make_generator(data_dict)
    
    # random.seed(int(data_dict["SEED"])) # sets the random num gen starting point from seed(config.txt), maze is reproducible
    #    this 2 lnes we dont need anymore
    # maze = Maze(int(data_dict["WIDTH"]), int(data_dict["HEIGHT"]), data_dict)
    # seed = int(data_dict["SEED"])
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

            modif_data(file_name, modif, generator)

            content = read_file(file_name)
                
            if not content:
                return print_error("Problem with reading the file")
            
            data_dict = fill_the_dict(content)

            generator = make_generator(data_dict)
            # seed = int(data_dict["SEED"])


        elif choice == "2":
            generator.generate()
            maze_obj = generator.get_maze()
            display(maze_obj)
            display_hex(maze_obj)
            
        elif choice == "3":
            maze_obj = generator.get_maze()
            path = solve(maze_obj)
            display_after_solve(maze_obj, path)  # display the grid on the terminal
            display_hex(maze_obj)
            print(path)

        elif choice == "4":
            generator.perfect_maze = not generator.perfect_maze
            print("Perfect maze = ", generator.perfect_maze)
            modif_file(file_name, generator.perfect_maze)
            
            content = read_file(file_name)
            data_dict = fill_the_dict(content)

            generator = make_generator(data_dict)
            generator.generate()

            display(generator)
            display_hex(generator)

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

            display_with_color(generator, color)
        
        elif choice == "q":
            break

        # writes the hex maze && entry/exit coordinates and shortest way to file
        # write_output_file(data_dict["OUTPUT_FILE"], maze, path)


if __name__ == "__main__":
    main()
