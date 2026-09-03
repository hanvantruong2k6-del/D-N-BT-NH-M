from .disjointset import DisjointSet


def kruskal(graph):
    """
    Tìm cây khung nhỏ nhất bằng thuật toán Kruskal.

    graph: đối tượng Graph vô hướng có trọng số

    Trả về:
        mst: danh sách các cạnh MST dạng (u, v, weight)
        total_weight: tổng trọng số MST
    """

    vertices = graph.vertices()
    n = len(vertices)

    # Không có đỉnh
    if n == 0:
        return [], 0

    # Ánh xạ tên đỉnh -> số nguyên
    vertex_id = {
        vertex: i
        for i, vertex in enumerate(vertices)
    }

    # Lấy toàn bộ cạnh
    edges = graph.edges()

    # Sắp xếp tăng dần theo trọng số
    edges.sort(key=lambda x: x[2])

    # Tạo Union-Find
    ds = DisjointSet(n)

    mst = []
    total_weight = 0

    # Duyệt từng cạnh
    for u, v, weight in edges:

        u_id = vertex_id[u]
        v_id = vertex_id[v]

        # Hai đỉnh khác tập hợp
        if ds.find(u_id) != ds.find(v_id):

            # Chọn cạnh
            mst.append((u, v, weight))

            # Hợp nhất hai tập hợp
            ds.union(u_id, v_id)

            # Cộng trọng số
            total_weight += weight

            # Đủ n - 1 cạnh
            if len(mst) == n - 1:
                break

    return mst, total_weight
