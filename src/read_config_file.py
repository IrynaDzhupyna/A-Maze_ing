import sys


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
