from collections import deque


def solve(maze):
    if maze.entry == maze.exit:
        return [maze.entry]

    start = maze.entry
    end = maze.exit
    queue = deque([start])
    came_from = {start: None}

    directions = [
        (0, -1, "N"),
        (1, 0, "E"),
        (0, 1, "S"),
        (-1, 0, "W")
    ]

    while queue:
        current = queue.popleft()
        if current == end:
            break
        for dx, dy, direction in directions:
            nx = current.x + dx
            ny = current.y + dy
            if 0 <= nx < maze.width and 0 <= ny < maze.height:
                neighbor = maze.grid[ny][nx]
                if not current.walls[direction] and neighbor not in came_from:
                    came_from[neighbor] = (current, direction)
                    queue.append(neighbor)

    # do we need this?
    if end not in came_from:
        return []
    path = []
    # reconstruction loop - starts at the exit and goes back to start
    current = end
    while current != start:
        current, direction = came_from[current]
        path.append(direction)

    path.reverse()
    return "".join(path)
