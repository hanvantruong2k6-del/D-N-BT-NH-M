from graph import Graph
def is_bipartite(graph):
    """
    Kiểm tra đồ thị có phải là đồ thị hai phía hay không.

    Sử dụng thuật toán tô màu 2 màu.

    Trả về:
        True, color  nếu là đồ thị hai phía
        False, color nếu không phải
    """

    n = graph.n
    undirected_adj = [[] for _ in range(n)]

    for u, v, w in graph.edges:
        undirected_adj[u].append(v)
        undirected_adj[v].append(u)

    color = [-1] * n
    for start in range(n):

        if color[start] != -1:
            continue

        color[start] = 0
        queue = [start]
        front = 0

        while front < len(queue):

            u = queue[front]
            front += 1

            for v in undirected_adj[u]:

                if color[v] == -1:
                    color[v] = 1 - color[u]
                    queue.append(v)

                elif color[v] == color[u]:
                    return False, color

    return True, color

def show_bipartite(graph):
    result, color = is_bipartite(graph)
    print("KIỂM TRA BIPARTITE")

    if result:

        print("Kết luận: ĐỒ THỊ LÀ HAI PHÍA.")

        group_1 = []
        group_2 = []

        for i in range(graph.n):

            if color[i] == 0:
                group_1.append(i + 1)

            else:
                group_2.append(i + 1)

        print("Tập V1:", group_1)
        print("Tập V2:", group_2)

    else:

        print("Kết luận: ĐỒ THỊ KHÔNG PHẢI LÀ HAI PHÍA.")

    return result

def main():
    print("KIỂM TRA ĐỒ THỊ HAI PHÍA")

    n = int(input("Nhập số đỉnh n: "))
    m = int(input("Nhập số cạnh m: "))

    print("\nLoại đồ thị:")
    print("1. Đồ thị vô hướng")
    print("2. Đồ thị có hướng")

    choice = int(input("Chọn: "))

    if choice == 2:
        directed = True
    else:
        directed = False

    # Tạo Graph
    graph = Graph(n, directed)

    print("\nNhập các cạnh:")
    print("Dạng: u v")
    print("Hoặc: u v w")

    for i in range(m):

        while True:

            try:

                data = input(f"Cạnh {i + 1}: ").split()

                if len(data) == 2:

                    u = int(data[0])
                    v = int(data[1])
                    w = 1

                elif len(data) == 3:

                    u = int(data[0])
                    v = int(data[1])
                    w = float(data[2])

                    if w.is_integer():
                        w = int(w)

                else:

                    print("Sai định dạng! Hãy nhập lại.")
                    continue

                if u < 1 or u > n or v < 1 or v > n:

                    print(
                        f"Đỉnh phải nằm trong khoảng 1 đến {n}."
                    )
                    continue

                graph.add_edge(u, v, w)

                break

            except ValueError:

                print("Vui lòng nhập số hợp lệ.")

    # Hiển thị danh sách cạnh
    graph.show_edge_list()

    # Kiểm tra Bipartite
    show_bipartite(graph)

if __name__ == "__main__":
    main()