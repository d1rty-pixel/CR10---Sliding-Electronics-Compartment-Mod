"""Creality CR10 sliding electronics compartment mod - parametric generator (printed parts).

Usage:
    python cr10mod.py <outdir>            -> <outdir>/parts.json (assembled, for IngeTrazo) + <outdir>/stl/*.stl (print orientation)
    python cr10mod.py <outdir> --check    -> additionally runs fit checks

Coordinates (mm) = IngeTrazo document x 1000:
    x  drawer travel (red axis); the drawer slides out towards -x. Rear face of the frame x 515..535, drawer front x -399
    y  across; frame outer edges y 258..658, cells y 278..438 and 478..638 (160 wide), centre post y 438..478
    z  up; cell z 25..105 (CELL_H = 80), centre ZC = 65
Local part frame ("print frame"): u, v across the face, h from the OUTER face inwards (h = 0 lies on the bed).
Stage 1 = printed cover parts only (bezels, plugs, hex side panels, shared cover mount). Frame, drawer and slide rails follow.
"""
import json, math, os, sys
import numpy as np
from manifold3d import Manifold, CrossSection, JoinType, Mesh

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cadio import planar_faces, write_stl
import cable
import cable_thin as thin
import tray
import wiring

# ============================================================ frame (measured, see docs/DESIGN.md)
CELL_H = 80.0
Z0, Z1 = 25.0, 105.0
ZC = (Z0 + Z1) / 2
CELL_W = 160.0
REAR_X_OUT = 534.7            # outer face of the rear plates
FRONT_X_OUT = -399.0          # outer face of the drawer front plates
DRAWER_FRONT_IN = -383.0      # inner face of the drawer front plates (document)
CELL_YC = {"left": 358.0, "right": 558.0}
SIDE_Y_NEAR, SIDE_Y_FAR = 258.0, 658.0
SIDE_X0 = {"a": 55.0, "b": 295.0}   # panel start x, both panels 200 long
SIDE_LEN = 200.0

# ============================================================ printed parts
FIT = 0.2                     # clearance per side (IEC cut-out)
PANEL_W, PANEL_H, PANEL_T = SIDE_LEN - 0.5, CELL_H - 0.5, 3.0
FRONT_PANEL_W = CELL_W - 0.5           # front hex panel, same rim/grid as the side panels
PANEL_RIM = 5.0                       # frame around the hex field (as on the original panels)
GRID_T = 2.0                          # hex web thickness (original grille insert)
# honeycomb of the original grille: flat-top holes, across flats 17.32, rounded corners, pitch 19.4 (web 2.1)
HEX_AF, HEX_RC, HEX_PITCH = 17.32, 1.7, 19.4
FAN60 = dict(hole=57.0, screw=3.4, pitch=50.0)
# Adam Tech IEC-GS-1-100 (data sheet rev C): cut-out 47.0 (+0.4) x 27.8, R 2, panel 1.0; body 46.3 x 27.5, hooks reach +-15.3 across
IEC_CUT = (47.0, 27.8, 2.0)
IEC_WALL = 1.0
IEC_RECESS = (53.0, 34.0)             # behind the wall: body + hook travel
IEC_U = 4.6                           # same centre as the old switch hole (y 553.4)
GX16 = 16.2
KEY = (14.6, 19.2)                    # keystone cut-out (across x up)
SEG = 24
# shared cover mount: exact copy of the original "Side Cover - Mount" (layer Print Parts), data/side_cover_mount.json;
# placements = the four clips of the original rear plate in the part frame (u across, v up, h inwards)
HERE = os.path.dirname(os.path.abspath(__file__))
MT_ROOT_FIX = -0.3          # original rear plate outer face was x 535.0, the document's ring is 534.7
MT_OVERLAP = 0.5            # clip root sunk into the part so that it fuses (the original clips were separate parts)
MT_SIDE_SHIFT = 20.0        # side panels: tabs 20 mm further out than on the bezels (+-60 instead of +-40)


def rrect(w, h, r, n=8):
    return CrossSection.square((w - 2 * r, h - 2 * r), True).offset(r, JoinType.Round, 2.0, n)

def circle(d, seg=SEG):
    return CrossSection.circle(d / 2, seg)

def at(cs, u, v):
    return cs.translate((u, v))

def plate(cs, t, h0=0.0):
    return Manifold.extrude(cs, t).translate([0, 0, h0])

HEX_SHIFT = (4.0, 0.0)    # lattice offset found by search: no cut hex leaves a sliver under 0.1 mm (IngeTrazo merges them)
FRONT_HEX_SHIFT = (0.0, 0.0)   # same search for the 159.5 wide front panel: centred lattice is free of slivers

def honeycomb(w, h, exclude=None, min_area=15.0, shift=None):
    """holes of the original honeycomb clipped to a w x h window centred on 0 (cut hexes at the border like the original)"""
    sh = HEX_SHIFT if shift is None else shift
    ap = HEX_AF / 2 - HEX_RC
    R = ap / math.cos(math.radians(30))
    hexcs = CrossSection([np.array([(R * math.cos(math.radians(60 * k)), R * math.sin(math.radians(60 * k))) for k in range(6)])]).offset(HEX_RC, JoinType.Round, 2.0, 6)
    win = CrossSection.square((w, h), True)
    dx = HEX_PITCH * math.sqrt(3) / 2
    cells = []
    nc = int(w / 2 / dx) + 2; nr = int(h / 2 / HEX_PITCH) + 2
    for c in range(-nc, nc + 1):
        for r in range(-nr, nr + 1):
            x = c * dx + sh[0]; y = r * HEX_PITCH + (HEX_PITCH / 2 if c % 2 else 0) + sh[1]
            if exclude and exclude(x, y): continue
            piece = hexcs.translate((x, y)) ^ win
            if piece.area() >= min_area: cells.append(piece)
    return CrossSection.compose(cells)

# ---- shared cover mount (one component, flanged onto every cover part) -------------------------
def _legacy_mount():
    d = json.load(open(os.path.join(HERE, "data", "side_cover_mount.json")))
    T3 = np.array(d["tris"], dtype=np.float64).reshape(-1, 3)
    uniq, inv = np.unique(np.round(T3, 3), axis=0, return_inverse=True)
    tri = inv.reshape(-1, 3)
    m = Manifold(Mesh(vert_properties=uniq.astype(np.float32), tri_verts=tri.astype(np.uint32)))
    if m.volume() < 0:
        m = Manifold(Mesh(vert_properties=uniq.astype(np.float32), tri_verts=tri[:, ::-1].astype(np.uint32)))
    return m, d["placements"]

_MOUNT = None
def cover_mount():
    global _MOUNT
    if _MOUNT is None: _MOUNT = _legacy_mount()
    return _MOUNT

def mount_in_part(i, kind):
    """clip i of the original plate in the part frame; kind 'side' moves the tabs further out along u"""
    m, plc = cover_mount(); p = plc[i]
    lin = np.array(p["lin"]); t = np.array(p["t"], dtype=float)
    t[2] += MT_ROOT_FIX - MT_OVERLAP
    if kind == "side": t[0] += MT_SIDE_SHIFT * (1 if t[0] > 0 else -1)
    return m.transform(np.hstack([lin, t.reshape(3, 1)]))

def with_mounts(part, kind, t_part=None):
    for i in range(4):
        part = part + mount_in_part(i, kind)
    return part

# ---- local-frame parts ------------------------------------------------------------
def lbox(u0, u1, v0, v1, h0, h1):
    return Manifold.cube([u1 - u0, v1 - v0, h1 - h0]).translate([u0, v0, h0])

def cyl_h(u, v, h0, h1, d, seg=SEG):
    return Manifold.cylinder(h1 - h0, d / 2, d / 2, seg).translate([u, v, h0])

def hex_exclude(uc, vc, hu, hv):
    """drop every hex whose bounding box touches the rectangle uc +- hu, vc +- hv (no hex is cut, so no new slivers)"""
    ex, ey = HEX_AF / 2 / math.cos(math.radians(30)), HEX_AF / 2
    return lambda x, y: abs(x - uc) < hu + ex and abs(y - vc) < hv + ey

# ---- rear panels (T-026): bezel ring + plug merged into one hex panel per cell, mounts as before (+-40) ----
# Switch side: solid pad around the IEC (1.0 wall at the hooks), 4 countersunk M3 for the separate red IEC Housing.
REAR_PAD = (40.0, 22.0)               # half sizes of the solid pad around the IEC (covers housing + ears)
HS_IN = (55.0, 36.0)                  # housing inside (u x v): IEC_RECESS 53 x 34 + 1 per side
HS_WALL = 2.5
HS_BACK_X = 484.0                     # outer face of the housing back wall; retracted fan holders + M4 nuts end at x 461.4
HS_EAR = (8.0, 9.0, 9.0)              # ear: out of the wall (u), width (v), height (h)
HS_SCREW_V = 12.0                     # screws at u = IEC_U +- (wall + ear/2), v = +-12
INSERT = (4.0, 7.0)                   # heat-set insert M3 x 5.7: hole d, depth (assumption)
CSK = (3.4, 6.6)                      # M3 countersunk: shank hole / head d (90 deg)
SHEATH_HOLE, SHEATH_V = 8.0, 8.0      # 230 V sheath 7.3 (wiring.SHEATH_D) through the back wall
TIE_SLOT, TIE_DU = (2.0, 4.5), 7.5    # cable tie slots beside the sheath hole (strain relief)
PE_HOLE, PE_Y, PE_X = 4.5, 570.0, 519.0   # PE lead through the bottom wall, straight down to the frame eye (x 507..531, y 564..576)
# Connector side: solid band 2 (keystones like the old 2 mm sheet) with a 3 mm rim, GX16 + 4 keystones as before
CON_BAND = (-66.3, 63.0, 14.0)        # u0, u1, half height v
CON_RIM = 2.0

def _hs_geom():
    ou, ov = HS_IN[0] / 2 + HS_WALL, HS_IN[1] / 2 + HS_WALL
    ub = ou + HS_EAR[0] / 2
    screws = [(IEC_U + su * ub, sv * HS_SCREW_V) for su in (-1, 1) for sv in (-1, 1)]
    return ou, ov, screws

def switch_panel():
    ou, ov, screws = _hs_geom()
    pad = at(rrect(2 * REAR_PAD[0], 2 * REAR_PAD[1], 2.0), IEC_U, 0.0)
    cut = plate(at(rrect(IEC_CUT[0] + 2 * FIT, IEC_CUT[1] + 2 * FIT, IEC_CUT[2]), IEC_U, 0.0), PANEL_T + 2, -1.0)
    cut = cut + plate(at(rrect(*IEC_RECESS, 3.0), IEC_U, 0.0), PANEL_T, IEC_WALL)
    for u, v in screws:
        r0, r1 = CSK[0] / 2, CSK[1] / 2
        prof = [(0, -1.0), (r1, -1.0), (r1, 0.0), (r0, r1 - r0), (r0, PANEL_T + 1), (0, PANEL_T + 1)]
        cut = cut + Manifold.revolve(CrossSection([np.array(prof)]), 24).rotate([0, 0, 7.5]).translate([u, v, 0.0])   # shank + 90 deg countersink in one solid; half-segment turn avoids a sliver
    return hex_panel(FRONT_PANEL_W, "bezel", shift=FRONT_HEX_SHIFT, exclude=hex_exclude(IEC_U, 0.0, *REAR_PAD),
                     solid=plate(pad, PANEL_T), cut=cut)

def connector_panel():
    u0, u1, hv = CON_BAND
    band = at(rrect(u1 - u0, 2 * hv, 2.0), (u0 + u1) / 2, 0.0)
    inner = at(CrossSection.square((u1 - u0 - 2 * CON_RIM, 2 * hv - 2 * CON_RIM), True), (u0 + u1) / 2, 0.0)
    solid = plate(band, GRID_T) + plate(band - inner, PANEL_T)
    holes = [at(circle(GX16), 50.0, 0.0)] + [at(CrossSection.square(KEY, True), u, 0.0) for u in (17.0, -7.0, -31.0, -55.0)]
    cut = plate(CrossSection.compose(holes), PANEL_T + 2, -1.0)
    return hex_panel(FRONT_PANEL_W, "bezel", shift=FRONT_HEX_SHIFT, exclude=hex_exclude((u0 + u1) / 2, 0.0, (u1 - u0) / 2, hv),
                     solid=solid, cut=cut)

def iec_housing():
    """red touch guard behind the IEC: open towards the panel, ears with inserts (screws from outside through the panel).
    Print frame = panel frame (u, v, h); STL is printed standing on the back wall, ears carried by 45 deg gussets."""
    ou, ov, screws = _hs_geom()
    h0, hb = PANEL_T, REAR_X_OUT - HS_BACK_X
    iu, iv = HS_IN[0] / 2, HS_IN[1] / 2
    m = lbox(IEC_U - ou, IEC_U + ou, -ov, ov, h0, hb)
    for u, v in screws:
        s = 1 if u > IEC_U else -1
        w0, w1 = IEC_U + s * ou, IEC_U + s * (ou + HS_EAR[0])
        ear = lbox(min(w0, w1), max(w0, w1), v - HS_EAR[1] / 2, v + HS_EAR[1] / 2, h0, h0 + HS_EAR[2])
        strip = lbox(min(w0, w0 - s * 0.5), max(w0, w0 - s * 0.5), v - HS_EAR[1] / 2, v + HS_EAR[1] / 2, h0, h0 + HS_EAR[2] + HS_EAR[0])
        m = m + (ear + strip).hull()
    m = m - lbox(IEC_U - iu, IEC_U + iu, -iv, iv, h0 - 1, hb - HS_WALL)
    for u, v in screws: m = m - cyl_h(u, v, h0 - 1, h0 + INSERT[1], INSERT[0], 16)
    m = m - cyl_h(IEC_U, SHEATH_V, hb - HS_WALL - 1, hb + 1, SHEATH_HOLE, 32)
    for du in (-TIE_DU, TIE_DU):
        u = IEC_U + du
        m = m - lbox(u - TIE_SLOT[0] / 2, u + TIE_SLOT[0] / 2, SHEATH_V - TIE_SLOT[1] / 2, SHEATH_V + TIE_SLOT[1] / 2, hb - HS_WALL - 1, hb + 1)
    pu, ph = CELL_YC["right"] - PE_Y, REAR_X_OUT - PE_X
    pe = Manifold.cylinder(HS_WALL + 2, PE_HOLE / 2, PE_HOLE / 2, 16).rotate([90, 0, 0]).translate([pu, -iv + 1, ph])
    return m - pe

def hex_panel(w, kind, fan=False, shift=None, exclude=None, solid=None, cut=None):
    """cover panel: PANEL_RIM frame around a hex field (one code for side, front and rear panels);
    exclude drops hexes, solid is added and cut removed afterwards (rear panels)"""
    ww, wh = w - 2 * PANEL_RIM, PANEL_H - 2 * PANEL_RIM
    ex = (lambda x, y: math.hypot(x, y) < 48.0) if fan else exclude
    frame = plate(rrect(w, PANEL_H, 1.0) - CrossSection.square((ww - 1.0, wh - 1.0), True), PANEL_T)   # 0.5 mm overlap with the grid
    grid = plate(CrossSection.square((ww, wh), True) - honeycomb(ww, wh, ex, shift=shift), GRID_T)
    p = frame + grid
    if solid is not None: p = p + solid
    if cut is not None: p = p - cut
    if fan:
        cutter = plate(circle(FAN60["hole"], 48), PANEL_T + 2, -1.0)
        for sx in (-1, 1):
            for sy in (-1, 1): cutter = cutter + plate(at(circle(FAN60["screw"], 12), sx * FAN60["pitch"] / 2, sy * FAN60["pitch"] / 2), PANEL_T + 2, -1.0)
        p = p - cutter
    return with_mounts(p, kind, PANEL_T)

def side_panel(fan=False):
    return hex_panel(PANEL_W, "side", fan)

def front_panel():
    # replaces bezel ring + front grille at the drawer front; tabs at the bezel positions (+-40)
    return hex_panel(FRONT_PANEL_W, "bezel", shift=FRONT_HEX_SHIFT)

# ---- placement: (u, v, h) -> world, rotations only ------------------------------------
def rot(m, f):
    return m.warp_batch(lambda p: np.stack(f(p[:, 0], p[:, 1], p[:, 2]), axis=1))

def place_rear(m, yc, xout=REAR_X_OUT):  return rot(m, lambda u, v, h: (xout - h, yc - u, ZC + v))
def place_front(m, yc, xout=FRONT_X_OUT): return rot(m, lambda u, v, h: (xout + h, yc + u, ZC + v))
def place_side_near(m, xc): return rot(m, lambda u, v, h: (xc - u, SIDE_Y_NEAR + h, ZC + v))
def place_side_far(m, xc):  return rot(m, lambda u, v, h: (xc + u, SIDE_Y_FAR - h, ZC + v))

# ============================================================ parts list
LAYER = "Druckteile (gen)"
COL = (0.95, 0.5, 0.05)
CHAIN_LAYER = "Schlepp (gen)"
CHAIN_COL = (0.2, 0.5, 0.85)
TRAY_LAYER = "Tray Druckteile (gen)"   # colour = filament: red 230 V, yellow 24/5 V, green data/bus, dark grey DIN holders

def parts():
    sw, cn, hs, fp = switch_panel(), connector_panel(), iec_housing(), front_panel()
    sp, spf = side_panel(False), side_panel(True)
    local = dict([("Rear Panel Switch", sw), ("Rear Panel Connector", cn), ("IEC Housing", hs.mirror([0, 0, 1])),
                  ("Front Panel Hex", fp), ("Side Panel Hex", sp), ("Side Panel Fan60", spf)])
    inst = [("Rear Panel Switch", place_rear(sw, CELL_YC["right"])), ("Rear Panel Connector", place_rear(cn, CELL_YC["left"])),
            ("IEC Housing", place_rear(hs, CELL_YC["right"])),
            ("Front Panel Left", place_front(fp, CELL_YC["left"])), ("Front Panel Right", place_front(fp, CELL_YC["right"]))]
    for k, x0 in SIDE_X0.items():
        inst.append((f"Side Panel Near {k}", place_side_near(sp, x0 + SIDE_LEN / 2)))
        inst.append((f"Side Panel Far {k}", place_side_far(sp, x0 + SIDE_LEN / 2)))
    chain, _, _ = cable.chain_links(cable.X_MOVING_EXT)
    bf, bm = cable.bracket_fixed(), cable.bracket_moving()
    local.update([("Chain Link", cable.link()), ("Chain Lid", cable.lid_print()),
                  ("Chain Bracket Fixed", cable.flat(bf)), ("Chain Bracket Moving", bm)])
    inst += [(n, m) for n, _, m in chain] + [("Chain Bracket Fixed", bf), ("Chain Bracket Moving", bm)]
    tchain, _, _ = thin.chain_links(thin.X_MOVING_EXT)
    tbf, tbm = thin.bracket_fixed(), thin.bracket_moving()
    tcf, tcr = thin.channel_parts(thin.channel_x0())
    local.update([("Thin Link", thin.link()), ("Thin Lid", thin.lid_print()), ("Thin Bracket Fixed", cable.flat(tbf)),
                  ("Thin Bracket Moving", tbm), ("Thin Channel Front", cable.flat(tcf)), ("Thin Channel Rear", cable.flat(tcr))])
    inst += [(n, m) for n, _, m in tchain] + [("Thin Bracket Fixed", tbf), ("Thin Bracket Moving", tbm),
                                             ("Thin Channel Front", tcf), ("Thin Channel Rear", tcr)]
    for n, _, m, p in tray.parts():
        local[n] = p; inst.append((n, m))
    return local, inst

# ============================================================ checks
def near_vertices(m, tol=0.1):
    V = np.unique(np.asarray(m.to_mesh().vert_properties)[:, :3].round(5), axis=0)
    o = V[np.argsort(V[:, 0])]; n = 0
    for i in range(len(o)):
        j = i + 1
        while j < len(o) and o[j, 0] - o[i, 0] < tol:
            if np.linalg.norm(o[j] - o[i]) < tol: n += 1
            j += 1
    return n

def run_checks():
    local, inst = parts(); ok = True
    def rep(name, cond):
        nonlocal ok; ok &= bool(cond); print(("  ok    " if cond else "  FAIL  ") + name)
    print("checks:")
    for n, m in local.items():
        rep(f"{n}: manifold, one body", m.status().name == "NoError" and len(m.decompose()) == 1)
        rep(f"{n}: no vertices closer than 0.1 mm", near_vertices(m) == 0)
    ms = [m for _, m in inst]
    bad = 0
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            vol = (ms[i] ^ ms[j]).volume()
            if vol > 1e-3: bad += 1; rep(f"{inst[i][0]} vs {inst[j][0]}: no collision ({vol:.2f} mm3)", False)
    rep("no collisions between assembled parts", bad == 0)
    for n, (c0, c1) in (("Rear Panel Connector", (278, 438)), ("Rear Panel Switch", (478, 638))):
        b = dict(inst)[n].bounding_box()
        rep(f"{n} inside cell y {b[1]:.1f}..{b[4]:.1f} ({c0}..{c1})", b[1] >= c0 - 1e-6 and b[4] <= c1 + 1e-6)
    # IEC housing: IEC body (doc mesh: tabs end x 507.2; body 46.3 x 27.5, hooks +-15.3) free, retracted fan holders >= 3 mm away
    hs = dict(inst)["IEC Housing"]; hb = hs.bounding_box()
    yi = CELL_YC["right"] - IEC_U
    body = cable.box(507.2, REAR_X_OUT, yi - 23.15, yi + 23.15, ZC - 15.3, ZC + 15.3)
    rep(f"IEC Housing: IEC body incl. tabs (x 507.2..534.7) inside, no contact", (hs ^ body).volume() < 1e-6)
    fx = max(dict(inst)[f"Fan Holder {k + 1}"].bounding_box()[3] for k in range(len(tray.FAN_YC))) + cable.TRAVEL
    rep(f"IEC Housing back x {hb[0]:.1f} vs retracted fan holders x {fx:.1f}: gap {hb[0] - fx:.1f} (>= 3)", hb[0] - fx >= 3.0)
    rep(f"IEC Housing below the acrylic plate: z {hb[2]:.1f}..{hb[5]:.1f} (> 26 PE eye, < 102)", hb[2] > 26 and hb[5] < 102)
    # every mount tab must sit exactly on the cell edge (rail face) and over the rail centre line
    for name, m in inst:
        if not name.startswith(("Rear Panel", "Side", "Front Panel")): continue
        bb = m.bounding_box()
        rep(f"{name}: tabs reach the rail faces z {bb[2]:.2f} / {bb[5]:.2f} (25 / 105)", abs(bb[2] - Z0) < 1e-6 and abs(bb[5] - Z1) < 1e-6)
    for n in ("Chain Bracket Fixed",):
        cb = dict(inst)[n].bounding_box()
        rep(f"{n} inside the chain lane y {cb[1]:.1f}..{cb[4]:.1f} (290..330) and below the plate z {cb[5]:.1f} (<= 102)",
            cb[1] >= 290 - 1e-6 and cb[4] <= 330 + 1e-6 and cb[5] <= cable.CH_ZT + 1e-6)
    for n, ymax in (("Thin Bracket Fixed", 627.0), ("Thin Bracket Moving", 627.0), ("Thin Channel Front", 632.0), ("Thin Channel Rear", 632.0)):   # far slide rail from y 627 (z < 36)
        cb = dict(inst)[n].bounding_box()
        rep(f"{n} inside y {cb[1]:.1f}..{cb[4]:.1f} (535..{ymax:.0f}), z {cb[2]:.1f}..{cb[5]:.1f} (25..102)",
            cb[1] >= 535 and cb[4] <= ymax + 1e-6 and cb[2] >= 25 - 1e-6 and cb[5] <= thin.ZT + 1e-6)
    # 60 mm fans (bought, document): bodies free of every printed part; holders between the chain lanes, below the thin channel
    for k, yc in enumerate(tray.FAN_YC):
        fb = tray.fan_box(yc); fm = cable.box(*fb)
        hit = [n for n, m in inst if (fm ^ m).volume() > 1e-3]
        rep(f"Fan {k + 1} body x {fb[0]:.1f}..{fb[1]:.1f} y {fb[2]:.1f}..{fb[3]:.1f} z {fb[4]:.1f}..{fb[5]:.1f}: no printed part inside{'' if not hit else ': ' + ', '.join(hit)}", not hit)
        hb = dict(inst)[f"Fan Holder {k + 1}"].bounding_box()
        rep(f"Fan Holder {k + 1} y {hb[1]:.1f}..{hb[4]:.1f} (330.4..603), z top {hb[5]:.1f} (<= 85, thin channel 86.5)",
            hb[1] >= 330.4 and hb[4] <= 603.0 and hb[5] <= 85.0 + 1e-6)
        # stepper motor of the stock frame (document Stock Frame/Group#4: x 472..514, y 392.4..463.4, z >= 77.9) cannot move:
        # retracted fan, holder above z 77.9 and the M4 nuts behind the plate must stay in front of it
        top = (dict(inst)[f"Fan Holder {k + 1}"] ^ cable.box(0, 1000, 0, 1000, 77.9, 200)).bounding_box()
        xr = max(fb[1], top[3], tray.FH_X1 + tray.FH_NUT) + cable.TRAVEL
        rep(f"Fan {k + 1} retracted: fan, holder top and nuts end x {xr:.1f} (< motor x 472)", xr < 472.0)
    for mod, tag, pitch, zu, zl in ((thin, "thin", thin.PITCH, thin.ZU, thin.ZL), (cable, "wide", cable.CHP, cable.CHAIN_ZU, cable.CHAIN_ZL)):
        arc = math.degrees(2 * math.asin(pitch / (zu - zl)))
        hit, stop = mod.hinge_sweep(arc + 5.0)
        rep(f"{tag} hinge incl. clamps free from 0 to {arc + 5.0:.0f} deg (arc needs {arc:.1f}){'' if hit is None else f': collision at {hit:.0f} deg'}", hit is None)
        rep(f"{tag} hinge: stop engages against bending outwards (collision at -1.5 deg)", bool(stop))
    poses = [(cable, "wide", xm) for xm in (cable.X_MOVING_EXT, cable.X_MOVING_EXT + cable.TRAVEL / 2, cable.X_MOVING_EXT + cable.TRAVEL)]
    poses += [(thin, "thin", xm) for xm in (thin.X_MOVING_EXT, thin.X_MOVING_EXT + thin.TRAVEL / 2, thin.X_MOVING_EXT + thin.TRAVEL)]
    for mod, tag, xm in poses:
        links, P, xc = mod.chain_links(xm); bad = 0
        for i in range(len(links)):
            for j in range(i + 1, len(links)):
                bi, bj = links[i][2].bounding_box(), links[j][2].bounding_box()
                if any(bi[k] > bj[k + 3] or bj[k] > bi[k + 3] for k in range(3)): continue
                if (links[i][2] ^ links[j][2]).volume() > 1e-3: bad += 1
        zs = [lk[2].bounding_box() for lk in links]
        ys = (min(b[1] for b in zs), max(b[4] for b in zs))
        rep(f"{tag} chain pose moving end x {xm:.0f}: arc centre x {xc:.0f}, no link collisions, z {min(b[2] for b in zs):.1f}..{max(b[5] for b in zs):.1f} (25..102), y {ys[0]:.1f}..{ys[1]:.1f}",
            bad == 0 and min(b[2] for b in zs) >= 25 - 1e-6 and max(b[5] for b in zs) <= cable.CH_ZT + 1e-6)
        # the arc moves with the fixed end, the drawer with the moving end: arc front vs inner face of the drawer front plates
        front = min(b[0] for b in zs) - (xm - mod.X_MOVING_EXT)
        rep(f"{tag} chain pose moving end x {xm:.0f}: arc front x {front:.1f} in drawer coordinates (>= {DRAWER_FRONT_IN + 3:.0f})",
            front >= DRAWER_FRONT_IN + 3)
    # wires: not printed, so outside the part collision test above, but they must not pierce any printed part
    ws = wiring.wires()
    for n, _, m, info in ws:
        rep(f"{n}: manifold, one body", m.status().name == "NoError" and len(m.decompose()) == 1)
        rep(f"{n}: no vertices closer than 0.1 mm", near_vertices(m) == 0)
        need = wiring.MIN_R * info["d"]
        free = [r for r, k in zip(info["radii"], info["kinks"]) if not k]
        rmin = min(free, default=float("inf"))
        rep(f"{n}: bend radius {rmin:.1f} >= {need:.0f} (4 x D)", rmin >= need - 1e-6)
        if any(info["kinks"]):
            print(f"  info  {n}: kink at the terminal, R {min(r for r, k in zip(info['radii'], info['kinks']) if k):.1f} (accepted)")
        wb = m.bounding_box(); hit = []
        for pn, pm in inst + wiring.bought_boxes():
            pb = pm.bounding_box()
            if any(wb[k] > pb[k + 3] or pb[k] > wb[k + 3] for k in range(3)): continue
            if (m ^ pm).volume() > 1e-3: hit.append(pn)
        rep(f"{n}: pierces no printed part / WAGO / PSU case{'' if not hit else ': ' + ', '.join(hit)}", not hit)
    short = wiring.sheath_for_cores()
    def body(a, b):   # a chain core is checked against the sheath without the end face it leaves from
        return short if a[0] == wiring.SHEATH and wiring.is_chain_core(b[0]) else a[2]
    bad = [f"{ws[i][0]} x {ws[j][0]}" for i in range(len(ws)) for j in range(i + 1, len(ws))
           if (body(ws[i], ws[j]) ^ body(ws[j], ws[i])).volume() > 1e-3]
    rep(f"wires do not intersect each other{'' if not bad else ': ' + '; '.join(bad)}", not bad)
    for n, m in local.items():
        bb = m.bounding_box(); print(f"  info  {n}: {bb[3]-bb[0]:.1f} x {bb[4]-bb[1]:.1f} x {bb[5]-bb[2]:.1f} mm, {m.volume()/1000:.1f} cm3")
    print("all checks passed" if ok else "CHECKS FAILED")

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(os.path.join(outdir, "stl"), exist_ok=True)
    for f in os.listdir(os.path.join(outdir, "stl")):
        if f.endswith(".stl"): os.remove(os.path.join(outdir, "stl", f))
    local, inst = parts()
    for name, m in local.items():
        b = m.bounding_box()
        write_stl(m.translate([-b[0], -b[1], -b[2]]), os.path.join(outdir, "stl", name.replace(" ", "_") + ".stl"))
        print(f"{name:20s} genus {m.genus():3d}  vol {m.volume() / 1000:7.2f} cm3  {m.status().name}")
    ischain = lambda n: n.startswith(("Chain", "Cable", "Thin"))
    tcol = {n: c for n, c, _, _ in tray.parts()}
    def style(n):
        if n in tcol: return TRAY_LAYER, tcol[n]
        if n == "IEC Housing": return LAYER, tray.COL_MAINS     # 230 V touch guard: red like the mains parts
        return (CHAIN_LAYER, CHAIN_COL) if ischain(n) else (LAYER, COL)
    data = [{"name": n, "layer": style(n)[0], "color": list(style(n)[1]), "faces": planar_faces(m)} for n, m in inst]
    data += [{"name": n, "layer": wiring.LAYER, "color": list(c), "faces": planar_faces(m)} for n, c, m, _ in wiring.wires()]
    with open(os.path.join(outdir, "parts.json"), "w") as f:
        json.dump(data, f)
    if "--check" in sys.argv:
        run_checks()
