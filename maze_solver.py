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


"""def solve_maze(maze):
    if maze.entry == maze.exit:
        return [maze.entry]

    #stores cells we need to explore
    queue = deque([maze.entry])
    # set
    visited = {maze.entry}
    # dict
    previous = {}

    while queue:
        current = queue.popleft()
        if current == maze.exit:
            break

        for neigbor in maze.get_neighbors(current):
            if neigbor not in visited:
                visited.add(neigbor)
                previous[neigbor] = current
                queue.append(neigbor)

    if maze.exit not in previous:
        return []

    current = maze.exit
    path = [maze.exit]

    while current != maze.entry:
        current = previous[current]
        path.append(current)

    path.reverse()
    return path


def convert_path_to_string(path):
    if not path:
        return ""

    directions = []

    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        if x2 == x1 and y2 == y1 - 1:
            directions.append("N")
        elif x2 == x1 + 1 and y2 == y1:
            directions.append("E")
        elif x2 == x1 and y2 == y1 + 1:
            directions.append("S")
        elif x2 == x1 - 1 and y2 == y1:
            directions.append("W")
    return "".join(directions)"""
