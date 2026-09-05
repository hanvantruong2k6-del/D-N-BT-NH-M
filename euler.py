from collections import deque


def is_connected(graph):
    vertices = graph.vertices()

    if not vertices:
        return True

    start = None
    for v in vertices:
        if graph.degree(v) > 0:
            start = v
            break

    if start is None:
        return True

    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        u = queue.popleft()

        for v, _ in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                queue.append(v)

    for v in vertices:
        if graph.degree(v) > 0 and v not in visited:
            return False

    return True


def check_euler(graph):
    if graph.directed:
        return "Not Euler"

    if not is_connected(graph):
        return "Not Euler"

    odd_vertices = []

    for v in graph.vertices():
        if graph.degree(v) % 2 == 1:
            odd_vertices.append(v)

    if len(odd_vertices) == 0:
        return "Euler circuit"

    if len(odd_vertices) == 2:
        return "Euler path"

    return "Not Euler"