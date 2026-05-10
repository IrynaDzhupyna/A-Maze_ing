Package - mazegen
Inside we have:
    - maze_generator.py
    - maze.py 
    - cell.py
maze && cell are internal. MazeGenerate - API
# __init__.py
    exposes MazeGenerator cleanly

# maze_generator.py
Inside:
    MazeGenerator class
        the user-facing class that wraps Maze

What it does:
- takes parameters of maze to generate
- kicks off generation
- exposes the result

# maze.py
Inside:
    Maze class
        the grid, validation, the recursive backtracking algorithm, the "42" pattern, wall removal for imperfect maze

What it does:
- contains internal data structure representing the grid

"""Write what exactly?"""

# cell.py
Inside:
    Cell class
        a signle cell with 4 walls (N/E/S/W) and hex encoder

What it does:
- contains internal building blocks

"""Write what exactly?"""

This separation adds simplisity for users.


## Maze class

The subject doesn't specify the minimum width/height of maze, but subject says "it must fit the "42" pattern.

Module level constants:
MIN_WIDTH_FOR_PATTERN = 7
MIN_HEIGHT_FOR_PATTERN = 5

Why 7 && 5:
    Width:
        - Pattern needs center_x + 3 < width
        - center_x = width // 2
        - so (width // 2) + 3 < width
        width = 7: 3 + 3 = 6 < 7

    Height:
        - Pattern needs center_y + 2 < height
        - center_y = heigth // 2
        - so (height // 2) + 2 < height
        height = 5: (5 // 2) + 2 = 2 + 2 = 4 < 5

Later it could be changed if pattern design will be different 


## Hatching

Hatching - build tool that creates .whl package
build-backend - mean whiich tool does the actual building. There are several options - hatching, setuptool, flit. 
Hatching works well with uv

To use - install
`uv add hatching --dev 


How it works:
    1. Get Maze object
        `maze_obj = maze.get_maze()`