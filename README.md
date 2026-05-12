*This project has been created as part of the 42 curriculum by irdzhupy, glegrand.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. It generates mazes from a 
configuration file, displays them in the terminal, and writes the result to an 
output file using a hexadecimal wall representation. The maze can be perfect 
(one unique path between entry and exit) or imperfect. It also contains a 
hidden "42" pattern visible in the terminal display.

## Instructions

### Installation
\```bash
git clone <your_repo_url>
cd a_maze_ing
make install
\```

### Running
\```bash
make run
# or
python3 a_maze_ing.py config.txt
\```

### Menu options
- `0` — display current configuration
- `1` — modify configuration
- `2` — generate and display a new maze
- `3` — show shortest path
- `4` — toggle perfect/imperfect
- `5` — change wall color
- `q` — quit

## Configuration File

The config file uses `KEY=VALUE` format. Lines starting with `#` are comments.

| Key | Description | Example |
|-----|-------------|---------|
| WIDTH | Maze width in cells | `WIDTH=20` |
| HEIGHT | Maze height in cells | `HEIGHT=15` |
| ENTRY | Entry coordinates (x,y) | `ENTRY=0,0` |
| EXIT | Exit coordinates (x,y) | `EXIT=19,14` |
| OUTPUT_FILE | Output filename | `OUTPUT_FILE=maze.txt` |
| PERFECT | Perfect maze? True/False | `PERFECT=True` |
| SEED | Random seed | `SEED=42` |

## Maze Generation Algorithm

We used **DFS (Depth-First Search / recursive backtracker)** for maze generation
and **BFS (Breadth-First Search)** for finding the shortest path.

We chose DFS because it produces mazes with long winding corridors and few 
dead ends, which makes them visually interesting and challenging to solve.

## Reusable Module (mazegen)

The maze generation logic is packaged as a reusable Python module called `mazegen`.

### Installation
\```bash
pip install mazegen-0.1.0-py3-none-any.whl
\```

### Basic Example
\```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    entry_pos=(0, 0),
    exit_pos=(19, 14),
    perfect=True,
    seed=42
)

generator.generate()
maze = generator.get_maze()

print(maze.width, maze.height)
print(maze.entry, maze.exit)

cell = maze.get_cell(5, 3)
print(cell.walls)  # {'N': True, 'E': False, 'S': True, 'W': True}
\```

### Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| width | int | Number of columns |
| height | int | Number of rows |
| entry_pos | tuple[int, int] | Entry coordinates (x, y) |
| exit_pos | tuple[int, int] | Exit coordinates (x, y) |
| perfect | bool | One path only if True |
| seed | int or None | Random seed |

### Accessing the Solution
\```python
from maze_solver import solve
path = solve(maze)  # returns string e.g. "EESSWN"
\```

## Resources

- [Maze generation algorithms - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Depth-first search - Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Breadth-first search - Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python packaging guide](https://packaging.python.org/en/latest/)

### AI Usage
We used Claude AI during this project for:
- Explaining BFS and DFS concepts
- Debugging crashes and error handling
- Reviewing code structure and suggesting fixes
- Helping write and structure the README

## Team and Project Management

### Roles
- **irdzhupy** — config parsing, error handling, maze display, solver, README
- **glegrand** — maze generation (DFS), Cell and Maze classes, mazegen package, Makefile

### Planning
We initially planned to finish the core generation in the first week and 
the display and output in the second. In practice, the maze generation 
took longer than expected due to the "42" pattern and the imperfect maze 
requirements.

We also realized late that we needed a reusable package, after we had 
already built the maze generation and output file. This required significant 
refactoring — we added the `MazeGenerator` class, refactored the `Maze` class, 
and updated all other files to work with the new structure.

### What worked well
- Splitting the work clearly between generation and display
- Using a seed made testing and debugging much easier
- The reusable package structure was straightforward with hatchling

### What could be improved
- We could have written tests earlier to catch bugs faster
- The ASCII display could be prettier with Unicode characters

### Tools used
- VSCode
- Git / GitHub
- Claude AI — used for explaining concepts, debugging, and reviewing code structure