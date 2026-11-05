# Run inside IngeTrazo via the MCP tool `run_python`:
#   exec(open("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/doc_export.py", encoding="utf-8").read())
# Writes build/doc_scene.json: every group that has faces, as world triangles in mm, with its path (top-level / ... names),
# layer (inherited from the parent when unset) and top-level name. Hidden groups, everything below them and the layers
# "Archive" and "Newton Axes" are left out, except the real parts in KEEP_HIDDEN (hidden only for the view). Read-only.
# Used by gen/travel_sim.py (drawer travel and collisions against the document, T-006/T-007).
import json

SCENE_JSON = "/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/build/doc_scene.json"
KEEP_HIDDEN = ("Tray Frame/Tray Plexiglass Plate",)      # tray floor plate (material unknown), hidden in the document

def _export():
    # not by layer visibility: layers are hidden only to look at the model
    lay_vis = {str(l.name): str(l.name) not in ("Archive", "Newton Axes") for l in layers}
    out = []
    def walk(gs, M, path, top, lay):
        for g in gs:
            name = str(g.name); p = path + [name]; t = top or name; ly = g.layer or lay   # children without a layer inherit it
            if ((g.hidden and not (g.ext or {}).get("newton_view_hidden")) or not lay_vis.get(str(g.layer), True)) and "/".join(p) not in KEEP_HIDDEN: continue
            Mg = M if g.xform is None else (g.xform if M is None else M * g.xform)
            tris = []
            if g.mesh is not None:
                for f in g.mesh.faces:
                    for tri in f.triangulate():
                        pts = [v if Mg is None else Mg.map(v) for v in tri]
                        tris.append([[round(q.x() * 1000, 4), round(q.y() * 1000, 4), round(q.z() * 1000, 4)] for q in pts])
            if tris: out.append(dict(path="/".join(p), name=name, layer=str(ly), top=t, tris=tris))
            ch = getattr(g, "children", None)
            if ch: walk(ch, Mg, p, t, ly)
    walk(groups, None, [], None, None)
    with open(SCENE_JSON, "w") as fh: json.dump(out, fh)
    print("exported", len(out), "groups,", sum(len(d["tris"]) for d in out), "triangles")

try:
    _export()
except Exception as e:
    print("ERR", repr(e))
