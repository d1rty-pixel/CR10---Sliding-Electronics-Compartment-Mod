# Run inside IngeTrazo via the MCP tool `run_python` (after ./venv/bin/python -I gen/newton_model.py):
#   exec(open("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/newton_import.py", encoding="utf-8").read())
# Sets the Newton extension data (mode, reference body, joint, limits, contact exemptions) of every top-level group from
# build/newton.json. Idempotent; run again after gen/ingetrazo_import.py, which recreates the generated groups with new IDs.
# Kinematic tree: outer slides static; middle slides slide on them, inner slides on the middle ones (each half the travel,
# all coupled to the near middle slide = the one drive); the drawer is welded to the near inner slide, every tray part to
# the drawer. Chains: link 01 hinges on the fixed bracket, each link on the previous one, the last link is pinned by a
# hinge connection to the moving bracket (closes the loop through the drawer). Lids are welded to their link.
# Everything else is "ignore" (shown, not simulated): the frame hulls would enclose the drawer, so there is no frame
# contact; the travel ends at the slide limits instead. Chain bodies do not touch anything in their lane.
# Before simulating: newton_view(True) (or newton_view(True, parts=True)) hides the unneeded groups, newton_view(False)
# shows them again; both stay defined in the run_python scope after the exec.
# Masses are assumptions (no weights known): drawer 2 kg, tray parts 0.1 kg, slide members 0.3 kg, link 10 g, lid 2 g.
import json
import math
from core.history import ExplodeGroupCommand
from core.group import world_mesh
from ingetrazo_plugin_newton.model import Configure, KEY, settings as _nt_settings
from ingetrazo_plugin_newton.worker import joint_settings, resolve_couplings
from ingetrazo_plugin_newton import axis_objects as _nt_axes

NEWTON_JSON = "/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/build/newton.json"
MASS = dict(drawer=2.0, part=0.1, slide=0.3, link=0.01, lid=0.002)


def _nt():
    d = json.load(open(NEWTON_JSON))
    # the near slide was one component (Outer/Middle/Inner as children); Newton moves only top-level groups
    for a in [g for g in groups if str(g.name) == "Auszugschiene" and g.children]:
        ExplodeGroupCommand(a).do(scene)
        for g in groups:
            if str(g.name).startswith("Slide Frame "):
                g.name = "Auszugschiene Nah " + str(g.name)[len("Slide Frame "):]

    def one(name):
        hit = [g for g in groups if str(g.name) == name]
        if len(hit) != 1:
            raise ValueError(f"{name}: {len(hit)} groups")
        return hit[0]

    def bbox(g):
        P = [v.position for v in world_mesh(g).vertices]
        return [min(p.x() for p in P) * 1e3, max(p.x() for p in P) * 1e3, min(p.y() for p in P) * 1e3,
                max(p.y() for p in P) * 1e3, min(p.z() for p in P) * 1e3, max(p.z() for p in P) * 1e3]

    def centre(g):
        b = bbox(g)
        return [(b[0] + b[1]) / 2000, (b[2] + b[3]) / 2000, (b[4] + b[5]) / 2000]

    bodies = [g for g in groups if not _nt_axes.owner_key(g)]
    cfg = {g.uid: dict(mode="ignore") for g in bodies}
    body = lambda mode, mass, shape="hull", **kw: dict(mode=mode, shape=shape, mass=mass, friction=.5, restitution=.1,
                                                       simulation_override=None, **kw)

    near_out, far_out = one(d["outer"][0]), one(d["outer"][1])
    near_mid, far_mid = one(d["middle"][0]), one(d["middle"][1])
    near_in, far_in = one(d["inner"][0]), one(d["inner"][1])
    drawer = one("Mod Frame Drawer")
    sl = d["slide"]
    stage = sl["stage_mm"] / 1000
    master = dict(type="slide", drive="position", name="Auszug (je Schienenstufe s/2)", parent=near_out.uid,
                  pivot=centre(near_mid), axis=sl["axis"], target=0.0, force=200.0, limited=True, lower=0.0,
                  upper=stage, max_speed=0.1, acceleration=0.5)
    follow = lambda g, parent, name: dict(type="slide", drive="free", name=name, parent=parent.uid, pivot=centre(g),
                                          axis=sl["axis"], force=0.0, limited=True, lower=0.0, upper=stage,
                                          coupling=dict(master=near_mid.uid, ratio=1.0))
    for g in (near_out, far_out):
        cfg[g.uid] = body("static", MASS["slide"], "box")
    cfg[near_mid.uid] = body("dynamic", MASS["slide"], "box", joint=joint_settings(master), reference=near_out.uid,
                             no_collision=[drawer.uid])
    cfg[near_in.uid] = body("dynamic", MASS["slide"], "box", joint=joint_settings(follow(near_in, near_mid, "Auszugschiene Nah Inner")),
                            reference=near_mid.uid, no_collision=[near_out.uid])
    cfg[far_mid.uid] = body("dynamic", MASS["slide"], "box", joint=joint_settings(follow(far_mid, far_out, "Auszugschiene Fern Middle")),
                            reference=far_out.uid, no_collision=[drawer.uid])
    cfg[far_in.uid] = body("dynamic", MASS["slide"], "box", joint=joint_settings(follow(far_in, far_mid, "Auszugschiene Fern Inner")),
                           reference=far_mid.uid, no_collision=[far_out.uid, drawer.uid])
    cfg[drawer.uid] = body("dynamic", MASS["drawer"], "compound", reference=near_in.uid)

    chain_names = {n for c in d["chains"] for l in c["links"] for n in (l["link"], l["lid"])}
    rails = {near_out, far_out, near_mid, far_mid, near_in, far_in}
    for g in bodies:
        n = str(g.name)
        if g is drawer or g in rails or n in chain_names:
            continue
        if any(n.startswith(t) for t in d["moving_tops"]) or g.layer in d["moving_layers"]:
            cfg[g.uid] = body("dynamic", MASS["part"], "box", reference=drawer.uid)

    for c in d["chains"]:
        fixed = one(c["fixed"])
        cfg[fixed.uid] = body("static", MASS["part"])
        parent = fixed
        for l in c["links"]:
            link, lid = one(l["link"]), one(l["lid"])
            j = dict(type="hinge", drive="free", name=f"{l['link']} Gelenk", parent=parent.uid,
                     pivot=[v / 1000 for v in l["pivot"]], axis=c["axis"], force=0.0, limited=True,
                     lower=math.radians(l["lower_deg"]), upper=math.radians(l["upper_deg"]), zero=None)
            cfg[link.uid] = body("dynamic", MASS["link"], joint=joint_settings(j), reference=parent.uid)
            cfg[lid.uid] = body("dynamic", MASS["lid"], reference=link.uid)
            parent = link
        cfg[parent.uid]["point_attachment"] = dict(type="hinge", target=one(c["moving"]).uid,
                                                   point=[v / 1000 for v in c["end"]], axis=c["axis"], span=.02)

    # chain bodies are exempt from every simulated body in their lane (+-5 mm): brackets, channel, ducts, slides, each
    # other. Only the links keep contact with the drawer: its profile carries the lower run, else the free loop sags.
    live = [g for g in bodies if cfg[g.uid]["mode"] != "ignore"]
    box_of = {g.uid: bbox(g) for g in live}
    for c, (y0, y1) in zip(d["chains"], d["lanes_y"]):
        lane = [g.uid for g in live if box_of[g.uid][2] < y1 + 5 and box_of[g.uid][3] > y0 - 5]
        for l in c["links"]:
            for n, keep in ((l["link"], {drawer.uid}), (l["lid"], set())):
                u = one(n).uid
                cfg[u]["no_collision"] = sorted(x for x in lane if x != u and x not in keep)

    resolve_couplings({u: v.get("joint") for u, v in cfg.items() if v.get("joint")})
    changed = 0
    for g in bodies:
        if (g.ext or {}).get(KEY) != cfg[g.uid]:
            Configure([g], cfg[g.uid]).do(scene)
            changed += 1
    sync = _nt_axes.plan(scene, _nt_axes.capture(scene), size=_nt_axes.gizmo_size)
    if sync:
        _nt_axes.ensure_axis_layer(scene)
        _nt_axes.SyncAxes(sync).do(scene)
    modes = {}
    for v in cfg.values():
        modes[v["mode"]] = modes.get(v["mode"], 0) + 1
    print(f"newton: {changed} groups configured, axis objects synced {len(sync)}, modes {modes}, "
          f"joints {sum(1 for v in cfg.values() if v.get('joint'))}")


def newton_view(on=True, parts=False):
    """Hide what the simulation does not need (the session copies and draws every visible group, which makes it slow).

    on: hide every "ignore" group; parts=True also the tray parts welded to the drawer (they still move as hidden
    bodies). Hidden here = flagged in ext, so newton_view(False) shows exactly those again, also after a reload."""
    drawer_uid = next(g.uid for g in groups if str(g.name) == "Mod Frame Drawer")
    n = 0
    for g in groups:
        if _nt_axes.owner_key(g):
            continue
        if on:
            s = _nt_settings(g)
            idle = s["mode"] == "ignore" or (parts and s.get("reference") == drawer_uid and not s.get("joint"))
            if idle and not g.hidden:
                g.hidden = True
                g.ext = dict(g.ext or {}, newton_view_hidden=True)
                n += 1
        elif (g.ext or {}).get("newton_view_hidden"):
            g.hidden = False
            g.ext = {k: v for k, v in g.ext.items() if k != "newton_view_hidden"}
            n += 1
    scene.version += 1
    viewport.update()
    print(f"newton_view({on}, parts={parts}): {n} groups {'hidden' if on else 'shown'}")


_nt()
