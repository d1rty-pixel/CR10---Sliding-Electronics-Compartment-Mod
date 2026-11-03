"""Thin 230 V drag chain on the far side of the tray (high y, 2020 at y 605..625), its end brackets and the fixed channel.

Link and clamp: chain_link.Link (shared with the wide chain), thin parameter set.
"""
import math
import numpy as np
from manifold3d import Manifold, CrossSection
import cable
from cable_base import box, cyl_z, hex_z, _ccw, _plate_y, _prism_x
from chain_link import Link

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

# ============================================================ link (shared code: chain_link.Link, thin parameter set)
LINK = Link(R=R, pitch=PITCH, y_in=5.0, t=1.8, w0=12.5, w1=15.5)   # inner clear width 10, web 12.5..15.5 (user: pitch - 15 .. - 12)
Y_IN, T = LINK.Y_IN, LINK.T
Y_INNER, Y_GAP, Y_OUTER = LINK.Y_INNER, LINK.Y_GAP, LINK.Y_OUTER     # 5.0..6.8 / 6.8..7.1 / 7.1..8.9
W0, W1, O0, INNER_EXT, STOP_H = LINK.W0, LINK.W1, LINK.O0, LINK.INNER_EXT, LINK.STOP_H
CLAMP_X, CAP_Z = LINK.CLAMP_X, LINK.CAP_Z
_circ, _rect, _hole_cs, _plate, _pins = LINK.circ, LINK.rect, LINK.hole_cs, LINK.plate, LINK.pins

def link():
    return LINK.link()

def lid():
    return LINK.lid()

def hinge_sweep(max_deg, step=1.0):
    return LINK.hinge_sweep(max_deg, step)

def lid_print():
    return LINK.lid_print()

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
