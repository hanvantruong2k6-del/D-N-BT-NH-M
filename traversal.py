from collections import deque


class GraphTraversal:

    def __init__(self, graph):
        self.graph = graph

    # =========================
    # BFS
    # =========================
    def bfs(self, start):
        visited = [False] * self.graph.n
        result = []

        queue = deque()

        start -= 1

        if start < 0 or start >= self.graph.n:
            print("Đỉnh bắt đầu không hợp lệ!")
            return []

        visited[start] = True
        queue.append(start)

        while queue:
            u = queue.popleft()

            result.append(u + 1)

            for v, w in self.graph.adj_list[u]:

                if not visited[v]:
                    visited[v] = True
                    queue.append(v)

        return result

    # =========================
    # DFS
    # =========================
    def dfs(self, start):
        visited = [False] * self.graph.n
        result = []

        start -= 1

        if start < 0 or start >= self.graph.n:
            print("Đỉnh bắt đầu không hợp lệ!")
            return []

        self._dfs(start, visited, result)

        return result

    def _dfs(self, u, visited, result):

        visited[u] = True
        result.append(u + 1)

        for v, w in self.graph.adj_list[u]:

            if not visited[v]:
                self._dfs(v, visited, result)


# =====================================
# CHẠY THỬ
# =====================================

if __name__ == "__main__":

    # Import Graph từ graph.py
    from graph import Graph

    # Tạo đồ thị vô hướng 5 đỉnh
    g = Graph(5, directed=False)

    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(2, 5)
    g.add_edge(3, 5)

    # Tạo đối tượng Traversal
    traversal = GraphTraversal(g)

    # BFS
    print("===== TRAVERSAL =====")

    bfs_result = traversal.bfs(1)

    print("BFS:", " -> ".join(map(str, bfs_result)))

    # DFS
    dfs_result = traversal.dfs(1)

    print("DFS:", " -> ".join(map(str, dfs_result)))