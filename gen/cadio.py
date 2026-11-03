"""Shared mesh I/O for the generator (taken over from the Lenovo Tab M10 project):
planar_faces() -> coplanar triangles merged into polygon faces with holes (IngeTrazo import),
write_stl()    -> binary STL."""
import math, struct
import numpy as np

def planar_faces(m):
    """merge coplanar triangles into polygon faces (outer loop + holes) for IngeTrazo"""
    mesh = m.to_mesh()
    V = np.asarray(mesh.vert_properties)[:, :3]
    T = np.asarray(mesh.tri_verts)
    # planes are matched with a tolerance (fixed rounding splits one plane into two faces -> T-junctions); sliver
    # triangles (collinear points, e.g. on sheared edges) have a random normal and join the face across their long edge
    tri_n, sliver = [], []
    for t in T:
        a, b, c = V[t[0]], V[t[1]], V[t[2]]
        n = np.cross(b - a, c - a); ln = np.linalg.norm(n)
        L = max(np.linalg.norm(b - a), np.linalg.norm(c - b), np.linalg.norm(a - c))
        sliver.append(ln / max(L, 1e-12) < 1e-3)                  # height of the triangle < 1 um
        tri_n.append((n / ln, float(np.dot(n / ln, a))) if ln > 0 else (None, 0.0))
    keys, key_of = [], [None] * len(T)
    for i, t in enumerate(T):
        if sliver[i]: continue
        n, d = tri_n[i]
        for k in keys:
            if abs(n[0] - k[0]) < 2e-4 and abs(n[1] - k[1]) < 2e-4 and abs(n[2] - k[2]) < 2e-4 and abs(d - k[3]) < 2e-3:
                break
        else:
            k = (float(n[0]), float(n[1]), float(n[2]), d); keys.append(k)
        key_of[i] = k
    owner = {}
    for i, t in enumerate(T):
        for j in range(3): owner[(int(t[j]), int(t[(j + 1) % 3]))] = i
    todo = [i for i in range(len(T)) if sliver[i]]
    for _ in range(10):                                           # slivers next to slivers: repeat
        rest = []
        for i in todo:
            t = T[i]; es = [(int(t[j]), int(t[(j + 1) % 3])) for j in range(3)]
            es.sort(key=lambda e: -np.linalg.norm(V[e[0]] - V[e[1]]))
            for e in es:
                o = owner.get((e[1], e[0]))
                if o is not None and key_of[o] is not None: key_of[i] = key_of[o]; break
            else: rest.append(i)
        todo = rest
        if not todo: break
    groups = {}
    for i, t in enumerate(T):
        if key_of[i] is not None: groups.setdefault(key_of[i], []).append(t)
    faces = []
    for key, tris in groups.items():
        n = np.array(key[:3]); n = n / np.linalg.norm(n)
        E = {}
        for t in tris:
            for i in range(3):
                e = (int(t[i]), int(t[(i + 1) % 3])); r = (e[1], e[0])
                if r in E: del E[r]
                else: E[e] = 1
        u = np.cross(n, [1, 0, 0]) if abs(n[0]) < 0.9 else np.cross(n, [0, 1, 0]); u /= np.linalg.norm(u)
        w = np.cross(n, u)
        P2 = lambda i: (float(np.dot(V[i], u)), float(np.dot(V[i], w)))
        out = {}
        for (a, b) in E: out.setdefault(a, []).append(b)
        used = set(); loops = []
        for e0 in list(E):
            if e0 in used: continue
            loop = [e0[0]]; cur = e0
            while True:
                used.add(cur); a, b = cur
                if b == loop[0]: break
                loop.append(b)
                cands = [q for q in out[b] if (b, q) not in used]
                if len(cands) > 1:
                    pa, pb = P2(a), P2(b); d0 = (pb[0] - pa[0], pb[1] - pa[1])
                    def turn(q):
                        pq = P2(q); d1 = (pq[0] - pb[0], pq[1] - pb[1])
                        return -math.atan2(d0[0] * d1[1] - d0[1] * d1[0], d0[0] * d1[0] + d0[1] * d1[1])
                    cands.sort(key=turn)
                cur = (b, cands[0])
            loops.append(loop)
        def area(L):
            pts = [P2(i) for i in L]
            return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts))) / 2
        def pip(pt, L):
            pts = [P2(i) for i in L]; x, y = pt; c = False
            for i in range(len(pts)):
                (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
            return c
        outs = [L for L in loops if area(L) > 0]; holes = [L for L in loops if area(L) <= 0]
        res = [[o, []] for o in outs]
        for h in holes:
            p0, p1 = P2(h[0]), P2(h[1]); mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]; ln = math.hypot(dx, dy) or 1
            test = (mid[0] - dy / ln * 1e-3, mid[1] + dx / ln * 1e-3)
            cand = [r for r in res if pip(test, r[0])] or res
            min(cand, key=lambda r: abs(area(r[0])))[1].append(h)
        for o, hs in res:
            faces.append({"n": [float(x) for x in n],
                          "outer": [[round(float(c), 5) for c in V[i]] for i in o],
                          "holes": [[[round(float(c), 5) for c in V[i]] for i in h] for h in hs]})
    return faces

def write_stl(m, path):
    mesh = m.to_mesh(); V = np.asarray(mesh.vert_properties)[:, :3]; T = np.asarray(mesh.tri_verts)
    with open(path, "wb") as f:
        f.write(b"\0" * 80); f.write(struct.pack("<I", len(T)))
        for t in T:
            a, b, c = V[t[0]], V[t[1]], V[t[2]]
            n = np.cross(b - a, c - a); ln = np.linalg.norm(n); n = n / ln if ln else n
            f.write(struct.pack("<12fH", *n, *a, *b, *c, 0))
