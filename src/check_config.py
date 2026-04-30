import sys


def print_error(message):
    print(f"{message}", file=sys.stderr)


def read_file(file_name):
    try:
        with open(file_name, "r") as file:
            content = file.read()
    except (FileNotFoundError, NotADirectoryError):
        print(f"Error opening file '{file_name}': "
              f"[Errno 2] No such file or directory: '{file_name}'")
    except PermissionError:
        print(f"Error opening file '{file_name}': "
              f"[Errno 13] Permission denied: '{file_name}'")
    else:
        return content


def fill_the_dict(content):
    # what if no "\n" found
    lines = content.split("\n")
    dictunary = {}
    try:
        for line in lines:
            key, value = line.split("=", 2)
            dictunary[key] = value
            print(key, value)
    except ValueError:
        return print_error("not enough values to unpack")
    else:
        return dictunary



def main():
    if len(sys.argv) != 2:
        return print_error("Not enough argumens")
    # should we check the name == "config.txt"
    file_name = sys.argv[1]
    content = read_file(file_name)
    if not content:
        return print_error("Problem in reading a file")
    # create a dict out of content
    our_dict = fill_the_dict(content)
    print(our_dict)

if __name__ == "__main__":
    main()