import sys, json
J = sys.argv[1]; sys.argv = ["x", "1"]
exec(open("/tmp/claude-1000/-home-equinox-git-private-Vodafone-Station-Rackmount/9a510f42-3b60-4339-95fb-862bcb43e163/scratchpad/wopt.py").read().split("order = list(T)")[0])
P = json.load(open(J))["pts"]
tub = {n: W.tube(fp(p)[0], W.CORE_D + CL) for n, p in P.items()}
tub["sheath"] = W.tube(np.array([(sx, sy, sz), (sx, e, sz)]), W.SHEATH_D + CL)
for n, p in P.items():
    path, radii, idx = fp(p); m = tub[n]
    ov = {k: round(200 * (m ^ v).volume(), 1) for k, v in tub.items() if k != n and (m ^ v).volume() > 1e-4}
    print(n, "obs", round(200 * (m ^ obs).volume(), 1), "wires", ov, "R", [round(float(r), 2) for r in radii])
