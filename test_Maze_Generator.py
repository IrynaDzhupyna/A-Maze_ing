import pytest
from mazegen import MazeGenerator


@pytest.fixture
def maze_obj():
    maze_obj = MazeGenerator(width=10, height=8, entry_pos=(0,0), exit_pos=(9,7), seed=42)
    return maze_obj

@pytest.fixture
def maze_generated(maze_obj):
    maze_obj.generate()
    return maze_obj

@pytest.fixture
def maze_get_maze(maze_generated):
    maze = maze_generated.get_maze()
    return maze

def test_maze_correct_size(maze_obj):
    assert maze_obj.width == 10
    assert maze_obj.height == 8
    assert maze_obj.entry_pos == (0,0)
    assert maze_obj.exit_pos == (9,7)
    assert maze_obj.seed == 42

def test_get_maze_without_generate_raises_error(maze_obj):
    with pytest.raises(ValueError):
        maze_obj.get_maze()
