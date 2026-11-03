import sys, json
seed, src_json, out_json, LW_ = int(sys.argv[1]), sys.argv[2], sys.argv[3], float(sys.argv[4])
sys.argv = ["x", str(seed)]
exec(open("/tmp/claude-1000/-home-equinox-git-private-Vodafone-Station-Rackmount/9a510f42-3b60-4339-95fb-862bcb43e163/scratchpad/wopt.py").read().split("order = list(T)")[0])
LW = LW_
prev = json.load(open(src_json))["pts"]
def inv(t, pts):
    x = []
    for p, q in zip(t, pts):
        for c, v in zip(p, q):
            if isinstance(c, tuple): x.append((v - c[1]) / (c[2] - c[1]))
    return np.clip(np.array(x), 0, 1)
def local(name, placed, x0, iters, sig0):
    n = len(x0); x = x0.copy(); c, m = cost(name, x, placed); sig = sig0
    for _ in range(iters):
        y = np.clip(x + rng.normal(0, sig, n), 0, 1); cy, my = cost(name, y, placed)
        if cy < c: x, c, m = y, cy, my; sig = min(0.3, sig * 1.3)
        else: sig = max(0.003, sig * 0.99)
    return c, x, m
order = ["230V PE Kette-WAGO", "230V N Kette-WAGO", "230V L Kette-WAGO", "230V PE WAGO-Tray", "230V PE WAGO-RS", "230V N WAGO-RS",
         "230V L WAGO-RS", "230V PE WAGO-LRS", "230V N WAGO-LRS", "230V L WAGO-LRS"]
X = {n: inv(T[n][0], prev[n]) for n in order}
LW = LW_
placed = {"sheath": W.tube(np.array([(sx, sy, sz), (sx, e, sz)]), W.SHEATH_D + CL)}
for n in order: placed[n] = cost(n, X[n], {})[1]
res = {}
for rnd in range(3):
    for n in order:
        others = {k: v for k, v in placed.items() if k != n}
        c0, _ = cost(n, X[n], others)
        best = local(n, others, X[n], 700, 0.05)
        if rnd == 0:                                   # also a fresh global try, keep the better one
            g = opt(n, others, iters=1200, starts=2)
            if g[0] < best[0]: best = g
        c, x, m = best
        if c <= c0: X[n], placed[n] = x, m
        res[n] = min(c, c0)
        print(rnd, f"{n:22s} {c0:8.2f} -> {res[n]:8.2f}", flush=True)
json.dump({"pts": {n: [[round(float(v), 2) for v in p] for p in build(T[n][0], X[n])] for n in order},
           "kink": {n: T[n][1] for n in order}, "cost": res}, open(out_json, "w"), indent=1)
