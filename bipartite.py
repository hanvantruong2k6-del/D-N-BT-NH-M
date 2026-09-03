
from collections import deque


def is_bipartite(graph):
    """
    Tra ve:
      result       : True/False
      color        : dict dinh -> 0/1 (mau da to), None neu khong bipartite duoc toan bo
      conflict_edge: canh gay mau thuan (u, v) neu phat hien, nguoc lai None
    Xu ly do thi khong lien thong: duyet tung thanh phan rieng.
    """
    color = {}
    conflict_edge = None

    for source in graph.vertices():
        if source in color:
            continue
        color[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v, _w in graph.neighbors(u):
                if v not in color:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    conflict_edge = (u, v)
                    return {"result": False, "color": None, "conflict_edge": conflict_edge}

    return {"result": True, "color": color, "conflict_edge": None}


def bipartite_sets(color):
    """Tach 2 tap dinh theo mau (chi dung khi is_bipartite tra ve True)."""
    set0 = [v for v, c in color.items() if c == 0]
    set1 = [v for v, c in color.items() if c == 1]
    return set0, set1
