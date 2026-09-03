from graph import Graph

def input_graph():
    print("NHẬP ĐỒ THỊ")
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

    print("\n===================================")
    print("Nhập các cạnh")
    print("Dạng: u v w")
    print("Trong đó:")
    print("- u: đỉnh đầu")
    print("- v: đỉnh cuối")
    print("- w: trọng số")
    print("===================================")

    for i in range(m):

        print(f"Cạnh {i + 1}: ", end="")

        data = input().split()

        if len(data) == 2:

            u = int(data[0])
            v = int(data[1])

            # Nếu không nhập trọng số
            w = 1

        elif len(data) == 3:

            u = int(data[0])
            v = int(data[1])
            w = float(data[2])

            # Nếu là số nguyên thì hiển thị đẹp hơn
            if w.is_integer():
                w = int(w)

        else:

            print("Sai định dạng! Hãy nhập lại.")
            continue

        graph.add_edge(u, v, w)

    return graph


def main():

    graph = input_graph()

    print("\n\n===================================")
    print("THÔNG TIN ĐỒ THỊ")
    print("===================================")

    print("Số đỉnh:", graph.n)
    print("Số cạnh:", len(graph.edges))

    if graph.directed:
        print("Loại: Đồ thị có hướng")
    else:
        print("Loại: Đồ thị vô hướng")


    graph.show_edge_list()
    graph.draw("graph.png")


if __name__ == "__main__":
    main()
