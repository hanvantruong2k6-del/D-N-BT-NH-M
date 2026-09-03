import heapq


def prim(graph, start):
    """
    Tìm cây khung nhỏ nhất bằng thuật toán Prim.

    graph: đối tượng Graph vô hướng có trọng số
    start: đỉnh bắt đầu

    Trả về:
        mst: danh sách cạnh MST
        total_weight: tổng trọng số
    """

    # Kiểm tra đỉnh bắt đầu
    if not graph.has_vertex(start):
        return [], 0

    visited = set()
    priority_queue = []

    mst = []
    total_weight = 0

    # Chọn đỉnh gốc
    visited.add(start)

    # Đưa các cạnh của đỉnh bắt đầu vào hàng đợi ưu tiên
    for neighbor, weight in graph.neighbors(start):
        heapq.heappush(
            priority_queue,
            (weight, start, neighbor)
        )

    # Xét các cạnh theo trọng số nhỏ nhất
    while priority_queue:

        weight, u, v = heapq.heappop(priority_queue)

        # Bỏ qua nếu v đã nằm trong cây
        if v in visited:
            continue

        # Thêm v vào cây
        visited.add(v)

        # Chọn cạnh
        mst.append((u, v, weight))

        # Cộng trọng số
        total_weight += weight

        # Đưa các cạnh mới vào hàng đợi
        for next_vertex, next_weight in graph.neighbors(v):

            if next_vertex not in visited:

                heapq.heappush(
                    priority_queue,
                    (next_weight, v, next_vertex)
                )

        # MST đủ n - 1 cạnh
        if len(mst) == graph.num_vertices() - 1:
            break

    return mst, total_weight
