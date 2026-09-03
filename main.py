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

SAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "images")
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


# =============================================================================
# HAM MAIN - goi tuan tu 3 phan tren
# =============================================================================
def main():
    print("#" * 78)
    print("#  TEST: GRAPH.PY + TRAVERSAL.PY + BIPARTITE.PY")
    print("#" * 78)

    g, pos = demo_graph()
    demo_traversal(g, pos)
    demo_bipartite()

    section("HOAN TAT")
    print("Da xuat 5 hinh anh vao outputs/images/")


if __name__ == "__main__":
    main()