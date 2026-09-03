# -*- coding: utf-8 -*-
"""
traversal.py
------------
Duyet do thi bang BFS va DFS - tu cai dat bang hang doi / ngan xep thu cong,
KHONG dung ham duyet co san cua bat ky thu vien do thi nao.
"""

from collections import deque


def bfs(graph, start):
    """
    Breadth-First Search tu dinh 'start'.
    Tra ve:
      order      : thu tu cac dinh duoc THAM (visit) - danh cho doi chieu bai lam tay
      parent     : dict dinh -> dinh cha trong cay BFS (None neu la goc/khong toi duoc)
      distance   : dict dinh -> so canh (khong trong so) tu start toi dinh do
      tree_edges : danh sach canh (u, v) thuoc cay BFS
    """
    if not graph.has_vertex(start):
        raise ValueError(f"Dinh '{start}' khong ton tai trong do thi")

    visited = {start}
    order = [start]
    parent = {start: None}
    distance = {start: 0}
    tree_edges = []

    queue = deque([start])
    while queue:
        u = queue.popleft()
        # duyet lang gieng theo thu tu duoc luu (deterministic) de de doi chieu tay
        for v, _w in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                parent[v] = u
                distance[v] = distance[u] + 1
                tree_edges.append((u, v))
                order.append(v)
                queue.append(v)

    return {
        "order": order,
        "parent": parent,
        "distance": distance,
        "tree_edges": tree_edges,
    }


def dfs(graph, start):
    """
    Depth-First Search tu dinh 'start' (cai dat kieu lap - iterative - de tranh
    gioi han do sau de quy, nhung mo phong dung thu tu de quy chuan).
    Tra ve:
      order        : thu tu THAM cac dinh (tien tu - preorder)
      parent       : dict dinh -> dinh cha trong cay/rung DFS
      discovery    : dict dinh -> thoi diem phat hien (tick)
      finish       : dict dinh -> thoi diem hoan tat (tick)
      tree_edges   : danh sach canh cay DFS
      back_edges   : danh sach canh nguoc (bao chu trinh) phat hien duoc
    """
    if not graph.has_vertex(start):
        raise ValueError(f"Dinh '{start}' khong ton tai trong do thi")

    visited = set()
    order = []
    parent = {start: None}
    discovery = {}
    finish = {}
    tree_edges = []
    back_edges = []
    on_stack = set()
    time_counter = [0]

    def visit(u):
        time_counter[0] += 1
        discovery[u] = time_counter[0]
        visited.add(u)
        on_stack.add(u)
        order.append(u)
        for v, _w in graph.neighbors(u):
            if v not in visited:
                parent[v] = u
                tree_edges.append((u, v))
                visit(v)
            elif v in on_stack and v != parent.get(u):
                # canh nguoc (huong ve to tien dang xu ly) => chu trinh
                if (u, v) not in back_edges and (v, u) not in back_edges:
                    back_edges.append((u, v))
        on_stack.discard(u)
        time_counter[0] += 1
        finish[u] = time_counter[0]

    visit(start)

    return {
        "order": order,
        "parent": parent,
        "discovery": discovery,
        "finish": finish,
        "tree_edges": tree_edges,
        "back_edges": back_edges,
    }


def connected_components_undirected(graph):
    """Tim cac thanh phan lien thong (danh cho do thi vo huong) bang BFS lap lai."""
    visited = set()
    components = []
    for v in graph.vertices():
        if v not in visited:
            comp = bfs(graph, v)["order"]
            visited.update(comp)
            components.append(comp)
    return components
