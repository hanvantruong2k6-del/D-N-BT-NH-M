import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

DEFAULT_NODE_COLOR = "#a9c9ff"
HIGHLIGHT_NODE_COLOR = "#ffb703"
START_NODE_COLOR = "#38b000"
END_NODE_COLOR = "#d90429"
DEFAULT_EDGE_COLOR = "#888888"
HIGHLIGHT_EDGE_COLOR = "#e63946"
MST_EDGE_COLOR = "#2a9d8f"
FIGSIZE = (8, 6)


def _build_nx_graph(graph):
    """Chuyen doi tu Graph tu-cai-dat sang networkx CHI DE lay layout va ve."""
    G = nx.DiGraph() if graph.directed else nx.Graph()
    G.add_nodes_from(graph.vertices())
    for u, v, w in graph.edges():
        G.add_edge(u, v, weight=w)
    return G


def _normalize_edge_set(edge_list, directed):
    """Chuan hoa danh sach canh de so sanh (vo huong -> frozenset khong phan biet chieu)."""
    norm = set()
    for e in edge_list:
        u, v = e[0], e[1]
        norm.add((u, v) if directed else frozenset((u, v)))
    return norm


def _edge_in_set(u, v, edge_set, directed):
    key = (u, v) if directed else frozenset((u, v))
    return key in edge_set


def draw_graph(graph, filename, title="Do thi",
               pos=None,
               node_colors=None,
               highlighted_edges=None,
               edge_color_highlight=HIGHLIGHT_EDGE_COLOR,
               edge_labels=None,
               show_weight=True,
               node_order_labels=None,
               seed=42):
    """
    Ham ve do thi tong quat.
      node_colors        : dict dinh -> ma mau (mac dinh DEFAULT_NODE_COLOR)
      highlighted_edges   : list/set canh (u,v) can to dam (vd: cay BFS, MST, duong di ngan nhat)
      edge_labels         : dict (u,v) -> nhan tuy chinh (vd thu tu Euler, luong/capacity)
      node_order_labels    : dict dinh -> nhan phu (vd thu tu tham BFS/DFS: '1','2',...)
    Luu anh vao 'filename' (PNG).
    """
    G = _build_nx_graph(graph)
    if pos is None:
        pos = nx.spring_layout(G, seed=seed, k=1.1 / (len(G.nodes()) ** 0.4 + 0.1))

    plt.figure(figsize=FIGSIZE)

    colors = [node_colors.get(v, DEFAULT_NODE_COLOR) if node_colors else DEFAULT_NODE_COLOR
              for v in G.nodes()]

    highlight_set = _normalize_edge_set(highlighted_edges, graph.directed) if highlighted_edges else set()

    normal_edges = []
    bold_edges = []
    for u, v in G.edges():
        if _edge_in_set(u, v, highlight_set, graph.directed):
            bold_edges.append((u, v))
        else:
            normal_edges.append((u, v))

    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=900,
                            edgecolors="#333333", linewidths=1.2)
    nx.draw_networkx_labels(G, pos, font_size=11, font_weight="bold")

    if graph.directed:
        nx.draw_networkx_edges(G, pos, edgelist=normal_edges, edge_color=DEFAULT_EDGE_COLOR,
                                width=1.4, arrows=True, arrowstyle="-|>",
                                arrowsize=18, connectionstyle="arc3,rad=0.05")
        if bold_edges:
            nx.draw_networkx_edges(G, pos, edgelist=bold_edges, edge_color=edge_color_highlight,
                                    width=3.2, arrows=True, arrowstyle="-|>",
                                    arrowsize=22, connectionstyle="arc3,rad=0.05")
    else:
        nx.draw_networkx_edges(G, pos, edgelist=normal_edges, edge_color=DEFAULT_EDGE_COLOR,
                                width=1.4)
        if bold_edges:
            nx.draw_networkx_edges(G, pos, edgelist=bold_edges, edge_color=edge_color_highlight,
                                    width=3.2)

    # nhan trong so / nhan tuy chinh tren canh
    labels = {}
    if edge_labels:
        labels = edge_labels
    elif show_weight and graph.weighted:
        for u, v, w in graph.edges():
            labels[(u, v)] = str(w)
    if labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=9,
                                      font_color="#1d3557", label_pos=0.5)

    if node_order_labels:
        for v, lab in node_order_labels.items():
            x, y = pos[v]
            plt.text(x, y + 0.12, str(lab), fontsize=9, color="#6a040f",
                      ha="center", fontweight="bold")

    plt.title(title, fontsize=13, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.savefig(filename, dpi=150)
    plt.close()
    return pos


def draw_bipartite(graph, filename, title, color_map):
    """color_map: dict dinh -> 0/1 (2 tap bipartite), hoac None -> tat ca do (khong bipartite)."""
    node_colors = {}
    if color_map:
        for v, c in color_map.items():
            node_colors[v] = "#90e0ef" if c == 0 else "#f4a261"
    else:
        node_colors = {v: "#e63946" for v in graph.vertices()}
    return draw_graph(graph, filename, title=title, node_colors=node_colors)
