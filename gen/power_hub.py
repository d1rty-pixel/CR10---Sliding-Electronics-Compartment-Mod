"""Power hub (world mm, tray fully out): three red 230 V boxes plus the AC duct (tray.ac_duct), user 2026-11-04. They replace the
red mains box and the DC box with the L-shaped divider.

- WAGO box against the 2020 of the tray (+y face 604, profile from 604.8) between the PSUs: the thin chain cable comes in through
  its +y wall (ENTRY, zip-tie strain relief), PE leaves through PE_SLOT to the ring lug on the 2020. The three WAGO 221 lie flat on
  a shelf at the -y wall, levers up, conductor entries +y; their tops stand 0.5 over the lid, which is open around each of them
  (measuring with a meter without opening the box).
- LRS box in front of the LRS-350 terminals (+x), AC and DC together with a low divider on the AC / DC boundary (y 557). Port hood
  over the terminal block like before. AC to the WAGO box through aligned windows in the two touching walls, DC down through a spout
  into the DC duct (tray.DC).
- RS box in front of the RS-15-5 terminals. The RS-15-5 is turned 90 deg counter-clockwise against T-033 (user 2026-11-04):
  terminals -x, i.e. the orientation of the STEP before T-033, shifted to x end 9.05 / y 475.5. Low divider between FG and -V,
  DC down through a spout into the DC duct, AC from the AC duct through its -x wall.
- AC duct: L from the -y wall of the WAGO box, centred between the terminal faces of the two PSUs, to the -x wall of the RS box.

Wires are screwed to the PSU terminals with insulated fork lugs: every PSU box keeps the lug plus a bend (R >= 4 x D) free in
front of the terminals (LUG_L, BEND_R; assumptions, see docs/COMPONENTS.md).
All boxes clip onto the power rails (tray.POWER_RAILS) with the DIN clips of tray.py (CLIPS), floor on the clip base, lids with M3.
"""
from manifold3d import Manifold, CrossSection, JoinType
from cable import box, cyl_z, _ccw, _plate_y

FLOOR_Z, T, LID_T = 15.9, 1.6, 1.6         # clip base top is z 16 (tray.CLIP_TOP): 0.1 overlap so the clip fuses
Z_TOP = 58.0                              # top of the base walls = underside of the lids (LRS top 55.9, RS top 53.0)
# LRS-350 x -373.75..-158.75 (user 2026-11-03: about 5 mm from the drawer frame, inside -378.8); shift against the vendor STEP
# placement (-364..-149). Binary-exact on purpose: -9.8 left float noise that IngeTrazo turned into zero-length edges on the lids.
LRS_DX = -9.75
Y_DC, Y_TOP = 475.0, 604.0                # -y face of the PSU boxes (DC duct up to 473) / +y face (2020 of the tray from 604.8)
Y_DIV = 557.0                             # AC / DC boundary of the LRS terminal block (FG 561.75 / -V 552.25)

# LRS terminal block (vendor STEP as placed in the document): x -175.85..-161.25, y 498.5..585.5, case top 55.9
LRS = dict(x_hood=-168.0 + LRS_DX, top=55.9, y_red=590.0, y_dc=497.0, wire_z=30.0, block_x=(-175.85, -161.25))

# RS-15-5: vendor STEP orientation (terminals -x, pins along y, L at +y), as placed before T-033: body x -36.6..26.06,
# y 530.75..581.85, z 25..53; block x -48.5..-36.6, y 540.84..580.5, z 30.59..43.75; pins y 576.0 L / 568.4 N / 560.8 FG /
# 553.1 -V / 545.5 +V (docs/COMPONENTS.md). Shifted by RS_SHIFT: body x end 9.05 (fan power lane from 10.2), body y from 475.5
# (DC duct to 473).
RS_SHIFT = (-17.01, -55.25)
def rs_xy(x, y):
    """RS position before T-033 (terminals -x) -> current position"""
    return (x + RS_SHIFT[0], y + RS_SHIFT[1])
_b0, _b1 = rs_xy(-36.6, 530.75), rs_xy(26.06, 581.85)
RS_BODY = (_b0[0], _b1[0], _b0[1], _b1[1], 25.0, 53.0)                 # x -53.61..9.05, y 475.5..526.6
_k0, _k1 = rs_xy(-48.5, 540.84), rs_xy(-36.6, 580.5)
RS_BLOCK = (_k0[0], _k1[0], _k0[1], _k1[1], 30.59, 43.75)              # x -65.51..-53.61, y 485.59..525.25
RS_PINS = {n: rs_xy(0, y)[1] for n, y in (("L", 576.0), ("N", 568.4), ("FG", 560.8), ("-V", 553.1), ("+V", 545.5))}

# fork lugs (assumption, not measured): insulated, 0.5-1.5 mm2, M3.5 (LRS) / M3 (RS), 18 from the screw centre to the end of the
# sleeve; screw centre = middle of the terminal block (assumption). Behind the sleeve the core bends with R >= 4 x D (wiring.py).
LUG_L, BEND_R, CORE_D = 18.0, 12.0, 3.0
LUG_FREE = BEND_R + CORE_D / 2            # free run behind the sleeve for a 90 deg bend
LRS_LUG_END = sum(LRS["block_x"]) / 2 + LUG_L         # -150.55 (wires leave +x)
RS_LUG_END = (RS_BLOCK[0] + RS_BLOCK[1]) / 2 - LUG_L  # -77.56 (wires leave -x)
BLK_Z = 30.0                              # cut-out for the RS block in the +x wall from here up (block bottom 30.59)
BLK_M = 0.3                               # play around the block in y (0.5 put a vertex 0.09 from the corner boss pad)
BLK_SKIRT_Z = RS_BLOCK[5] + 0.5           # lid skirt in the cut-out stops 0.5 over the block
DIV_Z = 48.0                              # top of the low AC / DC dividers (10 under the lid)

# ---------------------------------------------------------------- box extents
R_BASE, R_CORNER, BOSS_R, BOSS_PILOT = 6.0, 3.0, 4.0, 2.8
X0L = -148.5 + LRS_DX                     # -158.25: LRS box -x face, 0.5 to the LRS case end
X1L = -126.0                              # LRS box +x face: 23.6 behind the lug end (LUG_FREE 13.5)
X0R = -95.0                               # RS box -x face: 15.9 in front of the lug end
X1R = RS_BODY[0] - 0.5                    # RS box +x face, 0.5 to the RS case (the terminal block passes through its cut-out)
Y1R = 538.0                               # RS box +y face (rail A clip latch to 536.7)
RW = (Y_DIV + 0.1, Y_DIV + 0.1 + T)       # -y wall of the WAGO box (557.1..558.7)
X0W = X1L + 0.2                           # WAGO box -x face, 0.2 to the LRS box

# AC duct (tray.ac_duct): vertical leg centred between the terminal faces of the PSUs, horizontal leg on the RS AC pins
AC_XC = round((LRS["block_x"][1] + RS_BLOCK[0]) / 2, 1)   # -113.4
AC_W, AC_GAP = 20.0, 0.2                  # outer width like every duct; 0.2 joint to the box walls
AC_X = (AC_XC - AC_W / 2, AC_XC + AC_W / 2)
AC_YC = (RS_PINS["L"] + RS_PINS["FG"]) / 2
AC_Y = (AC_YC - AC_W / 2, AC_YC + AC_W / 2)
AC_ZT = FLOOR_Z + 25.0                    # wall top (duct height 25 like the other ducts), lid on top

# ---------------------------------------------------------------- WAGO 221 lying on a shelf, tops through the lid
# (name, width): 221-413 18.7 x 18.6 x 8.3 (width x length x thickness), 221-414 width 24.9 assumed. Length along y, conductor
# entries at +y, levers on the top face; the test slots are assumed reachable from the top / the entry face (not verified).
WAGOS = [("L", 18.7), ("N", 18.7), ("PE", 24.9)]
W_LEN, W_THK, RIB, FIT, W_GAP = 18.6, 8.3, 1.6, 0.2, 3.0
W_OUT = 6.0                               # rear end (lever pivots) sticks out of the -y wall (user 2026-11-04): pressing the levers
W_Y0 = RW[0] - W_OUT                      # shut loads the shelf where it runs through the wall
W_ZT = Z_TOP + LID_T + 0.5                # WAGO top 0.5 over the lid (60.1)
W_Z0 = W_ZT - W_THK                       # 51.8 = shelf top
SHELF_T = 2.4                             # shelf plate (T-039: closing the levers takes force)
GUS_W = 2.4                               # 45 deg gussets: under the outer ribs and the middle of every WAGO; between two pockets
                                          # one gusset over both ribs and the gap
W_FRONT = W_Y0 + W_LEN + FIT              # front stop lips from here (1.2 thick, 1.0 high)
PROBE = 5.0                               # lid opening in front of the entry face (test probe)
W_X0 = AC_X[1]                            # first rib: web 1.6 to the AC duct window in the -y wall

def wago_slots():
    """[(name, x0, x1)] of the WAGO bodies, from W_X0 to +x, each pocket with its own two ribs"""
    x = W_X0; out = []
    for n, w in WAGOS:
        out.append((n, x + RIB + FIT, x + RIB + FIT + w)); x += w + 2 * FIT + 2 * RIB + W_GAP
    return out

def _pocket_x(n):
    a, b = [(a, b) for m, a, b in wago_slots() if m == n][0]
    return a - FIT - RIB, b + FIT + RIB
W_X1 = _pocket_x(WAGOS[-1][0])[1]
X1W = W_X1 + 1.0 + BOSS_R + R_BASE        # corner boss 1.0 clear of the last rib

ENTRY = (-109.0, -94.0, 27.0)             # chain cable (thin bracket exit x -108..-96, z 29..39)
PE_SLOT = (-80.0, -74.0, 22.0)            # PE to the ring lug on the tray 2020; +x of the moving chain bracket (x <= -80.8)
WIN_LW = (562.0, 591.0, 20.0, 53.0)       # window LRS box <-> WAGO box (y0, y1, z0, z1): LRS AC pins 561.75..580.75

# ---------------------------------------------------------------- DC spouts into the DC duct (tray.DC)
DUCT_Y1, DUCT_WALL = 473.0, 1.6          # outer +y face and wall of the DC duct (tray.DC yc 463, DUCT_W 20)
SPOUT_R, SPOUT_GAP, SPOUT_Z0 = 4.0, 0.2, 6.0
NOTCH_Z = FLOOR_Z - SPOUT_GAP            # 15.7: top of the notched duct wall under the spout bridge
DUCT_WIN_Z = (FLOOR_Z + T, 29.0)          # window over the spout: floor top .. 1 under the duct lid (tray: wall top 30)
VENT_EDGE = 1.5
SPOUTS = {"LRS": (X0L + R_BASE + 0.75, X1L - R_BASE - BOSS_R - VENT_EDGE),     # -151.5..-137.5 (DC wires leave the lugs at -x)
          "RS": (X0R + R_BASE + 1.0, X1R - R_BASE - BOSS_R - VENT_EDGE)}       # -88.0..-65.6

# ---------------------------------------------------------------- bosses (corner: x, y, sx, sy towards the two walls)
BOSSES = {"LRS": ((X0L + R_BASE, Y_TOP - R_BASE, -1, 1), (X1L - R_BASE, Y_TOP - R_BASE, 1, 1), (X1L - R_BASE, Y_DC + R_BASE, 1, -1)),
          "RS": ((X0R + R_BASE, Y1R - R_BASE, -1, 1), (X1R - R_BASE, Y1R - R_BASE, 1, 1), (X1R - R_BASE, Y_DC + R_BASE, 1, -1)),
          "WAGO": ((X0W + R_BASE, Y_TOP - R_BASE, -1, 1), (X1W - R_BASE, Y_TOP - R_BASE, 1, 1), (X1W - R_BASE, RW[0] + R_BASE, 1, -1))}
WALL_R = 3.5
WALL_BOSSES = {"LRS": ((X1L - T - 2.0, 530.0, 1, 0),), "RS": (), "WAGO": ()}   # (x, y, sx, sy): band towards the wall

# ---------------------------------------------------------------- DIN clips (tray.py): (rail "A"/"B", x0, x1, release slot x)
def _mid(a, b):
    return (a + b) / 2
CLIPS = {"LRS": (("A", X0L + 6.0, X1L - 6.0, _mid(X0L, X1L)), ("B", X0L + 6.0, X1L - 6.0, _mid(X0L, X1L))),
         "RS": (("A", X0R + 6.0, X1R - 6.0, _mid(X0R, X1R)),),
         "WAGO": (("B", -100.0, -86.0, -89.0), ("B", X1W - 20.0, X1W - 6.0, X1W - 17.0)),   # release slots clear of the tie block
         "AC": (("A", AC_X[0] + 2.0, AC_X[1] - 2.0, AC_XC),)}

def box_extent(name):
    """(x0, x1, y0, y1) of a box base"""
    return {"LRS": (X0L, X1L, Y_DC, Y_TOP), "RS": (X0R, X1R, Y_DC, Y1R), "WAGO": (X0W, X1W, RW[0], Y_TOP)}[name]

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

def _plan(name, hood=False):
    """outer plan of a box; LRS with hood: plus the port cover over the LRS terminal block (lid)"""
    x0, x1, y0, y1 = box_extent(name)
    b, c = R_BASE, R_CORNER
    if name == "LRS" and hood:
        L = LRS
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, L["y_red"]), (L["x_hood"], L["y_red"]), (L["x_hood"], L["y_dc"]), (x0, L["y_dc"])]
        return _rounded(pts, [b, b, b, b, 0, c, c, 0])
    return _rounded([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], b)

def _pads(corners, r):
    """corner boss with its wedge to both walls: circle r plus the two rectangles between its tangent points and the walls"""
    cs = CrossSection()
    for cx, cy, sx, sy in corners:
        far = 20.0
        xa = sorted((cx, cx + sx * far)); ya = sorted((cy - sy * r, cy + sy * far))
        xb = sorted((cx - sx * r, cx + sx * far)); yb = sorted((cy, cy + sy * far))
        cs = cs + CrossSection.circle(r, 24).translate((cx, cy)) + _rect(*xa, *ya) + _rect(*xb, *yb)
    return cs

def _wall_pads(name, r=WALL_R):
    """wall boss: circle plus a band into the wall (band edges on the circle's 0/180 deg vertices)"""
    cs = CrossSection()
    for x, y, sx, sy in WALL_BOSSES[name]:
        band = _rect(*sorted((x, x + sx * 4.0)), y - r, y + r) if sx else _rect(x - r, x + r, *sorted((y, y + sy * 4.0)))
        cs = cs + CrossSection.circle(r, 24).translate((x, y)) + band
    return cs

def _bosses(name):
    return [c[:2] for c in BOSSES[name]] + [c[:2] for c in WALL_BOSSES[name]]

def _shell(name):
    """floor + walls, boss pads filled, pilot holes"""
    bp = _plan(name)
    cav = bp.offset(-T, JoinType.Miter) - _pads(BOSSES[name], BOSS_R) - _wall_pads(name)
    b = _vz(bp, FLOOR_Z, Z_TOP) - _vz(cav, FLOOR_Z + T, Z_TOP + 1)
    for x, y in _bosses(name):
        b = b - cyl_z(x, y, Z_TOP - 12.0, Z_TOP + 1, BOSS_PILOT, 16)
    return b

# ============================================================ vents (the fans on the rear cross member blow -x)
VENT_W, VENT_PITCH = 2.5, 5.0             # vertical strip slots in the x walls (across the air stream)
VENT_Z0 = FLOOR_Z + T + 2.0               # 2.0 above the floor top
VENT_ZT = Z_TOP - 4.0                     # below the lid lip (z 56..58)

def _vent_walls(name):
    """[(x of the wall face, side, y_lo, y_hi, full exclusions [(y0, y1)], low zones [(y0, y1, z_top)])]. y_lo/y_hi stop VENT_EDGE
    before the corner arcs / boss pads; exclusions are windows, wall bosses and dividers fused to the wall."""
    e, c = VENT_EDGE, R_BASE + BOSS_R + VENT_EDGE
    if name == "LRS":       # +x: to the AC duct / WAGO box (its window is the passage there); -x: under the LRS terminal cut-out
        wb = WALL_BOSSES["LRS"][0][1]
        return [(X1L, 1, Y_DC + c, Y_TOP - c, [(wb - WALL_R, wb + WALL_R), (Y_DIV - 0.8, Y_DIV + 0.8), WIN_LW[:2]], []),
                (X0L, -1, Y_DC + R_BASE + e, Y_TOP - c, [], [(LRS["y_dc"] + 2.0, LRS["y_red"], LRS["wire_z"] - 2.0)])]
    if name == "RS":        # -x only: the +x wall stands 0.5 in front of the RS case, slots there would be covered
        yd = rs_div_y()
        return [(X0R, -1, Y_DC + R_BASE + e, Y1R - c, [(yd - 0.8, AC_Y[1] - T)], [])]
    # WAGO: +x towards the fans; the -x wall is mostly the window into the LRS box
    return [(X1W, 1, RW[0] + c, Y_TOP - c, [], [])]

def vent_slots(name):
    """[(x wall, side, y centre, z0, z1)]: slots centred in every free stretch of a wall"""
    out = []
    for xw, side, lo, hi, full, low in _vent_walls(name):
        cuts = sorted((a - VENT_EDGE, b + VENT_EDGE) for a, b in full)
        segs, y = [], lo
        for a, b in cuts:
            if a > y: segs.append((y, min(a, hi)))
            y = max(y, b)
        if y < hi: segs.append((y, hi))
        for y0, y1 in segs:
            if y1 - y0 < VENT_W: continue
            n = int((y1 - y0 - VENT_W) // VENT_PITCH) + 1
            off = (y1 - y0 - VENT_W - (n - 1) * VENT_PITCH) / 2
            for k in range(n):
                yc = y0 + off + VENT_W / 2 + k * VENT_PITCH
                z1 = VENT_ZT
                for a, b, zt in low:
                    if a - VENT_EDGE < yc + VENT_W / 2 and yc - VENT_W / 2 < b + VENT_EDGE: z1 = min(z1, zt)
                out.append((xw, side, yc, VENT_Z0, z1))
    return out

def _vents(b, name):
    for xw, side, y, z0, z1 in vent_slots(name):
        xa, xb = (xw - 1, xw + T + 1) if side < 0 else (xw - T - 1, xw + 1)
        b = b - box(xa, xb, y - VENT_W / 2, y + VENT_W / 2, z0, z1)
    return b

# ============================================================ DC spouts
def spout_section():
    """(y, z) section: floor top -> quarter round (R 4) -> hook behind the duct wall (45 deg tip), bridge over the wall, skirt"""
    import math
    yi, yo = DUCT_Y1 - DUCT_WALL - SPOUT_GAP, DUCT_Y1 + SPOUT_GAP      # 471.2 hook face / 473.2 skirt face
    zf = FLOOR_Z + T                                                   # 17.5 = floor top = window bottom
    cy, cz = yo + 0.3, zf - SPOUT_R                                    # arc centre (473.5, 13.5)
    arc = [(cy + SPOUT_R * math.cos(math.radians(90 + 90 * j / 8)), cz + SPOUT_R * math.sin(math.radians(90 + 90 * j / 8))) for j in range(9)]
    tip = cy - SPOUT_R
    return [(Y_DC + T, SPOUT_Z0), (Y_DC + T, zf)] + arc + [(yi, cz - (yi - tip)), (yi, FLOOR_Z), (yo, FLOOR_Z), (yo, SPOUT_Z0)]

def spout(x0, x1):
    import numpy as np
    cs = CrossSection([_ccw(spout_section())])
    return Manifold.extrude(cs, x1 - x0).transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=float))

def _spout_window(b, name):
    x0, x1 = SPOUTS[name]
    return b - box(x0, x1, Y_DC - 1, Y_DC + T + 1, *DUCT_WIN_Z) + spout(x0, x1)

# ============================================================ bases
def lrs_base():
    b = _shell("LRS")
    b = b - box(X0L - 1, X0L + T + 1, LRS["y_dc"] + 2.0, LRS["y_red"], LRS["wire_z"], Z_TOP + 1)    # wires from the LRS terminals
    b = b - box(X1L - T - 1, X1L + 1, WIN_LW[0], WIN_LW[1], WIN_LW[2], WIN_LW[3])                  # AC to the WAGO box
    b = b + box(LRS_LUG_END + VENT_EDGE, X1L - T + 0.05, Y_DIV - 0.8, Y_DIV + 0.8, FLOOR_Z + T - 0.05, DIV_Z)   # AC / DC divider
    return _vents(_spout_window(b, "LRS"), "LRS")

def rs_div_y():
    return (RS_PINS["FG"] + RS_PINS["-V"]) / 2

def rs_base():
    b = _shell("RS")
    b = b - box(X1R - T - 1, X1R + 1, RS_BLOCK[2] - BLK_M, RS_BLOCK[3] + BLK_M, BLK_Z, Z_TOP + 1)        # terminal block through the +x wall
    b = b - box(X0R - 1, X0R + T + 1, AC_Y[0] + T, AC_Y[1] - T, FLOOR_Z + T, AC_ZT)                # AC duct
    yd = rs_div_y()
    b = b + box(X0R + T - 0.05, RS_LUG_END - VENT_EDGE, yd - 0.8, yd + 0.8, FLOOR_Z + T - 0.05, DIV_Z)   # AC / DC divider
    return _vents(_spout_window(b, "RS"), "RS")


def _wago_shelf():
    """WAGO shelf through the -y wall (the WAGO rear ends stick out W_OUT, user 2026-11-04): inside on 45 deg gussets (outer ribs,
    WAGO middles, one wide gusset over the ribs and the gap between two pockets), outside on a 45 deg corbel along the wall.
    Ribs with snap noses over the top edge (rear part, just inside the wall), front stop lips under the entry face."""
    import numpy as np
    m = Manifold(); yw = RW[1] - 0.5                                   # 0.5 into the wall (0.05 left a T-junction vertex)
    zs = W_Z0 - SHELF_T; yf = W_FRONT + 1.2
    m = m + box(W_X0, W_X1, W_Y0, yf, zs, W_Z0)                        # shelf, through the wall
    def xprism(pts, x0, x1):
        cs = CrossSection([_ccw(pts)])
        return Manifold.extrude(cs, x1 - x0).transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=float))
    gus = [(yw, zs + 0.5), (yw, zs - (yf - 0.5 - yw)), (yf - 0.5, zs + 0.5)]          # inside, 45 deg, top edge in the shelf
    yo = RW[0] + 0.5
    corbel = [(yo, zs + 0.5), (W_Y0, zs + 0.5), (yo, zs - (yo - W_Y0))]           # outside, 45 deg, into the wall
    m = m + xprism(corbel, W_X0, W_X1)
    zr = W_ZT + 1.2                                                    # rib top
    px = [_pocket_x(n) for n, _ in WAGOS]
    for (p0, p1), nxt in zip(px, px[1:] + [None]):
        a, b = p0 + RIB + FIT, p1 - RIB - FIT
        xs = [(p0, p0 + GUS_W) if p0 == px[0][0] else None, ((a + b - GUS_W) / 2, (a + b + GUS_W) / 2),
              (p1 - RIB, nxt[0] + RIB) if nxt else (p1 - GUS_W, p1)]
        for g in xs:
            if g: m = m + xprism(gus, *g)
        for x0 in (p0, p1 - RIB):
            m = m + box(x0, x0 + RIB, yw, yf, W_Z0 - 0.5, zr)                                 # ribs, from the wall
        for xw, s in ((a - FIT, +1), (b + FIT, -1)):                   # inner face of the rib, s = direction into the pocket
            xo = xw - s * 0.05
            zt = W_ZT + 0.1
            nose = CrossSection([_ccw([(xo, zt), (xw + s * 0.6, zt), (xw, zr), (xo, zr)])])
            m = m + _plate_y(nose, RW[1] + 0.3, RW[1] + 4.3)
        m = m + box(a - FIT - 0.05, b + FIT + 0.05, W_FRONT, W_FRONT + 1.2, W_Z0 - 0.5, W_Z0 + 1.0)    # front stop
    return m

def wago_notches():
    """x ranges of the U notches in the -y wall the WAGOs pass through (between the rib faces), from the shelf top up"""
    return [(a - FIT, b + FIT) for _, a, b in wago_slots()]

def wago_base():
    b = _shell("WAGO")
    b = b - box(X0W - 1, X0W + T + 1, WIN_LW[0], WIN_LW[1], WIN_LW[2], WIN_LW[3])                  # AC from the LRS box
    b = b - box(AC_X[0] + T, AC_X[1] - T, RW[0] - 1, RW[1] + 1, FLOOR_Z + T, AC_ZT)               # AC duct
    b = b - box(ENTRY[0], ENTRY[1], Y_TOP - T - 1, Y_TOP + 1, ENTRY[2], Z_TOP + 1)
    b = b - box(PE_SLOT[0], PE_SLOT[1], Y_TOP - T - 1, Y_TOP + 1, PE_SLOT[2], Z_TOP + 1)
    tie = box(ENTRY[0] + 1.0, ENTRY[1] - 1.0, Y_TOP - T - 7.0, Y_TOP - T - 1.0, FLOOR_Z + T, 29.0)  # strain relief for the chain cable
    tie = tie - box(ENTRY[0], ENTRY[1], Y_TOP - T - 5.5, Y_TOP - T - 2.5, 24.0, 26.5)             # zip-tie tunnel along x
    for x0, x1 in wago_notches():
        b = b - box(x0, x1, RW[0] - 1, RW[1] + 1, W_Z0 - 0.5, Z_TOP + 1)       # notch bottom inside the shelf (no coplanar seam)
    return _vents(b, "WAGO") + tie + _wago_shelf()

# ============================================================ lids
BOLT = [(-1.0, 6.0), (3.0, 6.0), (0.6, 0.8), (3.2, 0.8), (-1.2, -7.0), (0.0, -1.2), (-2.8, -1.2)]   # engraved mains bolt
BOLT_AT = {"LRS": (_mid(X0L, X1L), 530.0), "RS": (_mid(X0R, X1R), 492.0), "WAGO": (-114.0, 588.0)}

def wago_openings():
    """lid openings around each WAGO pocket (ribs + 0.3), open at the -y edge (the WAGOs pass the wall), to PROBE in front of the entry face"""
    return [(p[0] - 0.3, p[1] + 0.3, RW[0] - 1.0, W_Y0 + W_LEN + PROBE) for p in (_pocket_x(n) for n, _ in WAGOS)]

def _lid(name):
    plan = _plan(name, hood=True)
    m = _vz(plan, Z_TOP, Z_TOP + LID_T)
    if name == "LRS":
        big = 2000.0
        ring = plan - plan.offset(-T, JoinType.Miter)
        m = m + _vz(ring ^ _rect(-big, X0L, -big, big), LRS["top"] + 0.6, Z_TOP)                      # hood onto the LRS case
        m = m + box(LRS["x_hood"] + 1.0, X0L, Y_DIV - 0.8, Y_DIV + 0.8, 49.0, Z_TOP)                    # divider over the block
    if name == "RS":
        m = m + box(X1R - T, X1R, RS_BLOCK[2] - BLK_M, RS_BLOCK[3] + BLK_M, BLK_SKIRT_Z, Z_TOP)             # closes the block cut-out
    if name == "WAGO":
        for x0, x1, zb in ((ENTRY[0] + 0.3, ENTRY[1] - 0.3, 41.0), (PE_SLOT[0] + 0.3, PE_SLOT[1] - 0.3, 30.0)):
            m = m + box(x0, x1, Y_TOP - T, Y_TOP, zb, Z_TOP)                                           # tongues down to the cables
    cav = _plan(name).offset(-T, JoinType.Miter)
    lip = cav.offset(-0.3, JoinType.Miter) - cav.offset(-1.5, JoinType.Miter)
    lip = lip - _pads(BOSSES[name], BOSS_R + 0.3) - _wall_pads(name, WALL_R + 0.3)
    m = m + _vz(lip, Z_TOP - 2.0, Z_TOP)
    if name == "WAGO":
        for x0, x1, y0, y1 in wago_openings():
            m = m - box(x0, x1, y0, y1, Z_TOP - 3, Z_TOP + LID_T + 1)
    for x, y in _bosses(name):
        m = m - cyl_z(x, y, Z_TOP - 3, Z_TOP + 3, 3.4, 16)
    bc = BOLT_AT[name]
    sym = CrossSection([_ccw([(bc[0] + 2.0 * u, bc[1] + 2.0 * v) for u, v in BOLT])])
    return m - _vz(sym, Z_TOP + LID_T - 0.6, Z_TOP + LID_T + 1)

def lrs_lid():
    return _lid("LRS")

def rs_lid():
    return _lid("RS")

def wago_lid():
    return _lid("WAGO")
