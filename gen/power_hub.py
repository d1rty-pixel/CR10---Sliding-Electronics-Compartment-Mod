"""Power hub between the two PSUs (world mm, tray fully out): red mains box + yellow DC box, each a base and a lid.

Both PSUs have their AC / DC terminal boundary on one line, y = Y_DIV (LRS-350: pins 1-3 AC/L, AC/N, FG above, 4-9 -V/+V below;
RS-15-5: pins 1-3 above, -V/+V below; Mean Well data sheets). Two separate boxes, each with its own wall on that line (double
wall, 0.2 gap): mains (red, +y) and DC (yellow, -y), each on its own DIN rail (tray.POWER_RAILS) with its own lid screws.
The lids reach over the terminal blocks of both PSUs (port covers) and drop skirts onto the PSU cases.
WAGO 221 stand in pockets on the red face of the divider (the closed wall opposite the cable entry), entries up, levers to +y.
"""
from manifold3d import Manifold, CrossSection, JoinType
from cable import box, cyl_z, _ccw, _plate_y

# the boxes clip onto the power rails (tray.py); floor on the clip base
FLOOR_Z, T, LID_T = 15.9, 1.6, 1.6         # clip base top is z 16 (tray.CLIP_TOP): 0.1 overlap so the clip fuses
Z_TOP = 58.0                              # top of the base walls = underside of the lids (LRS top 55.9, RS top 53.0)
# PSU positions (user 2026-11-03: both PSUs about 5 mm from the tray edges): LRS-350 x -373.75..-158.75 (drawer frame inside
# -378.8), RS-15-5 x -48.5..26.06 incl. terminals (rear cross member 2020 L=334 from x 31.2). Shift against the vendor STEP
# placement (LRS -364..-149, RS -63..11.56); the document groups are moved by the same amounts. Binary-exact values on purpose:
# -9.8 / 14.6 left float noise that IngeTrazo turned into zero-length edges on the lids.
LRS_DX, RS_DX = -9.75, 14.5
X0, X1 = -148.5 + LRS_DX, -63.5 + RS_DX    # base between the PSUs: 0.5 to the LRS case end and to the RS block
Y_DIV = 557.0                             # AC / DC boundary of both PSUs
Y_RED, Y_DC = 604.0, 475.0                # outer +y face (2020 of the tray from 605) / outer -y face (DC duct up to 473)
RW = (Y_DIV + 0.1, Y_DIV + 0.1 + T)          # red wall on the boundary
YW = (Y_DIV - 0.1 - T, Y_DIV - 0.1)          # yellow wall on the boundary

# PSU terminal blocks (from the vendor STEP models as placed in the document)
LRS = dict(x_hood=-168.0 + LRS_DX, top=55.9, y_red=590.0, y_dc=497.0, wire_z=30.0)   # block x -166.1..-151.5 (+LRS_DX), y 498.5..585.5
RS = dict(x_hood=-48.0 + RS_DX, top=53.0, block_x=-52.0 + RS_DX, block_top=43.7, y_red=582.4, y_dc=539.3, wire_z=29.0)   # block y 540.9..580.6

# WAGO 221 standing on the floor in front of the divider: (name, width); 221-413 18.7 x 18.6 x 8.3, 221-414 width assumed 24.9
WAGOS = [("L", 18.7), ("N", 18.7), ("PE", 24.9)]
W_LEN, W_THK, RIB, FIT = 18.6, 8.3, 1.2, 0.1
SEAM_GAP = 8.0                            # between the N and PE pockets: room for the red wall boss (r 3.5 + rib clearance)
def wago_slots():
    """[(name, x0, x1)] of the WAGO bodies, centred on the base; every pocket has its own two ribs (L|N share one)"""
    tot = sum(w for _, w in WAGOS) + 5 * RIB + 2 * FIT * len(WAGOS) + SEAM_GAP
    x = (X0 + X1) / 2 - tot / 2 + RIB; out = []
    for n, w in WAGOS:
        if n == "PE": x += SEAM_GAP + RIB
        out.append((n, x + FIT, x + FIT + w)); x += w + 2 * FIT + RIB
    return out

def seam_x():
    """x of the wall bosses: middle of the gap between the N and PE pockets"""
    sl = dict((n, (a, b)) for n, a, b in wago_slots())
    return (sl["N"][1] + FIT + RIB + sl["PE"][0] - FIT - RIB) / 2
SEAM_R = 3.5

W_Y0 = RW[1] + 0.2                       # back of the WAGO
W_Z0 = FLOOR_Z + T                        # standing on the floor

ENTRY = (-109.0, -94.0, 27.0)             # chain cable (thin bracket exit x -108..-96, z 29..39)
PE_SLOT = (-80.0, -74.0, 22.0)            # PE to the ring lug on the tray 2020; +x of the moving chain bracket (x <= -80.8)
DUCT_WIN = (-140.0, -72.0, 17.5, 25.0)    # DC wires into the DC duct through its finger slots (z 16..25); bottom = hub floor top
BOSS_R, BOSS_PILOT = 4.0, 2.8          # corner bosses concentric with the corner arcs, filled to the walls
# (x, y, sx, sy): boss centre and the directions towards its two walls
RED_BOSSES = ((X0 + 6.0, Y_RED - 6.0, -1, 1), (X1 - 6.0, Y_RED - 6.0, 1, 1))
DC_BOSSES = ((X0 + 6.0, Y_DC + 6.0, -1, -1), (X1 - 6.0, Y_DC + 6.0, 1, -1))

def _rect(x0, x1, y0, y1):
    return CrossSection.square((x1 - x0, y1 - y0)).translate((x0, y0))

def _vz(cs, z0, z1):
    return Manifold.extrude(cs, z1 - z0).translate((0, 0, z0))

R_CORNER = 3.0

R_BASE = 6.0                              # base corners: the lid bosses are concentric with these arcs (no intersecting circles)

def _rounded(pts, rs=R_CORNER, n=8):
    """CCW polygon with its convex corners rounded (arcs start exactly on the edges: no near-duplicate vertices);
    inner corners stay sharp (the skirts are split there)"""
    import math
    out, k = [], len(pts)
    for i in range(k):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % k]
        d0 = (p1[0] - p0[0], p1[1] - p0[1]); d1 = (p2[0] - p1[0], p2[1] - p1[1])
        if d0[0] * d1[1] - d0[1] * d1[0] <= 0: out.append(p1); continue          # right turn = inner corner
        r = rs[i] if isinstance(rs, (list, tuple)) else rs
        l0, l1 = math.hypot(*d0), math.hypot(*d1)
        u0, u1 = (d0[0] / l0, d0[1] / l0), (d1[0] / l1, d1[1] / l1)
        c = (p1[0] - u0[0] * r + u1[0] * r, p1[1] - u0[1] * r + u1[1] * r)    # axis-parallel edges only
        a0 = math.atan2(-u1[1], -u1[0]); a1 = math.atan2(u0[1], u0[0])
        while a1 < a0: a1 += 2 * math.pi
        out += [(c[0] + r * math.cos(a0 + (a1 - a0) * j / n), c[1] + r * math.sin(a0 + (a1 - a0) * j / n)) for j in range(n + 1)]
    return CrossSection([out])

def _base_plan():
    return _rounded([(X0, Y_DC), (X1, Y_DC), (X1, Y_RED), (X0, Y_RED)], R_BASE)

def _inner_plan():
    w = T
    return _rounded([(X0 + w, Y_DC + w), (X1 - w, Y_DC + w), (X1 - w, Y_RED - w), (X0 + w, Y_RED - w)], R_BASE - w)

def _outline():
    """plan of both lids together: base + port covers"""
    L, R = LRS, RS
    c, b = R_CORNER, R_BASE
    return _rounded([(L["x_hood"], L["y_dc"]), (X0, L["y_dc"]), (X0, Y_DC), (X1, Y_DC), (X1, R["y_dc"]), (R["x_hood"], R["y_dc"]),
                     (R["x_hood"], R["y_red"]), (X1, R["y_red"]), (X1, Y_RED), (X0, Y_RED), (X0, L["y_red"]), (L["x_hood"], L["y_red"])],
                    [c, 0, b, b, 0, c, c, 0, b, b, 0, c])

def _half(cs, red):
    big = 2000.0
    return cs ^ (_rect(-big, big, RW[0], big) if red else _rect(-big, big, -big, YW[1]))

def _pads(corners, r):
    """corner boss with its wedge to both walls: circle r plus the two rectangles between its tangent points and the walls"""
    cs = CrossSection()
    for cx, cy, sx, sy in corners:
        far = 20.0
        xa = sorted((cx, cx + sx * far)); ya = sorted((cy - sy * r, cy + sy * far))
        xb = sorted((cx - sx * r, cx + sx * far)); yb = sorted((cy, cy + sy * far))
        cs = cs + CrossSection.circle(r, 24).translate((cx, cy)) + _rect(*xa, *ya) + _rect(*xb, *yb)
    return cs

def wall_boss(red):
    """(x, y) of the lid boss fused to the box's own boundary wall (red: in the gap between the N and PE pockets)"""
    return (seam_x(), RW[1] + 2.0) if red else (seam_x(), YW[0] - 2.0)   # 2.0: no circle vertex within 0.1 of the wall

def _wall_boss(red, r=SEAM_R):
    """circle plus a band to the wall (edges on the circle's 0/180 deg vertices: no shallow wall intersection)"""
    x, y = wall_boss(red)
    band = _rect(x - r, x + r, y, RW[1] - 0.5) if red else _rect(x - r, x + r, YW[0] + 0.5, y)
    return CrossSection.circle(r, 24).translate((x, y)) + band

def _pilots(m, pts):
    for x, y in pts:
        m = m - cyl_z(x, y, Z_TOP - 12.0, Z_TOP + 1, BOSS_PILOT, 16)
    return m

# ============================================================ vents (the 4 fans behind the rear cross member blow -x through both boxes onto the LRS)
VENT_W, VENT_PITCH = 2.5, 5.0             # vertical strip slots in both x walls of both boxes
VENT_Z0 = FLOOR_Z + T + 2.0               # 2.0 above the floor top
VENT_ZT = Z_TOP - 4.0                     # below the lid lip (z 56..58)
VENT_EDGE = 1.5                           # web to every cut-out, boss pad and boundary wall

def vent_slots(red):
    """[(x wall, y centre, z0, z1)] of the strip slots; below the terminal wire cut-outs only up to wire_z - 2"""
    if red:
        y_lo, y_hi = RW[1] + VENT_EDGE, Y_RED - R_BASE - BOSS_R - VENT_EDGE
        cuts = {X0: ((RW[1], LRS["y_red"]), LRS["wire_z"]), X1: ((RW[1], RS["y_red"] - 1.8), RS["wire_z"])}
    else:
        y_lo, y_hi = Y_DC + R_BASE + BOSS_R + VENT_EDGE, YW[0] - VENT_EDGE
        cuts = {X0: ((LRS["y_dc"] + 2.0, YW[0]), LRS["wire_z"]), X1: ((RS["y_dc"] + 1.6, YW[0]), RS["wire_z"])}
    out = []
    n = int((y_hi - y_lo - VENT_W) // VENT_PITCH) + 1
    off = (y_hi - y_lo - VENT_W - (n - 1) * VENT_PITCH) / 2       # centred in the free band
    for xw, ((c0, c1), wz) in cuts.items():
        for k in range(n):
            y = y_lo + off + VENT_W / 2 + k * VENT_PITCH
            under = c0 - VENT_EDGE < y + VENT_W / 2 and y - VENT_W / 2 < c1 + VENT_EDGE
            out.append((xw, y, VENT_Z0, wz - 2.0 if under else VENT_ZT))
    return out

def _vents(b, red):
    for xw, y, z0, z1 in vent_slots(red):
        xa, xb = (xw - 1, xw + T + 1) if xw == X0 else (xw - T - 1, xw + 1)
        b = b - box(xa, xb, y - VENT_W / 2, y + VENT_W / 2, z0, z1)
    return b

# ============================================================ red base
def _wago_pockets():
    """free-standing ribs (0.6 gap to the wall so they flex): front lips at the bottom, ramped snap noses over the top edge"""
    m = Manifold(); y0, y1 = RW[1] + 0.6, W_Y0 + W_THK + 1.2
    zr = W_Z0 + W_LEN + 1.8                                      # rib top
    slots = wago_slots()
    edges = sorted({round(a - FIT - RIB, 4) for _, a, _ in slots} | {round(b + FIT, 4) for _, _, b in slots})
    for xe in edges:
        m = m + box(xe, xe + RIB, y0, y1, W_Z0, zr)
    for _, a, b in slots:
        for xw, s in ((a - FIT, +1), (b + FIT, -1)):             # inner face of the rib, s = direction into the pocket
            xo = xw - s * 0.05                                     # overlap into the rib (touching bodies stay separate)
            lip = box(*sorted((xo, xw + s * 1.0)), W_Y0 + W_THK, y1, W_Z0, W_Z0 + 7.0)
            zt = W_Z0 + W_LEN + 0.1
            nose = CrossSection([_ccw([(xo, zt), (xw + s * 0.8, zt), (xw, zr), (xo, zr)])])
            m = m + lip + _plate_y(nose, W_Y0 + 4.0, W_Y0 + W_THK)
    return m

def red_base():
    w = T
    bp = _base_plan() ^ _rect(X0 - 1, X1 + 1, RW[0], Y_RED + 1)              # incl. its boundary wall
    cav = (_inner_plan() ^ _rect(X0, X1, RW[1], Y_RED)) - _pads(RED_BOSSES, BOSS_R) - _wall_boss(True)
    b = _vz(bp, FLOOR_Z, Z_TOP) - _vz(cav, FLOOR_Z + T, Z_TOP + 1)
    b = b - box(X0 - 1, X0 + w + 1, RW[1], LRS["y_red"], LRS["wire_z"], Z_TOP + 1)       # wires from the LRS AC terminals
    b = b - box(X1 - w - 1, X1 + 1, RW[1], RS["y_red"] - 1.8, RS["wire_z"], Z_TOP + 1)  # wires from the RS AC terminals
    b = b - box(ENTRY[0], ENTRY[1], Y_RED - w - 1, Y_RED + 1, ENTRY[2], Z_TOP + 1)
    b = b - box(PE_SLOT[0], PE_SLOT[1], Y_RED - w - 1, Y_RED + 1, PE_SLOT[2], Z_TOP + 1)
    b = _pilots(b, [c[:2] for c in RED_BOSSES] + [wall_boss(True)]) + _wago_pockets()
    tie = box(ENTRY[0] + 1.0, ENTRY[1] - 1.0, Y_RED - w - 7.0, Y_RED - w - 1.0, FLOOR_Z + T, 29.0)   # strain relief for the chain cable
    tie = tie - box(ENTRY[0], ENTRY[1], Y_RED - w - 5.5, Y_RED - w - 2.5, 24.0, 26.5)              # zip-tie tunnel along x
    b = b + tie
    return _vents(b, True)

# ============================================================ yellow base (own boundary wall YW)
def dc_base():
    w = T
    bp = _base_plan() ^ _rect(X0 - 1, X1 + 1, Y_DC - 1, YW[1])
    cav = (_inner_plan() ^ _rect(X0, X1, Y_DC, YW[0])) - _pads(DC_BOSSES, BOSS_R) - _wall_boss(False)
    b = _vz(bp, FLOOR_Z, Z_TOP) - _vz(cav, FLOOR_Z + T, Z_TOP + 1)
    b = b - box(X0 - 1, X0 + w + 1, LRS["y_dc"] + 2.0, YW[0], LRS["wire_z"], Z_TOP + 1)      # LRS DC terminals
    b = b - box(X1 - w - 1, X1 + 1, RS["y_dc"] + 1.6, YW[0], RS["wire_z"], Z_TOP + 1)        # RS DC terminals
    b = b - box(DUCT_WIN[0], DUCT_WIN[1], Y_DC - 1, Y_DC + w + 1, DUCT_WIN[2], DUCT_WIN[3])
    b = _pilots(b, [c[:2] for c in DC_BOSSES] + [wall_boss(False)])
    return _vents(b, False)

# ============================================================ lids (roof + port covers + skirts)
BOLT = [(-1.0, 6.0), (3.0, 6.0), (0.6, 0.8), (3.2, 0.8), (-1.2, -7.0), (0.0, -1.2), (-2.8, -1.2)]   # engraved mains bolt

def _lid(red):
    plan = _half(_outline(), red)
    ring = plan - plan.offset(-T, JoinType.Miter)
    big = 2000.0
    m = _vz(plan, Z_TOP, Z_TOP + LID_T)
    m = m + _vz(ring ^ _rect(-big, X0, -big, big), LRS["top"] + 0.6, Z_TOP)                           # onto the LRS case
    m = m + _vz(ring ^ _rect(RS["block_x"], big, -big, big), RS["top"] + 0.5, Z_TOP)                  # onto the RS case
    m = m + _vz(ring ^ _rect(X1, RS["block_x"], -big, big), RS["block_top"] + 0.5, Z_TOP)             # beside the RS block
    wy = RW if red else YW                                     # own boundary skirt over both terminal blocks
    m = m + box(LRS["x_hood"] + 1.0, X0, *wy, 49.0, Z_TOP)
    m = m + box(X1, RS["x_hood"] - 1.0, *wy, RS["block_top"] + 0.5, Z_TOP)
    if red:
        y_in = (RW[1] + 0.3, Y_RED - T - 0.3)
        for x0, x1, zb in ((ENTRY[0] + 0.3, ENTRY[1] - 0.3, 41.0), (PE_SLOT[0] + 0.3, PE_SLOT[1] - 0.3, 30.0)):
            m = m + box(x0, x1, Y_RED - T, Y_RED, zb, Z_TOP)                                          # tongues down to the cables
        bolts, bc = BOLT, ((X0 + X1) / 2, (Y_DIV + Y_RED) / 2 + 4.0)
    else:
        y_in = (Y_DC + T + 0.3, YW[0] - 0.3)
        bolts, bc = None, None
    ri = R_BASE - T - 0.3
    rr = [0, 0, ri, ri] if red else [ri, ri, 0, 0]
    rq = [0, 0, ri - 1.2, ri - 1.2] if red else [ri - 1.2, ri - 1.2, 0, 0]
    xa, xb = X0 + T + 0.3, X1 - T - 0.3
    lip = (_rounded([(xa, y_in[0]), (xb, y_in[0]), (xb, y_in[1]), (xa, y_in[1])], rr)
           - _rounded([(xa + 1.2, y_in[0] + 1.2), (xb - 1.2, y_in[0] + 1.2), (xb - 1.2, y_in[1] - 1.2), (xa + 1.2, y_in[1] - 1.2)], rq))
    lip = lip - _pads(RED_BOSSES if red else DC_BOSSES, BOSS_R + 0.3) - _wall_boss(red, SEAM_R + 0.3)
    m = m + _vz(lip, Z_TOP - 2.0, Z_TOP)
    for x, y in [c[:2] for c in (RED_BOSSES if red else DC_BOSSES)] + [wall_boss(red)]:
        m = m - cyl_z(x, y, Z_TOP - 3, Z_TOP + 3, 3.4, 16)
    if bolts:
        sym = CrossSection([_ccw([(bc[0] + 2.0 * u, bc[1] + 2.0 * v) for u, v in bolts])])
        m = m - _vz(sym, Z_TOP + LID_T - 0.6, Z_TOP + LID_T + 1)
    return m

def red_lid():
    return _lid(True)

def dc_lid():
    return _lid(False)
