import json, sys
R = json.load(open(sys.argv[1]))
cond = lambda n: n.split()[1]
lines = ["ROUTES = {"]
for n, pts in R["pts"].items():
    lines.append(f'    "{n}": ("{cond(n)}", [' + ", ".join("(" + ", ".join(f"{v:.2f}" for v in p) + ")" for p in pts) + "]),")
lines.append("}")
lines.append("KINK = {" + ", ".join(f'"{n}": ({", ".join(map(str, k))},)' for n, k in R["kink"].items() if k) + "}")
print("\n".join(lines))
