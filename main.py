# -*- coding: utf-8 -*-
"""
  1. graph.py       -> cau truc Graph, 3 cach bieu dien, doc file mau
  2. traversal.py    -> BFS, DFS
  3. bipartite.py     -> kiem tra do thi hai phia
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.graph import Graph
from src import traversal
from src import bipartite
from src import visualize
from src.kruskal import kruskal
from src.prim import prim
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")
IMAGES_DIR = os.path.join(BASE_DIR, "outputs", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)


def section(title):
    print("\n" + "=" * 78)
    print(f"  {title}")
    print("=" * 78)


def img(name):
    return os.path.join(IMAGES_DIR, name)


# =============================================================================
# 1. GRAPH.PY - CAU TRUC DO THI + 3 CACH BIEU DIEN + DOC FILE MAU
# =============================================================================
def demo_graph():
    section("1. GRAPH.PY - INPUT DO THI, VE HINH, 3 CACH BIEU DIEN")

    # ---- Doc do thi tu file mau ----
    g = Graph.load_from_file(os.path.join(SAMPLES_DIR, "basic_undirected.graph"))
    print("DEBUG - danh sach dinh doc duoc:", g.vertices())
    print(g.summary())

    # ---- Ve va luu hinh ----
    pos = visualize.draw_graph(g, img("01_basic_undirected_graph.png"),
                                title="Do thi vo huong dau vao (G)")
    print("Da luu hinh: 01_basic_undirected_graph.png")

    # ---- 3 cach bieu dien ----
    print()
    g.print_adjacency_list()
    print()
    g.print_adjacency_matrix()
    print()
    g.print_edge_list()

    # ---- Kiem chung chuyen doi qua lai ----
    print("\n-- Kiem chung chuyen doi qua lai --")
    verts, matrix = g.to_adjacency_matrix()
    g2 = Graph.from_adjacency_matrix(verts, matrix, directed=g.directed, weighted=g.weighted)
    print("Tu Adjacency Matrix -> dung lai Graph -> so canh:", g2.num_edges(),
          "(goc:", g.num_edges(), ")")

    edge_list = g.to_edge_list()
    g3 = Graph.from_edge_list(g.vertices(), edge_list, directed=g.directed, weighted=g.weighted)
    print("Tu Edge List -> dung lai Graph -> so canh:", g3.num_edges(),
          "(goc:", g.num_edges(), ")")

    return g, pos


# =============================================================================
# 2. TRAVERSAL.PY - BFS & DFS
# =============================================================================
def demo_traversal(g, pos):
    section("2. TRAVERSAL.PY - DUYET DO THI BANG BFS & DFS")
    start = "A"
    print(f"Dinh xuat phat: {start}\n")

    bfs_res = traversal.bfs(g, start)
    print("[BFS] Thu tu tham:", " -> ".join(bfs_res["order"]))
    print("[BFS] Cay BFS (canh):", bfs_res["tree_edges"])
    print("[BFS] Khoang cach tu", start, ":", bfs_res["distance"])

    order_labels = {v: i + 1 for i, v in enumerate(bfs_res["order"])}
    visualize.draw_graph(g, img("02_bfs_traversal.png"), title=f"BFS tu dinh {start}",
                          pos=pos, highlighted_edges=bfs_res["tree_edges"],
                          node_order_labels=order_labels)
    print("Da luu hinh: 02_bfs_traversal.png")

    dfs_res = traversal.dfs(g, start)
    print(f"\n[DFS] Thu tu tham (tien tu):", " -> ".join(dfs_res["order"]))
    print("[DFS] Cay DFS (canh):", dfs_res["tree_edges"])

    order_labels_dfs = {v: i + 1 for i, v in enumerate(dfs_res["order"])}
    visualize.draw_graph(g, img("03_dfs_traversal.png"), title=f"DFS tu dinh {start}",
                          pos=pos, highlighted_edges=dfs_res["tree_edges"],
                          node_order_labels=order_labels_dfs)
    print("Da luu hinh: 03_dfs_traversal.png")


# =============================================================================
# 3. BIPARTITE.PY - KIEM TRA DO THI HAI PHIA
# =============================================================================
def demo_bipartite():
    section("3. BIPARTITE.PY - KIEM TRA DO THI HAI PHIA")

    g_yes = Graph.load_from_file(os.path.join(SAMPLES_DIR, "bipartite_yes.graph"))
    res_yes = bipartite.is_bipartite(g_yes)
    print("(a) bipartite_yes.graph ->", g_yes.summary())
    print("    Ket qua:", "LA do thi hai phia" if res_yes["result"] else "KHONG phai")
    if res_yes["result"]:
        s0, s1 = bipartite.bipartite_sets(res_yes["color"])
        print("    Tap 1:", s0, " | Tap 2:", s1)
    visualize.draw_bipartite(g_yes, img("04_bipartite_true.png"),
                              "Do thi hai phia (True)", res_yes["color"])
    print("    Da luu hinh: 04_bipartite_true.png")

    g_no = Graph.load_from_file(os.path.join(SAMPLES_DIR, "bipartite_no.graph"))
    res_no = bipartite.is_bipartite(g_no)
    print("\n(b) bipartite_no.graph ->", g_no.summary())
    print("    Ket qua:", "LA do thi hai phia" if res_no["result"] else "KHONG phai")
    if not res_no["result"]:
        print("    Canh gay mau thuan:", res_no["conflict_edge"])
    visualize.draw_bipartite(g_no, img("05_bipartite_false.png"),
                              "Do thi hai phia (False)", None)
    print("    Da luu hinh: 05_bipartite_false.png")


# T.Trang
# ==================================================
# ĐỌC FILE DỮ LIỆU
# ==================================================

DATA_FILE = os.path.join(
    BASE_DIR,
    "samples",
    "mst_sample.graph"
)

# Đọc đồ thị MST từ file mẫu
graph = Graph.load_from_file(DATA_FILE)

# ==================================================
# HIỂN THỊ MST
# ==================================================

def hien_thi_mst(mst, total_weight):

    if not mst:
        print("Khong tim thay MST!")
        return

    print("\nCac canh trong MST:")

    for u, v, weight in mst:
        print(f"{u} -- {v} : {weight}")

    print(f"\nTong trong so MST = {total_weight}")


# ==================================================
# CHẠY KRUSKAL
# ==================================================

def xu_ly_kruskal():

    print("\n========== KRUSKAL ==========")

    mst, total_weight = kruskal(graph)

    hien_thi_mst(
        mst,
        total_weight
    )


# ==================================================
# CHẠY PRIM
# ==================================================

def xu_ly_prim():

    print("\n========== PRIM ==========")

    start = input(
        "Nhap dinh bat dau: "
    ).strip()

    if not graph.has_vertex(start):

        print("Dinh khong ton tai!")

        return

    mst, total_weight = prim(
        graph,
        start
    )

    print(
        f"\nDinh goc: {start}"
    )

    hien_thi_mst(
        mst,
        total_weight
    )


# ==================================================
# SO SÁNH KRUSKAL VÀ PRIM
# ==================================================

def so_sanh():

    print("\n========== SO SANH ==========")

    # Kruskal
    mst_k, total_k = kruskal(graph)

    # Chọn một đỉnh gốc khác
    # so với đỉnh đầu tiên để kiểm tra tính ổn định
    vertices = graph.vertices()

    if len(vertices) < 2:

        print("Do thi can it nhat 2 dinh.")

        return

    start = vertices[1]

    # Prim
    mst_p, total_p = prim(
        graph,
        start
    )

    print("\n--- KRUSKAL ---")

    hien_thi_mst(
        mst_k,
        total_k
    )

    print("\n--- PRIM ---")

    print(
        f"Dinh goc Prim = {start}"
    )

    hien_thi_mst(
        mst_p,
        total_p
    )

    print("\n--- KET LUAN ---")

    if total_k == total_p:

        print(
            "Kruskal va Prim cho cung "
            "tong trong so MST."
        )

    else:

        print(
            "Kruskal va Prim cho ket qua "
            "khac nhau."
        )


# ==================================================
# THỬ PRIM VỚI NHIỀU ĐỈNH GỐC
# ==================================================

def thu_nhieu_dinh_goc():

    print("\n========== THU NHIU DINH GOC ==========")

    vertices = graph.vertices()

    for start in vertices:

        mst, total_weight = prim(
            graph,
            start
        )

        print(
            f"Bat dau tu {start}"
            f" -> Tong MST = {total_weight}"
        )


# ==================================================
# TRUY VẤN ĐỈNH KỀ
# ==================================================

def truy_van_dinh_ke():

    v = input(
        "Nhap dinh can truy van: "
    ).strip()

    if not graph.has_vertex(v):

        print("Dinh khong ton tai!")

        return

    print(
        f"\nCac dinh ke cua {v}:"
    )

    for neighbor, weight in graph.neighbors(v):

        print(
            f"{neighbor} "
            f"(trong so = {weight})"
        )


# ==================================================
# TRUY VẤN TRỌNG SỐ
# ==================================================

def truy_van_trong_so():

    u = input("Nhap dinh u: ").strip()
    v = input("Nhap dinh v: ").strip()

    if not graph.has_vertex(u):

        print(f"Dinh {u} khong ton tai!")

        return

    if not graph.has_vertex(v):

        print(f"Dinh {v} khong ton tai!")

        return

    if graph.has_edge(u, v):

        weight = graph.edge_weight(
            u,
            v
        )

        print(
            f"Canh {u} -- {v}"
            f" co trong so = {weight}"
        )

    else:

        print(
            f"Khong co canh {u} -- {v}."
        )


# ==================================================
# MAIN
# ==================================================

def main():

    print(
        "\n======================================"
    )

    print(
        "     CHUONG TRINH KRUSKAL VA PRIM"
    )

    print(
        "======================================"
    )

    print(
        graph.summary()
    )

    print(
        "\nDu lieu: samples/mst_sample.graph"
    )


    while True:

        print("\n======================================")
        print("                MENU")
        print("======================================")
        print("1. Xem thong tin do thi")
        print("2. Xem danh sach dinh")
        print("3. Xem danh sach canh")
        print("4. Truy van cac dinh ke")
        print("5. Truy van trong so cua canh")
        print("6. Chay Kruskal")
        print("7. Chay Prim")
        print("8. So sanh Kruskal va Prim")
        print("9. Thu Prim voi tat ca dinh goc")
        print("0. Thoat")
        print("======================================")

        choice = input(
            "Nhap lua chon: "
        ).strip()


        # 1
        if choice == "1":

            print("\n========== THONG TIN ==========")

            print(
                graph.summary()
            )


        # 2
        elif choice == "2":

            print(
                "\n========== DANH SACH DINH =========="
            )

            for v in graph.vertices():

                print(v, end=" ")

            print()


        # 3
        elif choice == "3":

            print(
                "\n========== DANH SACH CANH =========="
            )

            for u, v, weight in graph.edges():

                print(
                    f"{u} -- {v} : {weight}"
                )


        # 4
        elif choice == "4":

            print(
                "\n========== TRUY VAN DINH KE =========="
            )

            truy_van_dinh_ke()


        # 5
        elif choice == "5":

            print(
                "\n========== TRUY VAN TRONG SO =========="
            )

            truy_van_trong_so()


        # 6
        elif choice == "6":

            xu_ly_kruskal()


        # 7
        elif choice == "7":

            xu_ly_prim()


        # 8
        elif choice == "8":

            so_sanh()


        # 9
        elif choice == "9":

            thu_nhieu_dinh_goc()


        # 0
        elif choice == "0":

            print(
                "\nKet thuc chuong trinh."
            )

            break


        else:

            print(
                "\nLua chon khong hop le!"
            )

if __name__ == "__main__":
    main()
