# Run inside IngeTrazo via the MCP tool `run_python` (T-042):
#   exec(open("/home/equinox/git/private/Creality CR10 Sliding Electronics Compartment Mod/gen/organize_document.py", encoding="utf-8").read())
# Puts every hand-made and vendor group of the document on the final layers, gives it its English name (L = power-supply
# side, high Y; R = mainboard side, low Y; front = -X) and nests loose sub-parts. Old and duplicate objects were deleted
# by the user (2026-11-05); only the two unplaced groups stay on the hidden layer "Archive". Idempotent: groups are found
# by their old or new name.
# Generated parts get their layers from gen/cr10mod.py (re-import with gen/ingetrazo_import.py afterwards).
from core.layers import Layer

LAYERS = [("CR10", True), ("Mod Frame", True), ("Mod Frame Print Parts", True),
          ("Mod Frame Electrics", True), ("Drawer Rails", True), ("Tray Frame", True), ("Tray Electrics", True),
          ("Tray Print Parts", True), ("Drag Chains", True), ("Archive", False)]
KEEP_LAYERS = {"Layer 0", "Newton Axes"} | {n for n, _ in LAYERS}

# old top-level name -> (new name, layer); several groups with one old name are told apart by position (see SPLIT)
TOP = {
    "Stock Frame": ("CR10 Frame", "CR10"),
    "Gruppo#11": ("CR10 Bed", "CR10"),
    "Group#45": ("CR10 Plexiglass Cover Plate", "CR10"),
    "Mod Frame Base": ("Mod Frame Base", "Mod Frame"),
    "Mod Frame Drawer": ("Tray Frame", "Tray Frame"),
    "Auszugschiene Nah Outer": ("Drawer Rail R Outer", "Drawer Rails"),
    "Auszugschiene Nah Middle": ("Drawer Rail R Middle", "Drawer Rails"),
    "Auszugschiene Nah Inner": ("Drawer Rail R Inner", "Drawer Rails"),
    "Auszugschiene Fern Outer": ("Drawer Rail L Outer", "Drawer Rails"),
    "Auszugschiene Fern Middle": ("Drawer Rail L Middle", "Drawer Rails"),
    "Auszugschiene Fern Inner": ("Drawer Rail L Inner", "Drawer Rails"),
    "Group#60": ("Unplaced Print Parts", "Archive"),
    "Group#50": ("Unplaced Part", "Archive"),
    "PE Ringoese Tray (M5, 2020 L=410 #1, hinter Thin Bracket Moving)":
        ("PE Ring Terminal Tray (M5, 2020 L=410 #1, behind Thin Bracket Moving)", "Tray Electrics"),
    "PE Ringoese Rahmen (M5, Base hinten, Y 570 zwischen Bezel-Mounts)":
        ("PE Ring Terminal Frame (M5, base rear, Y 570 between bezel mounts)", "Mod Frame Electrics"),
    "Hutschiene R2 Logik (280 mm)": ("DIN Rail R1 Logic (280 mm)", "Tray Electrics"),
    "Hutschiene R1a Netz A (370 mm, LRS-350 + DC-Hub + RS-15)": ("DIN Rail L1 Mains A (370 mm, LRS-350 + DC hub + RS-15)", "Tray Electrics"),
    "Hutschiene R1b Netz B (370 mm, LRS-350 + Netz-Hub + RS-15)": ("DIN Rail L2 Mains B (370 mm, LRS-350 + mains hub + RS-15)", "Tray Electrics"),
    "WAGO 221-413 L (liegend, Hebel oben, Einfuehrung +Y)": ("WAGO 221-413 Line (lying, lever up, entry +Y)", "Tray Electrics"),
    "WAGO 221-413 N (liegend, Hebel oben, Einfuehrung +Y)": ("WAGO 221-413 Neutral (lying, lever up, entry +Y)", "Tray Electrics"),
    "WAGO 221-414 PE (liegend, Hebel oben, Einfuehrung +Y)": ("WAGO 221-414 PE (lying, lever up, entry +Y)", "Tray Electrics"),
    "PSU Mean Well LRS-350-24": ("PSU Mean Well LRS-350-24", "Tray Electrics"),
    "PSU Mean Well RS-15-5": ("PSU Mean Well RS-15-5", "Tray Electrics"),
    "Raspberry Pi 4 Model B": ("Raspberry Pi 4 Model B", "Tray Electrics"),
    "BTT Octopus (V1.0 STEP)": ("BTT Octopus (V1.0 STEP)", "Tray Electrics"),
    "IEC-GS-1-100 Kaltgeraetestecker mit Schalter und Sicherung": ("IEC-GS-1-100 Inlet with Switch and Fuse", "Mod Frame Electrics"),
}

# same old name, told apart by the world box centre (mm): (old name, axis, threshold, new name below, new name above, layer)
SPLIT = [("Stock Foot", None, None, None, None, "CR10"),
         ("Group#68", 0, 1400, "CR10 Bed Rail 1", "CR10 Bed Rail 2", "CR10"),
         ("1", None, None, None, None, "CR10")]

# loose sub-parts nested into one group: (container name, layer, [(old top name, new child name)])
NEST = [("GX16 Connector", "Mod Frame Electrics",
         [("GX16 Koerper", "Body"), ("GX16 Huelse", "Sleeve"), ("GX16 Flansch", "Flange"), ("GX16 Mutter", "Nut"),
          ("GX16 Einsatz", "Insert"), ("GX16 Pin", "Pin"), ("GX16 Pin", "Pin"), ("GX16 Pin", "Pin"), ("GX16 Pin", "Pin")]),
        ("Keystone RJ45", "Mod Frame Electrics",
         [("Keystone RJ45 Koerper", "Body"), ("Keystone RJ45 Blende", "Faceplate"), ("Keystone RJ45 Port", "Port")]),
        ("Keystone USB 1", "Mod Frame Electrics",
         [("Keystone USB 1 Koerper", "Body"), ("Keystone USB 1 Blende", "Faceplate"), ("Keystone USB 1 Port", "Port")]),
        ("Keystone USB 2", "Mod Frame Electrics",
         [("Keystone USB 2 Koerper", "Body"), ("Keystone USB 2 Blende", "Faceplate"), ("Keystone USB 2 Port", "Port")]),
        ("Keystone Blank", "Mod Frame Electrics", [("Keystone Blind Koerper", "Body"), ("Keystone Blind Blende", "Faceplate")])]
# a lever is nested into its terminal block: (new parent name, old lever name)
LEVERS = [("WAGO 221-413 Line (lying, lever up, entry +Y)", "WAGO 221-413 L Hebel"),
          ("WAGO 221-413 Neutral (lying, lever up, entry +Y)", "WAGO 221-413 N Hebel"),
          ("WAGO 221-414 PE (lying, lever up, entry +Y)", "WAGO 221-414 PE Hebel")]

# children: (container new name, old child name, occurrence, new name, layer or "" = inherit); occurrence counts from 0
CHILD = [("CR10 Frame", "Gruppieren#12", 0, "Bottom Plate", ""),
         ("CR10 Bed", "Gruppo#35", 0, "Bed Plate", ""), ("CR10 Bed", "Gruppo#77", 0, "Bed Carriage", ""),
         ("Tray Frame", "Gruppieren#15", 0, "Tray Plexiglass Plate", "")]


def _layer(name, visible):
    for l in layers:
        if l.name == name:
            return l
    l = Layer(name)
    l.visible = visible
    layers.append(l)
    return l


def _centre(g, axis):
    import ingetrazo_plugin_newton.model as _m
    p = _m.world_points(g)
    return (p[:, axis].min() + p[:, axis].max()) / 2 * 1000


def _box(g):
    import ingetrazo_plugin_newton.model as _m
    p = _m.world_points(g) * 1000
    return p.min(0), p.max(0)


def _organize():
    report = []
    for name, visible in LAYERS:
        _layer(name, visible)
    tops = {}
    for g in groups:
        tops.setdefault(str(g.name), []).append(g)
    new_names = {new for new, _ in TOP.values()}
    for old, (new, layer) in TOP.items():
        hit = tops.get(old, []) or tops.get(new, [])
        if len(hit) != 1:
            report.append(f"{old}: {len(hit)} groups")
            continue
        hit[0].name, hit[0].layer = new, layer
    # feet: R = low Y, L = high Y; front = low X
    for g in tops.get("Stock Foot", []) + [g for n, l in tops.items() if n.startswith("CR10 Foot ") for g in l]:
        lo, hi = _box(g)
        g.name = f"CR10 Foot {'R' if (lo[1] + hi[1]) / 2 < 459 else 'L'} {'Front' if (lo[0] + hi[0]) / 2 < 270 else 'Rear'}"
        g.layer = "CR10"
    rails = sorted(tops.get("Group#68", []) + [g for n, l in tops.items() if n.startswith("CR10 Bed Rail ") for g in l],
                   key=lambda g: _centre(g, 0))
    for k, g in enumerate(rails):
        g.name, g.layer = f"CR10 Bed Rail {k + 1}", "CR10"
    small = sorted(tops.get("1", []) + [g for n, l in tops.items() if n.startswith("CR10 Mechanics Part ") for g in l],
                   key=lambda g: (round(_centre(g, 1)), round(_centre(g, 2))))
    for k, g in enumerate(small):
        g.name, g.layer = f"CR10 Mechanics Part {k + 1}", "CR10"
    for k in range(1, 5):
        for g in [g for n, l in tops.items() if n.startswith((f"Luefter 60x60x25 #{k} (", f"Fan 60x60x25 #{k} (")) for g in l]:
            g.name = f"Fan 60x60x25 #{k} (San Ace 9LG0624P4H001, 24 V PWM, blows -X)"
            g.layer = "Tray Electrics"
    # the former single "Tray" layer: generated parts are print parts, everything else is named in TOP
    for g in groups:
        if g.layer == "Tray":
            if (g.ext or {}).get("cr10mod"):
                g.layer = "Tray Print Parts"
            else:
                report.append(f"{g.name}: still on layer Tray")
    # nest loose sub-parts
    for container, layer, parts in NEST:
        if any(str(g.name) == container for g in groups):
            continue
        kids = []
        for old, child in parts:
            g = next((g for g in groups if str(g.name) == old), None)
            if g is None:
                report.append(f"{container}: {old} missing")
                continue
            groups.remove(g)
            g.name, g.layer = child, None
            kids.append(g)
        if kids:
            c = Group(name=container)
            c.adopt(kids)
            c.layer, c.component = layer, False
            groups.append(c)
    for parent, lever in LEVERS:
        p = next((g for g in groups if str(g.name) == parent), None)
        lv = next((g for g in groups if str(g.name) == lever), None)
        if p is None or lv is None:
            continue
        groups.remove(lv)
        lv.name, lv.layer = "Lever", None
        p.adopt(list(p.children) + [lv])
    # children of the containers
    by = {str(g.name): g for g in groups}
    for top, old, k, new, layer in CHILD:
        t = by.get(top)
        if t is None:
            report.append(f"{top}: missing")
            continue
        hit = [c for c in t.children if str(c.name) in (old, new)]
        if len(hit) <= k:
            report.append(f"{top}/{old}: missing")
            continue
        hit[k].name = new
        hit[k].layer = layer or None
    motors = sorted([c for c in by["CR10 Frame"].children if str(c.name) in ("Group#4", "Motor Z R", "Motor Z L", "Motor Y")],
                    key=lambda c: (_centre_child(by["CR10 Frame"], c, 2) < 120, _centre_child(by["CR10 Frame"], c, 1)))
    for c, n in zip(motors, ("Motor Z R", "Motor Z L", "Motor Y")):
        c.name, c.layer = n, None
    for c in by["CR10 Bed"].children:
        if str(c.name) in ("Gruppo#124", "Gruppo#125"):
            c.name = "Bed Corner Mount"
    # every remaining child layer that is going away falls back to its parent's layer
    from core.group import iter_placements
    for t in groups:
        for c, _ in iter_placements(t):
            if c is not t and c.layer and c.layer not in KEEP_LAYERS:
                c.layer = None
    # old layers that no group uses any more
    used = {g.layer for t in groups for g, _ in iter_placements(t)}
    for l in [l for l in layers if l.name not in KEEP_LAYERS]:
        if l.name in used:
            report.append(f"layer {l.name} still used")
        else:
            layers.remove(l)
    scene.version += 1
    viewport.update()
    print("organize:", report or "ok", "| layers", [l.name for l in layers])


def _centre_child(top, c, axis):
    import ingetrazo_plugin_newton.model as _m
    p = _m.world_points(c, top.xform)
    return (p[:, axis].min() + p[:, axis].max()) / 2 * 1000


_organize()
