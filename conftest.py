import pytest
from mazegen import MazeGenerator

@pytest.fixture
# fresh MazeGenerator, no generate() called
def maze_obj():
    maze_obj = MazeGenerator(width=10, height=8, entry_pos=(0,0), exit_pos=(9,7), seed=42)
    return maze_obj

@pytest.fixture
# takes maze_obj, calls generate() on it
def maze_generated(maze_obj):
    maze_obj.generate()
    return maze_obj

@pytest.fixture
# takes maze_generated, calls get_maze() on it
def maze_get_maze(maze_generated):
    maze = maze_generated.get_maze()
    return maze
