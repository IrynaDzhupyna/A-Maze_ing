"""
A-Maze-ing - Main entry point for maze generation.

This module handles parsing command-line arguments, loading the config file,
and initializing the maze generation process.
"""

import sys
import os
from typing import Dict, Any


def parse_config(filepath: str) -> Dict[str, Any]:
    """
    Parse the maze configuration file.

    Args:
        filepath (str): The path to the configuration file.

    Returns:
        Dict[str, Any]: A dictionary containing the parsed config options.

    Raises:
        FileNotFoundError: If the configuration file cannot be found.
        ValueError: If the config contains invalid syntax or values.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Configuration file not found: {filepath}")

    config: Dict[str, Any] = {}
    mandatory_keys = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
    }

    with open(filepath, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            # Ignore empty lines and comments
            if not line or line.startswith('#'):
                continue

            if '=' not in line:
                raise ValueError(
                    f"Line {line_num}: Invalid syntax. Expected 'KEY=VALUE'."
                )

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            if key in config:
                raise ValueError(f"Line {line_num}: Duplicate key '{key}'.")

            # Parse known keys
            if key in ["WIDTH", "HEIGHT"]:
                try:
                    config[key] = int(value)
                    if config[key] <= 0:
                        raise ValueError(f"{key} must be a positive int.")
                except ValueError as e:
                    raise ValueError(
                        f"Line {line_num}: Invalid value for {key}. {e}"
                    )

            elif key in ["ENTRY", "EXIT"]:
                try:
                    coords = tuple(map(int, value.split(',')))
                    if len(coords) != 2:
                        raise ValueError()
                    config[key] = coords
                except ValueError:
                    raise ValueError(
                        f"Line {line_num}: Invalid format for {key} "
                        "Expected 'x,y'."
                    )

            elif key == "PERFECT":
                if value.lower() in ['true', '1', 'yes']:
                    config[key] = True
                elif value.lower() in ['false', '0', 'no']:
                    config[key] = False
                else:
                    raise ValueError(
                        f"Line {line_num}: Invalid boolean value for {key}."
                    )

            elif key == "OUTPUT_FILE":
                if not value:
                    raise ValueError(
                        f"Line {line_num}: OUTPUT_FILE cannot be empty."
                    )
                config[key] = value
            else:
                # Optionally handle extra keys
                config[key] = value

    # Check for missing mandatory keys
    missing_keys = mandatory_keys - set(config.keys())
    if missing_keys:
        missing_str = ', '.join(missing_keys)
        raise ValueError(f"Missing mandatory keys: {missing_str}")

    return config


def main() -> None:
    """
    Main function to execute the maze generation script.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config.txt>")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        config = parse_config(config_file)
        print("Configuration successfully loaded:")
        for k, v in config.items():
            print(f"  {k}: {v}")

        # TODO: Initialize the maze generator using the config

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
