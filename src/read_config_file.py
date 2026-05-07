import sys
from maze_definition import Maze

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
        print_error("not enough values to unpack")
        return None
    else:
        return data_dict


def print_error(message):
    print(f"{message}", file=sys.stderr)


def modif_file(file_name, value):
    
    with open(file_name, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("PERFECT="):
            line = f"PERFECT={value}\n"
        new_lines.append(line)

    with open(file_name, 'w') as f:
            f.writelines(new_lines)


def modif_data(file_name, modif, maze):
    
    with open(file_name, 'r') as f:
        lines = f.readlines()

    new_lines = []

    if modif == "1":
        print("enter the new width:")
        value = int(input("> "))

        if value < 9 or value >= 429:
            raise ValueError("Width must be at least 9 and at most 429")

        elif maze.height*value >= 32000:
            raise ValueError("Grid cannot have more than 32000 cells")

        elif value <= maze.entry.x or value <= maze.exit.x:
            raise ValueError("Width is too small")
        
        else:
            for line in lines:
                if line.startswith("WIDTH="):
                    line = f"WIDTH={value}\n"
                new_lines.append(line)

            with open(file_name, 'w') as f:
                f.writelines(new_lines)

    elif modif == "2":
        print("enter the new height:")
        value = int(input("> "))

        if value < 7 or value >= 429:
            raise ValueError("Height must be at least 7 and at most 429")

        elif value*maze.width >= 32000:
            raise ValueError("Grid cannot have more than 32000 cells")

        elif value <= maze.entry.y or value <= maze.exit.y:
            raise ValueError("Height is too small")
        
        else:
            for line in lines:
                if line.startswith("HEIGHT="):
                    line = f"HEIGHT={value}\n"
                new_lines.append(line)

            with open(file_name, 'w') as f:
                f.writelines(new_lines)

    elif modif == "3":
        print("enter the new entry coordinates:(x,y)")
        value = input("> ")
        x,y = value.split(",")
        
        x = int(x)
        y = int(y)

        if x < 0 or x > maze.width:
            raise ValueError(f"x must be between 0 and {maze.width}")

        elif y < 0 or y > maze.height:
            raise ValueError(f"y must be between 0 and {maze.height}")
        
        elif x == maze.exit.x and y == maze.exit.y:
            raise ValueError("the entry and the exit cannot share the same location")

        elif (x,y) in maze.pattern_42 :
            raise ValueError("the entry cannot be in the 42 pattern")
        
        for line in lines:
            if line.startswith("ENTRY="):
                line = f"ENTRY={x},{y}\n"
            new_lines.append(line)

        with open(file_name, 'w') as f:
            f.writelines(new_lines)

    elif modif == "4":
        print("enter the new exit coordinates:(x,y)")
        value = input("> ")
        x,y = value.split(",")

        x = int(x)
        y = int(y)

        if x < 0 or x > maze.width:
            raise ValueError(f"x must be between 0 and {maze.width}")

        elif y < 0 or y > maze.height:
            raise ValueError(f"y must be between 0 and {maze.height}")
        
        elif x == maze.entry.x and y == maze.entry.y:
            raise ValueError("the entry and the exit cannot share the same location")
        
        elif (x,y) in maze.pattern_42 :
            raise ValueError("the exit cannot be in the 42 pattern")

        for line in lines:
            if line.startswith("EXIT="):
                line = f"EXIT={x},{y}\n"
            new_lines.append(line)

        with open(file_name, 'w') as f:
            f.writelines(new_lines)

    elif modif == "5":
        print("enter the seed number:")
        value = input("> ")

        for line in lines:
            if line.startswith("SEED="):
                line = f"SEED={value}\n"
            new_lines.append(line)

        with open(file_name, 'w') as f:
            f.writelines(new_lines)