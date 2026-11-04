"""Power hub between the LRS-350 and the turned RS-15-5 (world mm, tray fully out): red mains box + DC box, each a base and a lid.

LRS-350 (terminals +x): its AC / DC terminal boundary lies on y = Y_DIV (pins 1-3 AC/L, AC/N, FG above, 4-9 -V/+V below; Mean Well
data sheet). RS-15-5 turned 90 deg clockwise seen from above (user 2026-11-04): body along y in front of the DC duct, terminal block
facing +y, pins along x (L at +x ... +V at -x); its AC / DC boundary is the line x = XD between FG and -V.
The divider between the boxes is an L: y = Y_DIV from the LRS to x = XD, then along x = XD down to the RS terminal face; double wall
(0.2 gap), each box on its own DIN rail (tray.POWER_RAILS) with its own lid screws. The red box reaches over the AC pins of the RS up
to the fan ducts (X1R), the DC box keeps the DC pins of both PSUs. The RS terminal block passes through a cut-out in the pocket wall
and the divider (from BLK_Z up); the lids close it with skirts down to the block top. The lids also reach over the LRS terminal block
(port cover) and drop skirts onto its case.
WAGO 221 stand in pockets on the red face of the divider (y = Y_DIV), entries up, levers to +y, W_GAP apart.
"""
from manifold3d import Manifold, CrossSection, JoinType
from cable import box, cyl_z, _ccw, _plate_y

# the boxes clip onto the power rails (tray.py); floor on the clip base
FLOOR_Z, T, LID_T = 15.9, 1.6, 1.6         # clip base top is z 16 (tray.CLIP_TOP): 0.1 overlap so the clip fuses
Z_TOP = 58.0                              # top of the base walls = underside of the lids (LRS top 55.9, RS top 53.0)
# LRS-350 x -373.75..-158.75 (user 2026-11-03: about 5 mm from the drawer frame, inside -378.8); shift against the vendor STEP
# placement (-364..-149). Binary-exact on purpose: -9.8 left float noise that IngeTrazo turned into zero-length edges on the lids.
LRS_DX = -9.75
X0 = -148.5 + LRS_DX                      # -x face of both boxes: 0.5 to the LRS case end
Y_DIV = 557.0                             # AC / DC boundary of the LRS terminal block
Y_RED, Y_DC = 604.0, 475.0                # outer +y face (2020 of the tray from 604.8) / outer -y face (DC duct up to 473)
RW = (Y_DIV + 0.1, Y_DIV + 0.1 + T)          # red wall on the boundary
YW = (Y_DIV - 0.1 - T, Y_DIV - 0.1)          # DC wall on the boundary

# LRS terminal block (vendor STEP as placed in the document)
LRS = dict(x_hood=-168.0 + LRS_DX, top=55.9, y_red=590.0, y_dc=497.0, wire_z=30.0)   # block x -175.85..-161.25, y 498.5..585.5

# RS-15-5, turned 90 deg clockwise (user 2026-11-04). Vendor STEP as placed before (terminals -x): body x -36.6..26.06,
# y 530.75..581.85, z 25..53; block x -48.5..-36.6, y 540.84..580.5, z 30.59..43.75; pins at y 576.0 L / 568.4 N / 560.8 FG /
# 553.1 -V / 545.5 +V (docs/COMPONENTS.md). New = (y - RS_MAP[0], RS_MAP[1] - x): body against the DC duct side (y 475.5),
# body x end 9.05 (fan power lane from x 10.2).
RS_MAP = (572.8, 501.56)
def rs_xy(x, y):
    """old RS position (terminals -x) -> turned position"""
    return (y - RS_MAP[0], RS_MAP[1] - x)
RS_BODY = (*sorted(rs_xy(0, y)[0] for y in (530.75, 581.85)), *sorted(rs_xy(x, 0)[1] for x in (-36.6, 26.06)), 25.0, 53.0)
RS_BLOCK = (*sorted(rs_xy(0, y)[0] for y in (540.84, 580.5)), *sorted(rs_xy(x, 0)[1] for x in (-48.5, -36.6)), 30.59, 43.75)
RS_PINS = {n: rs_xy(0, y)[0] for n, y in (("L", 576.0), ("N", 568.4), ("FG", 560.8), ("-V", 553.1), ("+V", 545.5))}
XD = (RS_PINS["FG"] + RS_PINS["-V"]) / 2  # divider along y between FG and -V of the RS
XR0 = RS_BODY[0] - 0.5                    # +x face of the DC box beside the RS body
X1R = 10.0                                # +x face of the red box (fan power lane from 10.2)
Y_P = RS_BODY[3] + 0.2                    # -y face of the pocket over the RS terminals (0.2 to the RS case)
BLK_Z = 30.0                              # cut-out for the RS block in the pocket wall / divider from here up (block bottom 30.59)
BLK_CUT = (RS_BLOCK[0] - 0.5, RS_BLOCK[1] + 0.5, RS_BLOCK[3] + 0.5)   # x0, x1, y end
BLK_SKIRT_Z = RS_BLOCK[5] + 0.5           # lid skirts in the cut-out stop 0.5 over the block

# WAGO 221 standing on the floor in front of the divider: (name, width); 221-413 18.7 x 18.6 x 8.3, 221-414 width assumed 24.9
WAGOS = [("L", 18.7), ("N", 18.7), ("PE", 24.9)]
W_LEN, W_THK, RIB, FIT = 18.6, 8.3, 1.2, 0.1
W_GAP = 10.0                              # between the pockets (each with its own two ribs): wires; between N and PE the wall boss
def wago_slots():
    """[(name, x0, x1)] of the WAGO bodies, centred on the divider stretch X0..XD"""
    tot = sum(w + 2 * FIT + 2 * RIB for _, w in WAGOS) + W_GAP * (len(WAGOS) - 1)
    x = (X0 + XD) / 2 - tot / 2; out = []
    for n, w in WAGOS:
        out.append((n, x + RIB + FIT, x + RIB + FIT + w)); x += w + 2 * FIT + 2 * RIB + W_GAP
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
DUCT_WIN = (-140.0, -72.0, 17.5, 29.0)    # DC wires into the DC duct over the spout (spout()); floor top .. 1 under the duct lid (tray: z 30)
# form fit to the DC duct (tray.DC): under DUCT_WIN the floor runs out as a rounded spout; its hook reaches behind the inner face of
# the duct's +y wall (notched down to NOTCH_Z there), its skirt stands in front of the outer face down to the clip bottom (print bed)
DUCT_Y1, DUCT_WALL = 473.0, 1.6          # outer +y face and wall of the DC duct (tray.DC yc 463, DUCT_W 20)
SPOUT_R, SPOUT_GAP, SPOUT_Z0 = 4.0, 0.2, 6.0
NOTCH_Z = FLOOR_Z - SPOUT_GAP            # 15.7: top of the notched duct wall under the spout bridge
BOSS_R, BOSS_PILOT = 4.0, 2.8          # corner bosses concentric with the corner arcs, filled to the walls
R_CORNER = 3.0
R_BASE = 6.0                              # base corners: the lid bosses are concentric with these arcs (no intersecting circles)
# (x, y, sx, sy): boss centre and the directions towards its two walls. No boss in the pocket: the RS block and its wires fill it.
RED_BOSSES = ((X0 + R_BASE, Y_RED - R_BASE, -1, 1), (X1R - R_BASE, Y_RED - R_BASE, 1, 1))
DC_BOSSES = ((X0 + R_BASE, Y_DC + R_BASE, -1, -1), (XR0 - R_BASE, Y_DC + R_BASE, 1, -1))

def box_x(red):
    """x extent of a box base (for the DIN clips)"""
    return (X0, X1R) if red else (X0, XR0)

def _rect(x0, x1, y0, y1):
    return CrossSection.square((x1 - x0, y1 - y0)).translate((x0, y0))

def _vz(cs, z0, z1):
    return Manifold.extrude(cs, z1 - z0).translate((0, 0, z0))

def _rounded(pts, rs=R_CORNER, n=8):
    """CCW polygon with its convex corners rounded (arcs start exactly on the edges: no near-duplicate vertices);
    inner corners and corners with radius 0 stay sharp"""
    import math
    out, k = [], len(pts)
    for i in range(k):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % k]
        d0 = (p1[0] - p0[0], p1[1] - p0[1]); d1 = (p2[0] - p1[0], p2[1] - p1[1])
        r = rs[i] if isinstance(rs, (list, tuple)) else rs
        if d0[0] * d1[1] - d0[1] * d1[0] <= 0 or r <= 0: out.append(p1); continue          # right turn = inner corner
        l0, l1 = math.hypot(*d0), math.hypot(*d1)
        u0, u1 = (d0[0] / l0, d0[1] / l0), (d1[0] / l1, d1[1] / l1)
        c = (p1[0] - u0[0] * r + u1[0] * r, p1[1] - u0[1] * r + u1[1] * r)    # axis-parallel edges only
        a0 = math.atan2(-u1[1], -u1[0]); a1 = math.atan2(u0[1], u0[0])
        while a1 < a0: a1 += 2 * math.pi
        out += [(c[0] + r * math.cos(a0 + (a1 - a0) * j / n), c[1] + r * math.sin(a0 + (a1 - a0) * j / n)) for j in range(n + 1)]
    return CrossSection([out])

def _plan(red, hood=False):
    """outer plan of a box; with hood: plus the port cover over the LRS terminal block (lids)"""
    L, b, c = LRS, R_BASE, R_CORNER
    if red:
        pts = [(X0, RW[0]), (XD + 0.1, RW[0]), (XD + 0.1, Y_P), (X1R, Y_P), (X1R, Y_RED), (X0, Y_RED)]
        rs = [0, 0, 0, 0, b, b]                     # pocket corners sharp: an arc there met the block cut-out within 0.1
        if hood:
            pts = [(L["x_hood"], RW[0])] + pts[1:] + [(X0, L["y_red"]), (L["x_hood"], L["y_red"])]
            rs = [0] + rs[1:] + [0, c]
    else:
        pts = [(X0, Y_DC), (XR0, Y_DC), (XR0, Y_P), (XD - 0.1, Y_P), (XD - 0.1, YW[1]), (X0, YW[1])]
        rs = [b, b, 0, 0, 0, 0]
        if hood:
            pts = [(L["x_hood"], L["y_dc"]), (X0, L["y_dc"])] + pts[:-1] + [(L["x_hood"], YW[1])]
            rs = [c, 0] + rs[:-1] + [0]
    return _rounded(pts, rs)

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
    """(x, y) of the lid boss fused to the box's own boundary wall (in the gap between the N and PE pockets)"""
    return (seam_x(), RW[1] + 2.0) if red else (seam_x(), YW[0] - 2.0)   # 2.0: no circle vertex within 0.1 of the wall

def _wall_boss(red, r=SEAM_R):
    """circle plus a band to the wall (edges on the circle's 0/180 deg vertices: no shallow wall intersection)"""
    x, y = wall_boss(red)
    band = _rect(x - r, x + r, y, RW[1] - 0.5) if red else _rect(x - r, x + r, YW[0] + 0.5, y)
    return CrossSection.circle(r, 24).translate((x, y)) + band

def _bosses(red):
    return [c[:2] for c in (RED_BOSSES if red else DC_BOSSES)] + [wall_boss(red)]

def _pilots(m, pts):
    for x, y in pts:
        m = m - cyl_z(x, y, Z_TOP - 12.0, Z_TOP + 1, BOSS_PILOT, 16)
    return m

# ============================================================ vents (the fans on the rear cross member blow -x)
VENT_W, VENT_PITCH = 2.5, 5.0             # vertical strip slots in the x walls
VENT_Z0 = FLOOR_Z + T + 2.0               # 2.0 above the floor top
VENT_ZT = Z_TOP - 4.0                     # below the lid lip (z 56..58)
VENT_EDGE = 1.5                           # web to every cut-out, boss pad, corner arc and boundary wall

def vent_slots(red):
    """[(x wall, side, y centre, z0, z1)] of the strip slots; below the LRS wire cut-outs only up to wire_z - 2.
    Red: -x wall at the LRS and +x wall at the fan ducts (fan 4 blows on it); DC: -x wall at the LRS (its +x wall faces the RS case)"""
    top = Y_RED - R_BASE - BOSS_R - VENT_EDGE
    if red:
        walls = [(X0, -1, RW[1] + VENT_EDGE, top, (RW[1], LRS["y_red"]), LRS["wire_z"]),
                 (X1R, 1, Y_P + R_BASE + VENT_EDGE, top, None, None)]
    else:
        walls = [(X0, -1, Y_DC + R_BASE + BOSS_R + VENT_EDGE, YW[0] - VENT_EDGE, (LRS["y_dc"] + 2.0, YW[0]), LRS["wire_z"])]
    out = []
    for xw, side, y_lo, y_hi, cut, wz in walls:
        n = int((y_hi - y_lo - VENT_W) // VENT_PITCH) + 1
        off = (y_hi - y_lo - VENT_W - (n - 1) * VENT_PITCH) / 2       # centred in the free band
        for k in range(n):
            y = y_lo + off + VENT_W / 2 + k * VENT_PITCH
            under = cut is not None and cut[0] - VENT_EDGE < y + VENT_W / 2 and y - VENT_W / 2 < cut[1] + VENT_EDGE
            out.append((xw, side, y, VENT_Z0, wz - 2.0 if under else VENT_ZT))
    return out

def _vents(b, red):
    for xw, side, y, z0, z1 in vent_slots(red):
        xa, xb = (xw - 1, xw + T + 1) if side < 0 else (xw - T - 1, xw + 1)
        b = b - box(xa, xb, y - VENT_W / 2, y + VENT_W / 2, z0, z1)
    return b

# ============================================================ bases
def _shell(red):
    """floor + walls of a box, corner pads and the wall boss filled, RS block cut-out"""
    bp = _plan(red)
    cav = bp.offset(-T, JoinType.Miter) - _pads(RED_BOSSES if red else DC_BOSSES, BOSS_R) - _wall_boss(red)
    b = _vz(bp, FLOOR_Z, Z_TOP) - _vz(cav, FLOOR_Z + T, Z_TOP + 1)
    return b - box(BLK_CUT[0], BLK_CUT[1], Y_P - 1, BLK_CUT[2], BLK_Z, Z_TOP + 1)    # RS block through pocket wall and divider

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
    b = _shell(True)
    b = b - box(X0 - 1, X0 + w + 1, RW[1], LRS["y_red"], LRS["wire_z"], Z_TOP + 1)       # wires from the LRS AC terminals
    b = b - box(ENTRY[0], ENTRY[1], Y_RED - w - 1, Y_RED + 1, ENTRY[2], Z_TOP + 1)
    b = b - box(PE_SLOT[0], PE_SLOT[1], Y_RED - w - 1, Y_RED + 1, PE_SLOT[2], Z_TOP + 1)
    b = _pilots(b, _bosses(True)) + _wago_pockets()
    tie = box(ENTRY[0] + 1.0, ENTRY[1] - 1.0, Y_RED - w - 7.0, Y_RED - w - 1.0, FLOOR_Z + T, 29.0)   # strain relief for the chain cable
    tie = tie - box(ENTRY[0], ENTRY[1], Y_RED - w - 5.5, Y_RED - w - 2.5, 24.0, 26.5)              # zip-tie tunnel along x
    b = b + tie
    return _vents(b, True)

def dc_base():
    w = T
    b = _shell(False)
    b = b - box(X0 - 1, X0 + w + 1, LRS["y_dc"] + 2.0, YW[0], LRS["wire_z"], Z_TOP + 1)      # LRS DC terminals
    b = b - box(DUCT_WIN[0], DUCT_WIN[1], Y_DC - 1, Y_DC + w + 1, DUCT_WIN[2], DUCT_WIN[3])
    b = _pilots(b, _bosses(False)) + spout()
    return _vents(b, False)

def spout_section():
    """(y, z) section: floor top -> quarter round (R 4) -> hook behind the duct wall (45 deg tip), bridge over the wall, skirt"""
    import math
    yi, yo = DUCT_Y1 - DUCT_WALL - SPOUT_GAP, DUCT_Y1 + SPOUT_GAP      # 471.2 hook face / 473.2 skirt face
    zf = FLOOR_Z + T                                                   # 17.5 = floor top = window bottom
    cy, cz = yo + 0.3, zf - SPOUT_R                                    # arc centre (473.5, 13.5)
    arc = [(cy + SPOUT_R * math.cos(math.radians(90 + 90 * j / 8)), cz + SPOUT_R * math.sin(math.radians(90 + 90 * j / 8))) for j in range(9)]
    tip = cy - SPOUT_R
    return [(Y_DC + T, SPOUT_Z0), (Y_DC + T, zf)] + arc + [(yi, cz - (yi - tip)), (yi, FLOOR_Z), (yo, FLOOR_Z), (yo, SPOUT_Z0)]

def spout():
    import numpy as np
    x0, x1 = DUCT_WIN[0], DUCT_WIN[1]
    cs = CrossSection([_ccw(spout_section())])
    return Manifold.extrude(cs, x1 - x0).transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=float))

# ============================================================ lids (roof + LRS port cover + skirts)
BOLT = [(-1.0, 6.0), (3.0, 6.0), (0.6, 0.8), (3.2, 0.8), (-1.2, -7.0), (0.0, -1.2), (-2.8, -1.2)]   # engraved mains bolt

def _lid(red):
    plan = _plan(red, hood=True)
    ring = plan - plan.offset(-T, JoinType.Miter)
    big = 2000.0
    m = _vz(plan, Z_TOP, Z_TOP + LID_T)
    m = m + _vz(ring ^ _rect(-big, X0, -big, big), LRS["top"] + 0.6, Z_TOP)                          # onto the LRS case
    wy = RW if red else YW
    m = m + box(LRS["x_hood"] + 1.0, X0, *wy, 49.0, Z_TOP)                                           # own boundary skirt over the LRS block
    # skirts over the RS block: close the cut-out in the pocket wall and in the divider down to the block top
    px = (XD + 0.1, BLK_CUT[1]) if red else (BLK_CUT[0], XD - 0.1)
    dx = (XD + 0.1, XD + 0.1 + T) if red else (XD - 0.1 - T, XD - 0.1)
    m = m + box(*px, Y_P, Y_P + T, BLK_SKIRT_Z, Z_TOP) + box(*dx, Y_P, BLK_CUT[2], BLK_SKIRT_Z, Z_TOP)
    if red:
        for x0, x1, zb in ((ENTRY[0] + 0.3, ENTRY[1] - 0.3, 41.0), (PE_SLOT[0] + 0.3, PE_SLOT[1] - 0.3, 30.0)):
            m = m + box(x0, x1, Y_RED - T, Y_RED, zb, Z_TOP)                                          # tongues down to the cables
    cav = _plan(red).offset(-T, JoinType.Miter)
    lip = cav.offset(-0.3, JoinType.Miter) - cav.offset(-1.5, JoinType.Miter)
    lip = lip - _pads(RED_BOSSES if red else DC_BOSSES, BOSS_R + 0.3) - _wall_boss(red, SEAM_R + 0.3)
    m = m + _vz(lip, Z_TOP - 2.0, Z_TOP)
    for x, y in _bosses(red):
        m = m - cyl_z(x, y, Z_TOP - 3, Z_TOP + 3, 3.4, 16)
    if red:
        bc = ((X0 + XD) / 2, (Y_DIV + Y_RED) / 2 + 4.0)
        sym = CrossSection([_ccw([(bc[0] + 2.0 * u, bc[1] + 2.0 * v) for u, v in BOLT])])
        m = m - _vz(sym, Z_TOP + LID_T - 0.6, Z_TOP + LID_T + 1)
    return m

def red_lid():
    return _lid(True)

def dc_lid():
    return _lid(False)
