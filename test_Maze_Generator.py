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
        generator = MazeGenerator(
            width=width,
            height=height,
            entry_pos=entry_pos,
            exit_pos=exit_pos,
            seed=42
        )
        generator.generate()

# after generate maze correct dimensions
def test_maze_correct_dimension(maze_generated):
    maze = maze_generated.get_maze()
    assert len(maze.grid) == 8
    assert len(maze.grid[0]) == 10

# all cells are reachable, except 42 pattern
def test_all_cells_are_reachable(maze_get_maze):
    maze = maze_get_maze
    visited = set()
    queue = [maze.entry]
    visited.add((maze.entry.x, maze.entry.y))

    directions = [
        (0, -1 , "N"),
        (1, 0, "E"),
        (0, 1, "S"),
        (-1 , 0, "W")

    ]

    while queue:
        current = queue.pop(0)

        for dx, dy, direction in directions:
            nx = current.x + dx
            ny = current.y + dy

        if not current.walls[direction]:
            if 0 <= nx <= maze.width and 0 <= ny <= maze.height:
                if (nx, ny) not in visited:
                    neighbor = maze.grid[ny][nx]
                    queue.append(neighbor)
                    visited.add((nx, ny))
    assert len(visited) == maze.width * maze.height - len(maze.pattern_42)
        
        


