import sys
from mazegen import MazeGenerator


def read_file(file_name: str) -> str|None:
    """
        Reads and returns the content of the file

        Args:
            file_name (str): Path to the file to be read
        
        Returns:
            str: the file content as string if successful
            None: if an error occures

        Side Effects:
            Prints error message if the file cannot be opened
        """
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


def fill_the_dict(content: str) -> dict[str, str]| None:
    """
        Parses the file into dictionary of key-value pairs.
    
        Each non-empty line that does not start with "#" is expected to be in the format "key=value". 
        Leading and trailing is removed from both keys and values.

        Args:
            content (str): file content as a single string
             
        Returns:
            dict[str: str]: a dictionary of parsed key-value pairs if successful
            None: if parsing fails
            
        Side Effects:
            calls print_error() if a line is not in the expected format
    """
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


def validate_config(data_dict: dict) -> bool:
    """Checks if keys from data_dict we send is valid, have all keys and values needed
        
        Returns:
            True if all is fine
            Calls print_error() and return False if not"""
    required_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in required_keys:
        if key not in data_dict:
            print_error(f"Missing required key: {key}")
            return False
        
    if data_dict["PERFECT"] not in ("True", "False"):
        print_error(f"PERFECT must be True or False")
        return False
    
    for key in ("ENTRY", "EXIT"):
        try:
            x, y = data_dict[key].split(",")
            int(x)
            int(y)
        except ValueError:
            print_error(f"{key} must be in x, y format")
            return False
    return True


def print_error(message: str) -> None:
    """ Prints an error message to stderr
    
        Args:
            message(str): message explaining error
            
        Returns:
            None
        
        Side Effects:
            prints message
    """
    print(f"{message}", file=sys.stderr)


def modif_file(file_name: str, value: str) -> None:
    """
        Updates the value of the "PERFECT" key in configuration file.

        It reads the file line by line, replaces the line starts with "PERFECT=" with the new value
        and writes content back to a file.
        
        Args:
            file_name (str): path to a file send as string
            value (str): New value to assign the "PERFECT" key
             
        Return:
            None
             
        Side Effects:
            Modifies the file by owerwriting its content. """
    try:
        with open(file_name, 'r') as f:
            lines = f.readlines()
    except OSError:
        print_error("Could not open the file")
        return

    new_lines = []
    for line in lines:
        if line.strip().startswith("PERFECT="):
            line = f"PERFECT={value}\n"
        new_lines.append(line)

    with open(file_name, 'w') as f:
            f.writelines(new_lines)


def modif_data(file_name: str, modif: str, maze: MazeGenerator) -> None:
    """
        Modifies a configuration file based on user input and maze constrains.

        Depending on the value of "modif" the function
        updates one of the parameters in the file:
        "1" - WIDTH
        "2" - HEIGHT
        "3" - ENTRY
        "4" - EXIT
        "5" - SEED

        Function reads the file, updates the corresponding line,
        and writes the modified content back to file.

        Args:
            file_name (str): path to the configuration file
            modif (str): option indicating which parameter to modify
            maze (MazeGenerator): 

        Returns:
            
    """
    try:
        with open(file_name, 'r') as f:
            lines = f.readlines()
    except OSError:
        print_error("Could not open the file")

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
        print("enter the new exit coordinates:(x,y)")following
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