from mazegen import MazeGenerator
import pytest


def test_maze_correct_size(maze_obj):
    assert maze_obj.width == 10
    assert maze_obj.height == 8
    assert maze_obj.entry_pos == (0, 0)
    assert maze_obj.exit_pos == (9, 7)
    assert maze_obj.seed == 42


def test_get_maze_without_generate_raises_error(maze_obj):
    with pytest.raises(ValueError):
        maze_obj.get_maze()


@pytest.mark.parametrize("width, height, entry_pos, exit_pos", [
    (4, 8, (0, 0), (9, 7)),
    (10, 6, (0, 0), (9, 7)),
    (10, 8, (0, 0), (0, 0)),
    (6, 9, (7, 3), (5, 7)),
    (6, 9, (3, 10), (5, 7)),
    (6, 9, (5, 7), (7, 3)),
    (6, 9, (5, 7), (5, 10))
])
def test_invalid_parameters(width, height, entry_pos, exit_pos):
    with pytest.raises(ValueError):
        MazeGenerator(
            width=width,
            height=height,
            entry_pos=entry_pos,
            exit_pos=exit_pos,
            seed=42
        )