from collections import OrderedDict


class Graph:
    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted
        # adjacency list: OrderedDict giu thu tu chen dinh -> giup ket qua deterministic
        self._adj = OrderedDict()   # vertex -> list of (neighbor, weight)

    # ---------------------------------------------------------------
    # Xay dung do thi
    # ---------------------------------------------------------------
    def add_vertex(self, v):
        if v not in self._adj:
            self._adj[v] = []

    def add_edge(self, u, v, weight=1):
        self.add_vertex(u)
        self.add_vertex(v)
        w = weight if self.weighted else 1
        self._adj[u].append((v, w))
        if not self.directed:
            self._adj[v].append((u, w))

    # ---------------------------------------------------------------
    # Truy van co ban
    # ---------------------------------------------------------------
    def vertices(self):
        return list(self._adj.keys())

    def num_vertices(self):
        return len(self._adj)

    def num_edges(self):
        total = sum(len(lst) for lst in self._adj.values())
        return total if self.directed else total // 2

    def neighbors(self, v):
        """Tra ve danh sach (dinh_ke, trong_so)."""
        return list(self._adj.get(v, []))

    def has_vertex(self, v):
        return v in self._adj

    def has_edge(self, u, v):
        return any(nb == v for nb, _w in self._adj.get(u, []))

    def edge_weight(self, u, v):
        for nb, w in self._adj.get(u, []):
            if nb == v:
                return w
        return None

    def degree(self, v):
        """Bac cua dinh (chi dung cho do thi vo huong)."""
        return len(self._adj.get(v, []))

    def in_out_degree(self, v):
        """Bac vao / bac ra (dung cho do thi co huong)."""
        out_deg = len(self._adj.get(v, []))
        in_deg = 0
        for u in self._adj:
            for nb, _w in self._adj[u]:
                if nb == v:
                    in_deg += 1
        return in_deg, out_deg

    def edges(self):
        """Danh sach canh dang (u, v, w). Voi do thi vo huong, moi canh chi lay 1 lan (u<=v theo thu tu xuat hien)."""
        result = []
        seen = set()
        for u in self._adj:
            for v, w in self._adj[u]:
                if self.directed:
                    result.append((u, v, w))
                else:
                    key = frozenset((u, v)) if u != v else (u, v)
                    if key in seen:
                        continue
                    seen.add(key)
                    result.append((u, v, w))
        return result

    def copy(self):
        g = Graph(directed=self.directed, weighted=self.weighted)
        for v in self._adj:
            g.add_vertex(v)
        for u in self._adj:
            for v, w in self._adj[u]:
                g._adj[u].append((v, w))
        return g

    # ---------------------------------------------------------------
    # 3 cach bieu dien: Adjacency List / Adjacency Matrix / Edge List
    # ---------------------------------------------------------------
    def to_adjacency_list(self):
        """Tra ve dict: dinh -> [(dinh_ke, trong_so), ...]"""
        return OrderedDict((u, list(self._adj[u])) for u in self._adj)

    def to_adjacency_matrix(self):
        """Tra ve (danh_sach_dinh, ma_tran vuong NxN). O [i][j] = trong so canh i->j, hoac None neu khong co canh."""
        verts = self.vertices()
        idx = {v: i for i, v in enumerate(verts)}
        n = len(verts)
        matrix = [[None for _ in range(n)] for _ in range(n)]
        for u in self._adj:
            for v, w in self._adj[u]:
                matrix[idx[u]][idx[v]] = w
        return verts, matrix

    def to_edge_list(self):
        """Tra ve danh sach canh (u, v, w)."""
        return self.edges()

    @staticmethod
    def from_adjacency_matrix(vertices, matrix, directed=False, weighted=False):
        g = Graph(directed=directed, weighted=weighted)
        for v in vertices:
            g.add_vertex(v)
        n = len(vertices)
        added = set()
        for i in range(n):
            for j in range(n):
                if matrix[i][j] is not None:
                    if directed:
                        g._adj[vertices[i]].append((vertices[j], matrix[i][j]))
                    else:
                        key = frozenset((i, j))
                        if key in added:
                            continue
                        added.add(key)
                        g.add_edge(vertices[i], vertices[j], matrix[i][j])
        return g

    @staticmethod
    def from_edge_list(vertices, edge_list, directed=False, weighted=False):
        g = Graph(directed=directed, weighted=weighted)
        for v in vertices:
            g.add_vertex(v)
        for e in edge_list:
            if len(e) == 3:
                u, v, w = e
            else:
                u, v = e
                w = 1
            g.add_edge(u, v, w)
        return g

    # ---------------------------------------------------------------
    # In cac bieu dien ra man hinh (dung cho doi chieu / bao cao)
    # ---------------------------------------------------------------
    def print_adjacency_list(self):
        print("== ADJACENCY LIST ==")
        for u in self._adj:
            parts = [f"{v}({w})" if self.weighted else f"{v}" for v, w in self._adj[u]]
            print(f"  {u}: [{', '.join(parts)}]")

    def print_adjacency_matrix(self):
        verts, matrix = self.to_adjacency_matrix()
        print("== ADJACENCY MATRIX ==")
        header = "      " + " ".join(f"{v:>4}" for v in verts)
        print(header)
        for i, v in enumerate(verts):
            row = []
            for j in range(len(verts)):
                val = matrix[i][j]
                row.append(f"{val:>4}" if val is not None else "   .")
            print(f"  {v:>3} " + " ".join(row))

    def print_edge_list(self):
        print("== EDGE LIST ==")
        for u, v, w in self.edges():
            arrow = "->" if self.directed else "--"
            if self.weighted:
                print(f"  {u} {arrow} {v}   (w={w})")
            else:
                print(f"  {u} {arrow} {v}")

    def summary(self):
        kind = "co huong" if self.directed else "vo huong"
        wkind = "co trong so" if self.weighted else "khong trong so"
        return (f"Do thi {kind}, {wkind} | so dinh = {self.num_vertices()} | "
                f"so canh = {self.num_edges()}")

    # ---------------------------------------------------------------
    # Doc tu file dinh dang tu dinh nghia (khong dung thu vien do thi)
    # ---------------------------------------------------------------
    @staticmethod
    def load_from_file(path):
        directed = False
        weighted = False
        vertices = []
        edges_section = False
        edges_raw = []

        with open(path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.upper().startswith("DIRECTED:"):
                    directed = line.split(":", 1)[1].strip().lower() in ("yes", "true", "1")
                    edges_section = False
                elif line.upper().startswith("WEIGHTED:"):
                    weighted = line.split(":", 1)[1].strip().lower() in ("yes", "true", "1")
                    edges_section = False
                elif line.upper().startswith("VERTICES:"):
                    vlist = line.split(":", 1)[1].strip()
                    vertices = [x.strip() for x in vlist.split(",") if x.strip()]
                    edges_section = False
                elif line.upper().startswith("EDGES:"):
                    edges_section = True
                elif edges_section:
                    tokens = line.split()
                    if len(tokens) >= 2:
                        u, v = tokens[0], tokens[1]
                        w = float(tokens[2]) if len(tokens) >= 3 else 1
                        if w == int(w):
                            w = int(w)
                        edges_raw.append((u, v, w))

        g = Graph(directed=directed, weighted=weighted)
        for v in vertices:
            g.add_vertex(v)
        for u, v, w in edges_raw:
            g.add_edge(u, v, w)
        return g

    def save_to_file(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"DIRECTED: {'yes' if self.directed else 'no'}\n")
            f.write(f"WEIGHTED: {'yes' if self.weighted else 'no'}\n")
            f.write(f"VERTICES: {','.join(self.vertices())}\n")
            f.write("EDGES:\n")
            for u, v, w in self.edges():
                if self.weighted:
                    f.write(f"{u} {v} {w}\n")
                else:
                    f.write(f"{u} {v}\n")
