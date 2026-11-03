"""Thin 230 V drag chain on the far side of the tray (high y, 2020 at y 605..625), its end brackets and the fixed channel.

Parametric link (not a scaled copy of the user link): pins on the rear (inner) plates, hole + snap slot in the front (outer)
plates, joggle web between them, short closed bar on the outer side of the bend, open inner side closed by an outer U clamp.
Chain frame: x along the chain, rear pivot at the origin, front pivot at (PITCH, 0, 0), bar on -z, open side +z.
"""
import math
import numpy as np
from manifold3d import Manifold, CrossSection
import cable
from cable import box, cyl_z, hex_z, _ccw, _plate_y, _prism_x

# ============================================================ placement (world mm)
CHAIN_Y = 615.0                      # slot centre of the 2020 on the tray; outer rail of the far slide starts at y 627
ZT = cable.CH_ZT                     # underside of the acrylic plate
R = 7.5                              # plate radius = half outer height (15)
ZU, ZL = 91.4, 34.7                  # pivot height upper / lower run -> arc radius 28.35: with full-height stop corners the joints
                                     # stick out about 2.6 mm in the arc, so the runs sit 3.1 below the plate / 2.2 above the 2020
PITCH, N_LINKS = 26.0, 12            # 12 links: arc centre x -138 (out) .. 60 (in), always in front of the fixed end
X_SHIFT = 45.0                       # thin chain 45 mm further forward than the wide one: its cable exit lands on the junction box
X_MOVING_EXT = cable.X_MOVING_EXT - X_SHIFT
TRAVEL = cable.TRAVEL
X_FIXED = cable.X_FIXED - X_SHIFT    # still the middle of the travel

# ============================================================ link
# Same scheme as the user component "Chain Link (new)" (data/chain_link_user.json, pitch 29.5, R 9), scaled by rule, not by stretching:
# inner plates (pins at the rear pivot) run to the front face of the web; on the bar half they reach back behind the pivot and stop
# against the web of the previous link. Outer plates (hole at the front pivot) are square at the front on the bar half and stop
# against the stepped rear of the next outer plate (bar half starts at R + 0.2 behind its pivot, open half only at the web);
# that step leaves the clamp window on the open side. Square stop corners are kept only STOP_H high (envelope in the arc).
Y_IN = 5.0                           # inner clear width 10
T = 1.8                              # plate thickness
GAP = 0.3
Y_INNER = (Y_IN, Y_IN + T)                          # inner plates with pins, 5.0..6.8
Y_GAP = (Y_INNER[1], Y_INNER[1] + GAP)              # filled only on the bar half and at the web
Y_OUTER = (Y_GAP[1], Y_GAP[1] + T)                  # outer plates with hole, 7.1..8.9
W0, W1 = 12.5, 15.5                  # web (user: 14.5..17.5 at pitch 29.5 = pitch - 15 .. pitch - 12)
OUT_GAP, IN_GAP = 0.2, 0.1           # stop clearances as on the user component
O0 = R + OUT_GAP                     # rear of the outer plate on the bar half
INNER_EXT = PITCH - W1 - IN_GAP      # inner plate behind the pivot on the bar half (10.4)
BAR = (2.5, W0 - 0.5, -R, -R + 2.0)  # closed bar between the inner plates, z -7.5..-5.5 -> clear height to the lid 10
STOP_H = R                           # square stop corners over the full bar half (anti-sag) as on the user component
PIN_D, HOLE_D, SLOT_W = 4.0, 4.4, 3.6
PIN_Y = (Y_INNER[1] - 0.8, Y_OUTER[1] - 0.4)

def _plate(cs, yr):
    m = Manifold()
    for y0, y1 in ((yr[0], yr[1]), (-yr[1], -yr[0])): m = m + _plate_y(cs, y0, y1)
    return m

def _circ(x, z, r, seg=48):
    return CrossSection.circle(r, seg).translate((x, z))

def _rect(x0, x1, z0, z1):
    return CrossSection.square((x1 - x0, z1 - z0)).translate((x0, z0))

def _pins(x, z):
    m = Manifold()
    for s in (-1, 1):
        ya, yb = s * PIN_Y[0], s * PIN_Y[1]
        m = m + cable.cyl_y(x, z, min(ya, yb), max(ya, yb), PIN_D)
    return m

def _hole_cs(x, z, slot=+1):
    sl = _rect(x - SLOT_W / 2, x + SLOT_W / 2, z if slot > 0 else z - R - 1, z + R + 1 if slot > 0 else z)
    return _circ(x, z, HOLE_D / 2, 24) + sl

def _inner_cs(px=0.0, x1=W1):
    return _circ(px, 0, R) + _rect(px, x1, -R, R) + _rect(px - INNER_EXT, px, -STOP_H, 0)

def _outer_cs(px, x0_bar, x0_open):
    """outer plate around the pivot px (hole); bar half from x0_bar, open half from x0_open, square stop corner in front"""
    return (_rect(x0_bar, px, -R, 0) + _rect(x0_open, px, 0, R) + _circ(px, 0, R) + _rect(px, px + R, -STOP_H, 0)) - _hole_cs(px, 0, +1)

# clamp window on the open half, outer face of the inner plates: between the round end of the previous outer plate and the own web
CLAMP_X = (R + 0.8, W0 - 0.3)
GROOVE_Z, GROOVE_D = (1.2, 3.2), 0.6
CAP_T, CAP_FIT = 1.8, 0.2            # clamp bow sunk into a notch in the open edge of the inner plates, flush with the link
CAP_Z = (R - CAP_T, R)

def link():
    """built from y slabs whose (x, z) sections meet exactly: unions of coplanar outer faces of mixed primitives leave slivers"""
    web = _rect(W0, W1, -R, R)
    m = _plate_y(_rect(*BAR), -Y_IN, Y_IN)
    m = m + _plate(_inner_cs(), Y_INNER) + _plate(_rect(O0, W0, -R, 0) + web, Y_GAP) + _plate(_outer_cs(PITCH, O0, W0) + web, Y_OUTER)
    m = m + _pins(0, 0)
    for s in (-1, 1):
        y0, y1 = sorted((s * (Y_INNER[1] - GROOVE_D), s * (Y_INNER[1] + 0.2)))
        m = m - box(CLAMP_X[0], CLAMP_X[1], y0, y1, GROOVE_Z[0], GROOVE_Z[1])
    return m - box(CLAMP_X[0], CLAMP_X[1], -Y_INNER[1] - 0.5, Y_INNER[1] + 0.5, CAP_Z[0] - CAP_FIT, R + 1)

# ---- lid: U clamp over the open side, arms on the outer face of the inner plates inside the clamp window, hooks in the grooves
ARM_Y = (Y_INNER[1] + 0.2, Y_INNER[1] + 1.4)        # 7.0..8.2, within the outer plate width
STUB_Z = (R - 3.0, CAP_Z[0])                        # closes the opening between the inner plates, clear height 10 below it
ARM_Z0 = 1.0

def lid():
    """constant section along x: built as one (y, z) cross-section and extruded once (no coplanar unions of separate solids)"""
    x0, x1 = CLAMP_X[0] + CAP_FIT, CLAMP_X[1] - CAP_FIT
    sq = lambda y0, y1, z0, z1: CrossSection.square((y1 - y0, z1 - z0)).translate((y0, z0))
    cs = sq(-ARM_Y[1], ARM_Y[1], CAP_Z[0], CAP_Z[1]) + sq(-(Y_IN - 0.2), Y_IN - 0.2, STUB_Z[0], CAP_Z[0] + 0.1)
    for s in (-1, 1):
        ya, yb = sorted((s * ARM_Y[0], s * ARM_Y[1]))
        cs = cs + sq(ya, yb, ARM_Z0, CAP_Z[1])
        yi, yt = s * (ARM_Y[0] + 0.5), s * (Y_INNER[1] - GROOVE_D + 0.1)    # hook tip 0.1 short of the groove bottom
        hook = [(yi, GROOVE_Z[0] + 0.2), (yt, GROOVE_Z[0] + 1.1), (yt, GROOVE_Z[1] - 0.2), (yi, GROOVE_Z[1] - 0.2)]   # ramp leads, flat face retains
        cs = cs + CrossSection([_ccw(hook)])
    return Manifold.extrude(cs, x1 - x0).transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=float))

def _bent(m, phi_deg):
    """m as the next link, pivot (PITCH, 0, 0), bent by phi towards the open side (+z)"""
    c, s = math.cos(math.radians(phi_deg)), math.sin(math.radians(phi_deg))
    return m.transform(np.array([[c, 0, -s, PITCH], [0, 1, 0, 0], [s, 0, c, 0]]))

def hinge_sweep(max_deg, step=1.0):
    """(first angle in 0..max_deg where two neighbours incl. clamps collide or None, stop engages within -1.5 deg)"""
    a = link() + lid()
    for k in range(int(max_deg / step) + 1):
        if (a ^ _bent(a, k * step)).volume() > 1e-3: return k * step, None
    return None, (link() ^ _bent(link(), -1.5)).volume() > 1e-3

def lid_print():
    return lid().rotate((180, 0, 0))

def chain_links(x_m):
    P, xc = cable.chain_pivots(x_m, n=N_LINKS, x_f=X_FIXED, chp=PITCH, zu=ZU, zl=ZL)
    lk, ld = link(), lid()
    out = []
    for k in range(N_LINKS):
        a, b = P[k], P[k + 1]; d = (b - a) / np.linalg.norm(b - a)
        M = np.array([[d[0], 0, -d[1], a[0]], [0, 1, 0, CHAIN_Y], [d[1], 0, d[0], a[1]]])
        out.append((f"Thin Link {k + 1:02d}", "Link", lk.transform(M)))
        out.append((f"Thin Lid {k + 1:02d}", "Lid", ld.transform(M)))
    return out, P, xc

# ============================================================ end brackets (world)
LANE_Y = (605.0, 627.0)              # 2020 starts at 605 (duct below), inner rail of the far slide starts at 627
SCREW_Y_FIXED = 607.0                # M3 from above through the acrylic plate; y < 618 (2040 on top of the plate beyond)

def bracket_fixed():
    """fork (hole plates, slot down) around the first pivot; body under the plate with two M3 + nut pockets; cable tunnel"""
    px, pz = X_FIXED, ZU
    x0, x1 = px + PITCH - W1, px + 44.0               # counterpart of the inner-plate stop of the first link (like a web)
    fork = _circ(px, pz, R) + _rect(px, x0 + 1.0, pz - R, pz + R) + _rect(px - R, px, pz, pz + STOP_H) - _hole_cs(px, pz, -1)
    body = box(x0, x1, 603.0, LANE_Y[0] + 20.0, pz - R, ZT)
    body = body - box(x0 - 1, x1 + 1, CHAIN_Y - Y_IN, CHAIN_Y + Y_IN, pz - 5.0, ZT - 2.0)  # tunnel 10 wide, 2 mm roof
    for x in (px + 22.0, px + 38.0):
        body = body - cyl_z(x, SCREW_Y_FIXED, pz - R - 1, ZT + 1, 3.4, 16) - hex_z(x, SCREW_Y_FIXED, pz - R - 1, pz - R + 2.4)
    return body + _plate(fork, Y_OUTER).translate((0, CHAIN_Y, 0))

GROOVE_R, GROOVE_W = 24.0, 9.6       # centre-line radius (> R_static 22 of the cable); 9.6 keeps the walls clear of the tongue plates

def bracket_moving(x_m=X_MOVING_EXT):
    """on the 2020 of the tray, two M3 into hammer nuts in its top slot (y 615); the cable leaves in a quarter turn through the
    -y face (x_m + 21..33) straight into the +y slot of the mains junction box"""
    pz = ZL
    xa = x_m + O0                     # body face = counterpart of the outer stop corner of the last link
    x1 = xa + 40.0
    tongue = _circ(x_m, pz, R) + _rect(x_m, xa + 1.0, pz - R, pz + R)
    m = _plate(tongue, Y_INNER).translate((0, CHAIN_Y, 0)) + _pins(x_m, pz).translate((0, CHAIN_Y, 0))
    body = box(xa, x1, LANE_Y[0], LANE_Y[0] + 20.0, 25.0, pz + R)
    yc = CHAIN_Y - GROOVE_R
    ro, ri = GROOVE_R + GROOVE_W / 2, GROOVE_R - GROOVE_W / 2
    zf = pz - 5.5                     # groove floor level with the link cavity
    ring = cyl_z(xa, yc, zf, pz + R + 1, 2 * ro, 96) - cyl_z(xa, yc, zf - 1, pz + R + 2, 2 * ri, 96)
    body = body - (ring ^ box(xa - 1, x1 + 1, yc, LANE_Y[1], zf, pz + R + 1))      # starts 1 mm in front of the face: no coplanar cut
    for dx in (23.0, 34.0):
        x = xa + dx
        body = body - cyl_z(x, CHAIN_Y, 24, pz + R + 1, 3.4, 16) - cyl_z(x, CHAIN_Y, 29.0, pz + R + 1, 6.4, 16)
    return body + m

# ============================================================ fixed channel under the acrylic plate
CH_W, CH_WALL, CH_FLANGE = 14.0, 2.0, 13.5           # trough outer width, wall, flange half width
CH_ZB = ZT - 15.5                                     # underside of the floor (z 86.5)
SWITCH_Y = 558.0 - 4.6                                # centre of the switch in the swapped switch plug
# plan path: straight along y=CHAIN_Y, one L turn at the rear, short leg towards -y ending in front of the switch
L_R = 30.0                                            # turn radius > R_static 22
X_LEG = 410.0                                         # leg centre: flange (+-13.5) and screw bosses stay in front of the 2020 at x 425..445
Y_END = SWITCH_Y + 20.0                               # open end; the cable turns freely to +x (R >= 22) and drops to the switch
CH_END_X = X_LEG + 7.0                                # rearmost trough wall
CH_SPLIT = 262.0                                      # two parts (about 150 mm each): the whole channel is longer than the bed
CH_SCREWS = ((145.0, CHAIN_Y - 9.5), (235.0, CHAIN_Y - 9.5), (290.0, CHAIN_Y - 9.5), (350.0, CHAIN_Y - 9.5),
             (X_LEG - 9.5, Y_END + 6.0))

def _band(x0, hw, ext=0.0):
    """plan shape of the path buffered by hw; ext lengthens the open end (for the inner cut)"""
    xc, yc = X_LEG - L_R, CHAIN_Y - L_R
    ring = CrossSection.circle(L_R + hw, 128) - CrossSection.circle(L_R - hw, 128)
    ring = (ring ^ CrossSection.square((L_R + hw + 1, L_R + hw + 1))).translate((xc, yc))
    s = CrossSection.square((xc - x0, 2 * hw)).translate((x0, CHAIN_Y - hw)) + ring
    return s + CrossSection.square((2 * hw, yc - Y_END + ext)).translate((X_LEG - hw, Y_END - ext))

def _vz(cs, z0, z1):
    return Manifold.extrude(cs, z1 - z0).translate((0, 0, z0))

def channel(x0):
    hw = CH_W / 2
    ch = _vz(_band(x0, hw), CH_ZB, ZT) - _vz(_band(x0 - 1, hw - CH_WALL, 1.0), CH_ZB + CH_WALL, ZT + 1)
    ch = ch + (_vz(_band(x0, CH_FLANGE), ZT - 2.3, ZT) - _vz(_band(x0 - 1, hw - CH_WALL, 1.0), ZT - 3, ZT + 1))
    for x, y in CH_SCREWS:
        ch = ch + cyl_z(x, y, ZT - 6, ZT - 1, 8.0)
    for x, y in CH_SCREWS:
        ch = ch - cyl_z(x, y, ZT - 7, ZT + 1, 3.4, 16) - hex_z(x, y, ZT - 7, ZT - 4.3)
    ramp = _prism_x([(Y_END + 9.0, CH_ZB - 0.3), (Y_END - 0.3, CH_ZB - 0.3), (Y_END - 0.3, CH_ZB + 9.0)],   # floor ramp at the open end
                    X_LEG - hw - 1, X_LEG + hw + 1)
    return ch - ramp

def channel_parts(x0):
    """front and rear part, 0.2 mm butt gap at CH_SPLIT"""
    ch = channel(x0); big = 1000.0
    return (ch ^ box(-big, CH_SPLIT - 0.1, -big, big, -big, big)), (ch ^ box(CH_SPLIT + 0.1, big, -big, big, -big, big))

def channel_x0():
    return bracket_fixed().bounding_box()[3] + 0.5
