import heapq
from graph import Graph
def prim(graph, start):
    visited = set()
    pq = []
    mst = []
    total_weight = 0
    visited.add(start)
    for v, weight in graph.neighbors(start):
        heapq.heappush(pq, (weight, start, v))
    while pq:
        weight, u, v = heapq.heappop(pq)
        if v in visited:
            continue
        visited.add(v)
        mst.append((u, v, weight))
        total_weight += weight
        for next_v, next_weight in graph.neighbors(v):
            if next_v not in visited:
                heapq.heappush(
                    pq,
                    (next_weight, v, next_v)
                )
        if len(mst) == graph.num_vertices() - 1:
            break
    return mst, total_weight
graph = Graph.load_from_file("basic_undirected.graph")

mst, total_weight = prim(graph, "A")

print("Cac canh trong MST:")

for u, v, weight in mst:
    print(u, "-", v, ":", weight)

print("Tong trong so MST =", total_weight)