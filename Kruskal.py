from disjointset import DisjointSet
def kruskal(n, ds_canh):
    ds_canh.sort(key=lambda x: x[2])
    ds = DisjointSet(n)
    mst = []
    total_weight = 0
    for u, v, weight in ds_canh:
        if ds.find(u) != ds.find(v):
            mst.append((u, v, weight))
            ds.union(u, v)
            total_weight += weight
            if len(mst) == n - 1:
                break

    return mst, total_weight