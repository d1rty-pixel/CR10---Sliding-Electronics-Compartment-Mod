"""Printed parts inside the tray (world mm, tray fully out): 230 V junction box, 24/5 V duct, data/bus duct, DIN rail holders.

Separation: mains only inside the red hub box (power_hub.py: WAGO 221-413 for L / N, 221-414 for PE, fed from the thin chain),
low voltage DC in the DC hub box and the DC duct, data and bus lines in the data duct along the wide chain (all anthracite). Purchased parts
(PSUs, Pi, Octopus, WAGO, rails, lugs) are models in the document (layers "Electronics (neu)" / "Electronics (vendor)").

Layout along x on the high-y side (tray inside x -378.8..31.2): LRS-350 x -373.75..-158.75 (terminals +x), hub x -158.25..-49,
RS-15-5 x -48.5..26.06 (terminals -x, y 530.8..581.8), about 5 mm to the drawer frame / rear cross member (hub.LRS_DX / RS_DX).
Four 60 x 60 x 25 fans (24 V PWM) on the rear cross member (2020 L=334 #1) blow -x into the tray, through the vented hub boxes.
"""
import math
import numpy as np
from manifold3d import Manifold, CrossSection
from cable import box, cyl_z, _ccw, _plate_y
import power_hub as hub

FLOOR_Z = 5.0                        # top of the tray floor plate
RAIL_TOP = 12.5                      # EN 50022 35 x 7.5 on the floor
# colour = filament (user 2026-11-03): anthracite for every inner part, theme orange outside (cr10mod.COL), red only for 230 V
COL_ANTHRACITE = (0.22, 0.23, 0.25)
COL_MAINS, COL_DC, COL_DATA, COL_DIN = (0.85, 0.1, 0.1), COL_ANTHRACITE, COL_ANTHRACITE, COL_ANTHRACITE

def _yz_prism(cs, x0, x1):
    """cross-section in (y, z) extruded along x over x0..x1"""
    return Manifold.extrude(cs, x1 - x0).transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=float))

def _sq(y0, y1, z0, z1):
    return CrossSection.square((y1 - y0, z1 - z0)).translate((y0, z0))

def _screw_down(x, y, z_top, depth=3.0):
    """M3 countersunk-ish hole from the top of a floor (z_top) down to the tray floor"""
    return cyl_z(x, y, FLOOR_Z - 1, z_top + 1, 3.4, 16) + Manifold.cylinder(depth, 1.7, 3.3, 16).translate((x, y, z_top - depth + 0.01))

# ============================================================ ducts (U channel with snap lid, finger slots)
DUCT_W, DUCT_H, DUCT_T = 20.0, 25.0, 1.6     # every duct z 5..30, lid to 31.6 (user 2026-11-03); the boards sit low (BOARD_Z),
                                             # so the finger slots (z 21..30) are at board level. Higher ducts would cover the fan outlets
SLOT_PITCH, SLOT_W, SLOT_D = 10.0, 3.0, 9.0

def _duct_x(x0, x1, yc, slots=True, keep=None):
    """straight duct along x, centre line yc; finger slots only where x is outside `keep` (corner zone)"""
    y0, y1 = yc - DUCT_W / 2, yc + DUCT_W / 2
    d = box(x0, x1, y0, y1, FLOOR_Z, FLOOR_Z + DUCT_H) - box(x0 - 1, x1 + 1, y0 + DUCT_T, y1 - DUCT_T, FLOOR_Z + 2.0, FLOOR_Z + DUCT_H + 1)
    if slots:
        n = int((x1 - x0 - 10) // SLOT_PITCH)
        for k in range(n):
            x = x0 + 5 + SLOT_PITCH * (k + 0.5)
            if keep and keep[0] - SLOT_W < x < keep[1] + SLOT_W: continue
            d = d - box(x - SLOT_W / 2, x + SLOT_W / 2, y0 - 1, y1 + 1, FLOOR_Z + DUCT_H - SLOT_D, FLOOR_Z + DUCT_H + 1)
    return d

def _duct_y(y0, y1, xc, slots=True, keep=None):
    x0, x1 = xc - DUCT_W / 2, xc + DUCT_W / 2
    d = box(x0, x1, y0, y1, FLOOR_Z, FLOOR_Z + DUCT_H) - box(x0 + DUCT_T, x1 - DUCT_T, y0 - 1, y1 + 1, FLOOR_Z + 2.0, FLOOR_Z + DUCT_H + 1)
    if slots:
        n = int((y1 - y0 - 10) // SLOT_PITCH)
        for k in range(n):
            y = y0 + 5 + SLOT_PITCH * (k + 0.5)
            if keep and keep[0] - SLOT_W < y < keep[1] + SLOT_W: continue
            d = d - box(x0 - 1, x1 + 1, y - SLOT_W / 2, y + SLOT_W / 2, FLOOR_Z + DUCT_H - SLOT_D, FLOOR_Z + DUCT_H + 1)
    return d

# data duct: from the wide chain bracket exit (x -56..-38, y 330) along the low-y edge to the Pi at the front (open front end)
WIDE_EXIT_X, WIDE_EXIT_Z = (-58.0, -37.0), 31.0   # wide chain bracket exit (x -60..-35, z 31.25..46.75, its +y face at y 330)
DATA = dict(x=(-300.0, -35.0), yc=340.0, screws=(-280.0, -190.0, -100.0))
# DC duct: straight along x between the PSUs and Octopus/Pi; the DC wires come in from the yellow hub box through its finger slots
DC = dict(yc=463.0, x=(-300.0, -45.0), screws=((-280.0, 463.0), (-210.0, 463.0), (-150.0, 463.0), (-60.0, 463.0)))

def _floor_screws(d, pts):
    for x, y in pts: d = d - _screw_down(x, y, FLOOR_Z + 2.0)
    return d

def _bead_grooves_x(d, x0, x1, yc):
    zt = FLOOR_Z + DUCT_H
    for s in (-1, 1):
        yw = yc + s * (DUCT_W / 2 - DUCT_T)
        y0, y1 = sorted((yw - s * 0.5, yw + s * 0.5))
        d = d - box(x0 - 1, x1 + 1, y0, y1, zt - 4.8, zt - 2.2)
    return d

def data_duct():
    """window in the -y wall where the wide chain bundle leaves its bracket (+y face at y 330, z 31.25..46.75)"""
    d = _bead_grooves_x(_duct_x(*DATA["x"], DATA["yc"]), *DATA["x"], DATA["yc"])
    if FLOOR_Z + DUCT_H > WIDE_EXIT_Z:                   # only when the wall reaches the exit
        d = d - box(*WIDE_EXIT_X, DATA["yc"] - DUCT_W / 2 - 1, DATA["yc"] - DUCT_W / 2 + DUCT_T + 1, WIDE_EXIT_Z, FLOOR_Z + DUCT_H + 1)
    return _floor_screws(d, [(x, DATA["yc"]) for x in DATA["screws"]])

NOTCH_X = (hub.DUCT_WIN[0] - hub.SPOUT_GAP, hub.DUCT_WIN[1] + hub.SPOUT_GAP)   # +y wall notch under the hub spout

def dc_duct():
    """both ends open (rear end takes the tongue of the Fan DC Duct); +y wall notched under the spout of the DC hub box"""
    xa, xb = DC["x"]; yc = DC["yc"]
    h, t, zf, zt = DUCT_W / 2, DUCT_T, FLOOR_Z + 2.0, FLOOR_Z + DUCT_H
    assert abs(yc + h - hub.DUCT_Y1) < 1e-9 and abs(t - hub.DUCT_WALL) < 1e-9
    d = box(xa, xb, yc - h, yc + h, FLOOR_Z, zt) - box(xa - 1, xb + 1, yc - h + t, yc + h - t, zf, zt + 1)
    for k in range(int((xb - xa - 10) // SLOT_PITCH)):
        x = xa + 5 + SLOT_PITCH * (k + 0.5)
        d = d - box(x - SLOT_W / 2, x + SLOT_W / 2, yc - h - 1, yc + h + 1, zt - SLOT_D, zt + 1)
    d = _bead_grooves_x(d, xa, xb, yc)
    d = d - box(*NOTCH_X, yc + h - t - 1, yc + h + 1, hub.NOTCH_Z, zt + 1)
    return _floor_screws(d, DC["screws"])

def _lid_x(x0, x1, yc):
    """flat lid with two lips that snap inside the walls (bead into the wall)"""
    y0, y1 = yc - DUCT_W / 2, yc + DUCT_W / 2; zt = FLOOR_Z + DUCT_H
    cs = _sq(y0, y1, zt, zt + 1.6)
    for s in (-1, 1):
        yi = yc + s * (DUCT_W / 2 - DUCT_T - 0.25)
        a, b2 = sorted((yi, yi - s * 1.2))
        cs = cs + _sq(a, b2, zt - 5.0, zt)
        bead = [(yi, zt - 4.6), (yi + s * 0.5, zt - 3.8), (yi + s * 0.5, zt - 3.0), (yi, zt - 2.4)]
        cs = cs + CrossSection([_ccw(bead)])
    return _yz_prism(cs, x0, x1)


def data_lid():
    """window over the wide chain exit (open from the -y edge, a 4 mm strip on +y holds both halves): the bundle leaves
    the bracket above the lid and drops into the duct"""
    zt = FLOOR_Z + DUCT_H
    return _lid_x(*DATA["x"], DATA["yc"]) - box(*WIDE_EXIT_X, DATA["yc"] - DUCT_W / 2 - 1, DATA["yc"] + DUCT_W / 2 - 4.0, zt - 6.0, zt + 3.0)   # +y strip with its lip stays

def dc_lid():
    """lid over the whole length; no +y lip over the notch (the wires come in over the spout below the lid)"""
    yc, zt = DC["yc"], FLOOR_Z + DUCT_H
    return _lid_x(*DC["x"], yc) - box(*NOTCH_X, yc + DUCT_W / 2 - DUCT_T - 2.0, yc + DUCT_W / 2 + 1, zt - 6.0, zt)

# ============================================================ fan ducts: +24 V / GND and PWM / tacho to the 4 fans
# Two lanes along y in front of the rear cross member (x 31.2), side by side: PWM/tacho lane against the member, power lane in front.
# Both end before the RS-15-5 (y 530.8) with an open end, so they have the full duct height (DUCT_H, user 2026-11-03).
# The fans are turned so their leads leave at the bottom of the outlet flange (fan_model.py): fans 1-3 enter the lane through a
# rounded notch in its +x wall at the fan centre y, fan 4 (behind the RS-15-5) runs -y in the 5 mm gap between RS and member and
# enters through the open end. Red / black cross into the power lane through aligned slots in the two inner walls.
# Power lane: T from the open rear end of the DC duct (tongue into it), PWM lane: 90 deg bend (R 13) from the data duct.
# The M4 heads of the lower fan screws (x >= 27.2, z 26.5..33.5) sit in notches of the +x wall and the lid.
# x limits: rails R1a/R1b end x 9.0, DIN PSU5 Cradle 2 x 8.0; 2040 of the wide chain to y 330.4.
FD_ZT = FLOOR_Z + DUCT_H              # wall top like every duct (lid 1.6 on top)
FD_LANE_W = 10.3
FD_Y_X = (10.2, 10.2 + FD_LANE_W)     # power lane 10.2..20.5
FD_G_X = (FD_Y_X[1] + 0.2, 31.0)      # PWM lane 20.7..31.0 (member face 31.2)
FD_Y_END = 528.0                      # open end, 2.8 before the RS-15-5 (y 530.8)
FD_BEND_RI = 12.0                     # inner fillet of the PWM bend; the power lane ends in an arc concentric to it (gap = lane gap)
FD_JOINT = 0.2                        # gap to the old duct end faces / walls
FD_NOTCH_W, FD_NOTCH_ZB = 6.0, 20.0   # lead notch in the +x wall, round bottom (leads leave the fan at z ~25)
FD_SLOT_W = 5.0                       # cross-over slots between the lanes (depth SLOT_D)
FD_HEAD = dict(x=27.0, dy=4.5, z=26.0)   # notch for the M4 heads of the lower fan screws (head d 7, k 4 assumed: x 27.2..31.2)

def _lead_y():
    """y of the lead entries: fan centre (leads leave at the bottom); fan 4 enters through the open end"""
    return tuple(yc for yc in FAN_YC if yc < FD_Y_END - FD_NOTCH_W)

def _head_y():
    return tuple(yc + s * FAN["pitch"] / 2 for yc in FAN_YC for s in (-1, 1) if yc + s * FAN["pitch"] / 2 < FD_Y_END + FD_HEAD["dy"])
FD_NOTCH_W, FD_NOTCH_ZB = 6.0, 13.0                  # lead notch in the green +x wall, round bottom
FD_SLOT_W = 5.0                                      # cross-over slots between the lanes (depth SLOT_D)

def _rr(pts, radii, d=0.0):
    """rectilinear CCW polygon with per-corner fillet radius (convex and concave), offset outward by d, exact arcs.
    radii may be dict(r=[...], arc=(i, j, cx, cy, R)): the sharp corners i, j (one edge between them) are replaced by an arc
    of the circle (cx, cy, R + d), from where it cuts the edge into corner i to the tangent point on the edge out of corner j"""
    arc = None
    if isinstance(radii, dict): radii, arc = radii["r"], radii["arc"]
    groups, k = [], len(pts)
    for i in range(k):
        p0, p1, p2 = np.array(pts[i - 1], float), np.array(pts[i], float), np.array(pts[(i + 1) % k], float)
        u0 = (p1 - p0) / np.linalg.norm(p1 - p0); u1 = (p2 - p1) / np.linalg.norm(p2 - p1)
        n0, n1 = np.array([-u0[1], u0[0]]), np.array([-u1[1], u1[0]])          # inward normals
        sg = 1.0 if u0[0] * u1[1] - u0[1] * u1[0] > 0 else -1.0                # +1 convex, -1 concave
        r = radii[i]; rho = r + sg * d
        if r <= 0 or rho < 0.3:
            groups.append([tuple(p1 - d * (n0 + n1))]); continue
        c = p1 + sg * r * (n0 + n1)
        a0 = math.atan2(*(-sg * n0)[::-1])
        m = max(4, min(16, int(math.ceil(rho * math.pi / 2 / 1.0))))
        groups.append([(c[0] + rho * math.cos(a0 + sg * math.pi / 2 * j / m), c[1] + rho * math.sin(a0 + sg * math.pi / 2 * j / m)) for j in range(m + 1)])
    if arc:
        i, j, cx, cy, R = arc
        (xl, _), (xr, _) = groups[i][0], groups[j][0]
        Rd = R + d
        aL = math.atan2(-math.sqrt(Rd * Rd - (xl - cx) ** 2), xl - cx)
        aR = math.atan2(0.0, xr - cx) if abs(abs(xr - cx) - Rd) < 1e-9 else math.atan2(-math.sqrt(Rd * Rd - (xr - cx) ** 2), xr - cx)
        if aR <= aL: aR += 2 * math.pi
        n = max(8, int(math.ceil(Rd * (aR - aL) / 1.0)))
        groups[i] = [(cx + Rd * math.cos(aL + (aR - aL) * t / n), cy + Rd * math.sin(aL + (aR - aL) * t / n)) for t in range(n + 1)]
        groups[j] = []
    return CrossSection([np.array([q for g in groups for q in g])])

def _vz(cs, z0, z1):
    return Manifold.extrude(cs, z1 - z0).translate((0, 0, z0))

def _tongue(x_end, y0, y1):
    """U tongue pushed 10 into the open end of an old duct (inner faces y0..y1, floor top 7, below the lid lips), 0.2 play;
    one extruded U section running 3 into the new body, a narrower block below reaches into its floor (fused, no coplanar faces)"""
    g, w, zf, L = FD_JOINT, 1.2, FLOOR_Z + 2.0, 3.0
    a, b, z0, z1, zt = y0 + g, y1 - g, zf + 0.2, zf + 1.4, FLOOR_Z + DUCT_H - 5.5
    u = CrossSection([_ccw([(a, z0), (b, z0), (b, zt), (b - w, zt), (b - w, z1), (a + w, z1), (a + w, zt), (a, zt)])])
    return _yz_prism(u, x_end - 10.0, x_end + L) + box(x_end, x_end + L - 0.5, a + 0.5, b - 0.5, FLOOR_Z + 1.0, z1 - 0.4)

def _fan_duct(pts, radii, mouths, slot_lane_x, notches, finger, screws):
    """lane duct from a plan: floor + walls (block minus cavity), bead grooves, open mouths, finger / cross-over slots,
    lead notches and head notches in the +x wall of the PWM lane"""
    t, zf, zt = DUCT_T, FLOOR_Z + 2.0, FD_ZT
    P = _rr(pts, radii)
    cav = _rr(pts, radii, -t)
    for x0, x1, y0, y1 in mouths: cav = cav + CrossSection.square((x1 - x0, y1 - y0)).translate((x0, y0))
    d = _vz(P, FLOOR_Z, zt) - _vz(cav, zf, zt + 1)
    d = d - _vz(_rr(pts, radii, -t + 0.5) - _rr(pts, radii, -t), zt - 4.8, zt - 2.2)          # bead groove all round
    for xw, y in slot_lane_x:                                                                 # cross-over slots (inner walls)
        d = d - box(xw[0] - 0.5, xw[1] + 0.5, y - FD_SLOT_W / 2, y + FD_SLOT_W / 2, zt - SLOT_D, zt + 1)
    for xw, y in notches:                                                                     # lead entries, round bottom
        r = FD_NOTCH_W / 2
        d = d - box(xw[0] - 0.5, xw[1] + 0.5, y - r, y + r, FD_NOTCH_ZB + r, zt + 1)
        d = d - _yz_prism(CrossSection.circle(r, 24).translate((y, FD_NOTCH_ZB + r)), xw[0] - 0.5, xw[1] + 0.5)
    if notches:
        for y in _head_y():
            d = d - box(FD_HEAD["x"], FD_G_X[1] + 1, y - FD_HEAD["dy"], y + FD_HEAD["dy"], FD_HEAD["z"], zt + 1)
    for x, y0, y1 in finger:                                                                  # finger slots across an arm
        d = d - box(x - SLOT_W / 2, x + SLOT_W / 2, y0 - 1, y1 + 1, zt - SLOT_D, zt + 1)
    return _floor_screws(d, screws)

def _fan_lid(pts, radii, mouth_cuts, notches):
    """flat lid on the plan, lips inside the walls with a bead into the groove; open mouths without lips"""
    t, zt = DUCT_T, FD_ZT
    m = _vz(_rr(pts, radii), zt, zt + 1.6)
    lip = _vz(_rr(pts, radii, -t - 0.25) - _rr(pts, radii, -t - 1.45), zt - 5.0, zt + 0.05)
    lip = lip + _vz(_rr(pts, radii, -t) - _rr(pts, radii, -t - 0.3), zt - 4.6, zt - 3.8)        # bead: lead-in step
    lip = lip + _vz(_rr(pts, radii, -t + 0.25) - _rr(pts, radii, -t - 0.3), zt - 3.8, zt - 2.4)
    for c in mouth_cuts: lip = lip - box(*c, zt - 6, zt + 0.1)
    m = m + lip
    for x0, y in notches:
        m = m - box(x0, x0 + 10.0, y - FD_NOTCH_W / 2, y + FD_NOTCH_W / 2, zt - 6, zt + 3)
    if notches:
        for y in _head_y():
            m = m - box(FD_HEAD["x"], FD_G_X[1] + 1, y - FD_HEAD["dy"], y + FD_HEAD["dy"], FD_HEAD["z"], zt + 3)
    return m

def _fd_yellow_plan():
    xa, xb = FD_Y_X; x0 = DC["x"][1] + FD_JOINT; y0, y1 = DC["yc"] - DUCT_W / 2, DC["yc"] + DUCT_W / 2
    # end at -y: arc around the centre of the PWM bend fillet, radius = fillet - gap; it is tangent to the +x wall (xb) by
    # construction and meets the -x wall at y ~350.3, so the power lane wraps around the bend with a constant 0.2 joint
    cx, cy = FD_G_X[0] - FD_BEND_RI, DATA["yc"] + DUCT_W / 2 + FD_BEND_RI
    R = FD_BEND_RI - (FD_G_X[0] - FD_Y_X[1])
    pts = [(x0, y0), (xa, y0), (xa, cy), (xb, cy), (xb, FD_Y_END), (xa, FD_Y_END), (xa, y1), (x0, y1)]
    return pts, dict(r=[0, 6, 0, 0, 0, 0, 6, 0], arc=(2, 3, cx, cy, R))

def _fd_green_plan():
    xa, xb = FD_G_X; x0 = DATA["x"][1] + FD_JOINT; y0, y1 = 330.5, DATA["yc"] + DUCT_W / 2
    return [(x0, y0), (xb, y0), (xb, FD_Y_END), (xa, FD_Y_END), (xa, y1), (x0, y1)], [0, 13, 0, 0, 12, 0]

def _end_mouth(xs):
    return (xs[0] + DUCT_T, xs[1] - DUCT_T, FD_Y_END - 3.0, FD_Y_END + 1.2)

def fan_dc_duct():
    pts, rr = _fd_yellow_plan(); x0 = pts[0][0]; yc = DC["yc"]; t = DUCT_T
    yi0, yi1 = yc - DUCT_W / 2 + t, yc + DUCT_W / 2 - t
    xw = (FD_Y_X[1] - t, FD_Y_X[1])
    d = _fan_duct(pts, rr, [(x0 - 1.2, x0 + 3.0, yi0, yi1), _end_mouth(FD_Y_X)], [(xw, y) for y in _lead_y()], [],
                  [(x, yi0 - t, yi1 + t) for x in (-38.0, -28.0, -18.0, -8.0)],
                  [(-20.0, yc), (sum(FD_Y_X) / 2, 400.0), (sum(FD_Y_X) / 2, 515.0)])
    return d + _tongue(DC["x"][1] + FD_JOINT, yi0, yi1)

def fan_data_duct():
    pts, rr = _fd_green_plan(); x0 = pts[0][0]; t = DUCT_T
    yi0, yi1 = pts[0][1] + t, pts[-1][1] - t
    d = _fan_duct(pts, rr, [(x0 - 1.2, x0 + 3.0, yi0, yi1), _end_mouth(FD_G_X)],
                  [((FD_G_X[0], FD_G_X[0] + t), y) for y in _lead_y()], [((FD_G_X[1] - t, FD_G_X[1]), y) for y in _lead_y()],
                  [(x, yi0 - t, yi1 + t) for x in (-28.0, -18.0, -8.0)],
                  [(-15.0, DATA["yc"]), (sum(FD_G_X) / 2, 400.0), (sum(FD_G_X) / 2, 515.0)])
    return d + _tongue(DATA["x"][1] + FD_JOINT, DATA["yc"] - DUCT_W / 2 + t, DATA["yc"] + DUCT_W / 2 - t)

def _lid_cuts(pts, xs):
    x0 = pts[0][0]
    return [(x0 - 1, x0 + 3.5, pts[0][1] + 1.0, pts[-1][1] - 1.0), (xs[0] + 1.0, xs[1] - 1.0, FD_Y_END - 3.5, FD_Y_END + 1)]

def fan_dc_lid():
    pts, rr = _fd_yellow_plan()
    return _fan_lid(pts, rr, _lid_cuts(pts, FD_Y_X), [])

def fan_data_lid():
    pts, rr = _fd_green_plan()
    return _fan_lid(pts, rr, _lid_cuts(pts, FD_G_X), [(FD_G_X[1] - 3.0, y) for y in _lead_y()])

# ============================================================ DIN rail holders (EN 50022 35 x 7.5)
CLIP_TOP = 16.0                       # top of the clip base

LATCH_END = 26.7                      # outer end of the latch side, from the rail centre
RELEASE = (18.8, 22.6)                # screwdriver slot from above, from the rail centre (notch 18.8..20.4 + 1.5 travel)

def _clip_cs(yc):
    """(y, z) section of a clip: base over the rail, rigid hook at -y, sprung slider latch at +y. Every clip latches to +y,
    so neighbouring holders never lock each other in.
    Print in place, one body: the slider hangs on a three-leg meander spring (legs 0.6, gaps 0.5) from a post of the base;
    ramp under the nose for snapping on, notch on top for a screwdriver through the release slot to pull it back."""
    f = 17.5; zt = RAIL_TOP                                  # flange edge |y| 17.5, flange z 11.5..12.5
    def sq(u0, u1, z0, z1):                                   # u = distance from the rail centre towards the latch
        return _sq(yc + u0, yc + u1, z0, z1)
    cs = sq(-f - 2.2, LATCH_END, zt + 0.2, CLIP_TOP)
    cs = cs + sq(-f - 2.2, -f - 0.2, zt - 2.6, CLIP_TOP) + sq(-f - 0.2, -f + 1.3, zt - 2.6, zt - 1.2)
    zb, zs = 6.0, zt - 0.2                                    # slider bottom (floor 5) / top (0.4 under the base)
    nose = [(19.0, zb), (21.0, zb), (21.0, zs), (17.9, zs), (17.9, zt - 1.2), (f - 1.3, zt - 1.2), (f - 1.3, zt - 1.9)]
    slider = CrossSection([_ccw([(yc + u, z) for u, z in nose])]) - sq(RELEASE[0], 20.4, zt - 2.2, zs + 1)
    cs = cs + slider
    t, g = 0.6, 0.5
    for k in range(4):                                       # bridges alternate bottom / top: slider, 3 legs, post
        u = 21.0 + g + k * (t + g)
        if k < 3: cs = cs + sq(u, u + t, zb, zs)
        cs = cs + sq(u - g - 0.05, u + 0.05, *((zb, zb + 0.8) if k % 2 == 0 else (zs - 0.8, zs)))
    return cs + sq(21.0 + 3 * (t + g) + g, LATCH_END, zb, zt + 0.25)

def clip(x0, x1, yc):
    return _yz_prism(_clip_cs(yc), x0, x1)

def release_cut(xc, yc, z1, half=2.5):
    """screwdriver slot through everything above the slider notch (stops above the slider top z 12.3)"""
    return box(xc - half, xc + half, yc + RELEASE[0], yc + RELEASE[1], RAIL_TOP + 0.1, z1)

# rail centre lines: power A (DC hub) / B (mains hub, fixed by the box: hook and latch inside y 557.1..604), 50 apart
# (A latch end 553.7, B hook 557.3); LRS-350 centre 532.5 and RS-15-5 centre 556.3 lie between them. Logic R2 = Octopus centre.
RAIL_A, RAIL_B, RAIL_R2 = 527.0, 577.0, 402.0
POWER_RAILS = (RAIL_A, RAIL_B)

def psu_cradle(xc, y0=473.0, y1=592.0, top=25.0, lip=8.0, w=20.0):
    """saddle on both power rails: platform under the PSU, side lips, two slots for a strap / zip tie; one extruded section"""
    x0, x1 = xc - w / 2, xc + w / 2
    cs = _sq(y0, y1, top - 4.0, top) + _sq(y0, y0 + 2.0, top, top + lip) + _sq(y1 - 2.0, y1, top, top + lip)
    for rail in POWER_RAILS:
        cs = cs + _clip_cs(rail) + _sq(rail - 19.7, rail + 19.7, CLIP_TOP - 1.0, top - 4.0)
    m = _yz_prism(cs, x0, x1)
    for y in (y0 + 6.0, y1 - 6.0):
        m = m - box(x0 + 3.0, x1 - 3.0, y - 1.5, y + 1.5, top - 5.0, top + 1)
    for rail in POWER_RAILS:
        m = m - release_cut(xc, rail, top + 1)
    return m

PSU5_CRADLE_X = (-44.0 + hub.RS_DX, 2.0)   # two narrow saddles under the RS-15-5 body (x -37.5..26.06); the second stays on the
                                          # power rails (end x 9): x -4..8
PSU5_CRADLE_W = 12.0

def psu5_cradle(xc):
    """narrow saddle for the RS-15-5 (y 530.8..581.8) on both power rails"""
    return psu_cradle(xc, 528.8, 583.8, 25.0, 6.0, PSU5_CRADLE_W)

# boards low (user 2026-11-03): bottom z 22.5 instead of 31, so the duct finger slots (z 21..30) sit at board level.
# Parts below the PCB (document vendor models): Octopus 3.1 (pins), Pi 2.1 -> holder top z 18 leaves 1.4 / 2.4.
BOARD_Z = 22.5                        # PCB bottom of Octopus and Pi
HOLDER_TOP = 18.0                     # top of the Octopus bars and the Pi plate (clip base top 16)

def octopus_holder(xh):
    """bar across the logic rail under one hole column of the Octopus (holes 150 x 90, board bottom BOARD_Z)"""
    x0, x1 = xh - 5.0, xh + 5.0
    m = _yz_prism(_clip_cs(RAIL_R2) + _sq(352.0, 452.0, CLIP_TOP - 1.0, HOLDER_TOP), x0, x1)
    for y in (357.0, 447.0):
        m = m + (cyl_z(xh, y, HOLDER_TOP - 1.0, BOARD_Z, 7.0, 24) - cyl_z(xh, y, BOARD_Z - 6.0, BOARD_Z + 1.0, 2.8, 16))
    return m - release_cut(xh, RAIL_R2, HOLDER_TOP + 1.0)

# logic rail R2 (x -320..-40): Pi 4 at the front, Octopus at the rear end close to the 4 fans (stepper drivers in the
# strongest airflow; swapped 2026-11-03, before: Octopus x -300..-140, Pi x -125..-40)
# Pi turned 180 deg (2026-11-03, user): USB/LAN -x towards the front, GPIO -y, USB-C +y; about 41 mm left for the plugs
# in front of the ports (-337.5) up to the drawer frame (-378.8), 50 mm to the Octopus.
PI_YC = RAIL_R2                       # Pi 4 centred over the logic rail (hole pattern centre)
PI_X0 = -335.0                        # Pi board -x edge = port side (board 85 long, holes 3.5 from the +x edge, 58 apart)
PI_HOLDER_X0 = PI_X0 + 85.0 - 65.0    # holder 65 long under the hole end of the board (+x)
OCTO_X0 = -200.0                      # Octopus board -x edge (board 160 long, hole columns 5 in, 150 apart)
OCTO_HOLDER_X = (OCTO_X0 + 5.0, OCTO_X0 + 155.0)

def pi_holder():
    """plate under the Pi 4 (holes 58 x 49, M2.5), board bottom BOARD_Z; release slots inside the clips, clear of the standoffs"""
    x0, x1, yc = PI_HOLDER_X0, PI_HOLDER_X0 + 65.0, PI_YC
    m = clip(x0, x0 + 14.0, RAIL_R2) + clip(x1 - 14.0, x1, RAIL_R2) + box(x0, x1, yc - 28.0, yc + 28.0, CLIP_TOP - 1.0, HOLDER_TOP)
    m = m - box(x0 + 14.0, x1 - 14.0, yc - 18.0, yc + 18.0, CLIP_TOP - 1, HOLDER_TOP + 1.0)          # window, saves material
    for x in (x0 + 3.5, x0 + 61.5):
        for y in (yc - 24.5, yc + 24.5):
            m = m + (cyl_z(x, y, HOLDER_TOP - 0.1, BOARD_Z, 6.0, 24) - cyl_z(x, y, BOARD_Z - 5.5, BOARD_Z + 1.0, 2.2, 16))
    for xc in (x0 + 10.0, x1 - 10.0): m = m - release_cut(xc, RAIL_R2, HOLDER_TOP + 1.0)
    return m

# ============================================================ 4 x 60 mm fans standing on the rear cross member
# 2020 L=334 #1 (document): x 31.2..51.2, y 290.8..624.8, z 5..25, rear slot centre z 15. Its bottom face lies on the tray
# floor plate (Gruppieren#15, z 0..5) and is not reachable -> the holder is screwed to the rear slot only.
# Fans (bought, in the document): Sanyo Denki San Ace 60L 9LG0624P4H001, 24 V, 4-wire PWM (25 kHz) + pulse sensor,
# 60 x 60 x 25 (catalogue p. 382: 60 +-0.5, 25 +-0.5, flanges 4 +-0.3, 8 x d 4.3 on 50 x 50, leads AWG26 300 mm).
# Axis x, blowing -x into the tray. They stand on the top face of the member (outlet face flush with its front face x 31.2),
# because the stepper motor of the stock frame (Stock Frame/Group#4, x 472..514, y 392..463, z >= 77.9) cannot move:
# retracted (stroke 396) fan + holder + nuts end at x 460.4.
# Limits: chain lanes y 290..330 (wide, upper run z 80.7+) and y 603..627 (thin bracket z 83.9+); thin channel
# (fixed, z 86.5..102, x 114..424, y 573.4..628.5) passes over the moving fan 4 -> fan and holder top z 85 (1.5 clear).
# RS-15-5 ends x 26.06 (z 25..53): screw heads on the outlet flange of fan 4 leave about 2 mm.
# Holder: plate on the intake side (x 56.2..61.2, z 7..85) with a spacer block behind the member (x 51.2..56.2, z 7..25; it
# also carries the 5 mm of fan behind the member), 2 x M5 + T-nut in the rear slot. Fan: 4 x M4 x 35 from the outlet side
# through both flanges and the plate, nut + washer on the back of the plate. Section constant along y (62 wide, fan 60):
# the 4.5 gaps between the holders take the fan leads (exit at +y) to the back of the plate; no cable shelf (user).
PROFILE_X, PROFILE_TOP, PROFILE_REAR_Z = (31.2, 51.2), 25.0, 15.0
FAN = dict(size=60.0, depth=25.0, pitch=50.0, hole=4.5, bore=57.0)
FAN_N, FAN_PITCH_Y = 4, 66.5
FAN_YC0 = 466.75                      # centre of the fan row: between the chain lanes (330.4 .. 603)
FAN_YC = tuple(FAN_YC0 + (k - (FAN_N - 1) / 2) * FAN_PITCH_Y for k in range(FAN_N))
FAN_X0 = PROFILE_X[0]                 # fan outlet face = front face of the member
FAN_ZTOP = PROFILE_TOP + FAN["size"]  # 85; thin channel bottom 86.5
FH_W = 62.0                           # holder width along y (fan 60; 4.5 gaps between the holders for the leads)
FH_T = 5.0                            # plate on the fan intake face
FH_X1 = FAN_X0 + FAN["depth"] + FH_T  # 61.2, back of the plate
FH_Z0 = 7.0                           # holder bottom (tray floor plate ends at x 51.2, z 5)
FH_SCREW_DY = 18.0                    # M5 positions +-18 from the fan centre (rear slot, z 15)
FH_NUT = 3.2 + 1.0                    # M4 nut + washer behind the plate (for the retracted check)

def fan_box(yc):
    """(x0, x1, y0, y1, z0, z1) of one fan body"""
    h = FAN["size"] / 2
    return (FAN_X0, FAN_X0 + FAN["depth"], yc - h, yc + h, PROFILE_TOP, FAN_ZTOP)

def _vent_oct(yc, zc, r):
    """octagon with inscribed radius r (covers the round fan bore; flat top bridges when printed on the side)"""
    R = r / math.cos(math.radians(22.5))
    return CrossSection([np.array([(yc + R * math.cos(math.radians(22.5 + 45 * k)), zc + R * math.sin(math.radians(22.5 + 45 * k))) for k in range(8)])])

def fan_holder(yc):
    """one fan standing on the member: plate on the intake side, spacer block behind the member"""
    fx0, fx1, fy0, fy1, fz0, fz1 = fan_box(yc)
    y0, y1 = yc - FH_W / 2, yc + FH_W / 2
    zc = (fz0 + fz1) / 2
    x0, x1 = PROFILE_X[1], FH_X1
    sec = [(x0, FH_Z0), (x1, FH_Z0), (x1, fz1), (fx1, fz1), (fx1, PROFILE_TOP), (x0, PROFILE_TOP)]
    m = _plate_y(CrossSection([_ccw(sec)]), y0, y1)                                     # block + plate, one section
    m = m - _yz_prism(_vent_oct(yc, zc, FAN["bore"] / 2), fx1 - 1, x1 + 1)
    for dy in (-1, 1):
        for dz in (-1, 1):
            m = m - _yz_prism(CrossSection.circle(FAN["hole"] / 2, 20).translate((yc + dy * FAN["pitch"] / 2, zc + dz * FAN["pitch"] / 2)), fx1 - 1, x1 + 1)
    for dy in (-FH_SCREW_DY, FH_SCREW_DY):
        m = m - _yz_prism(CrossSection.circle(5.5 / 2, 24).translate((yc + dy, PROFILE_REAR_Z)), x0 - 1, x1 + 1)   # M5 rear slot
    return m

HUB_CLIP_X = ((hub.X0 + 6.0, hub.X0 + 20.0), (hub.X1 - 20.0, hub.X1 - 6.0))   # inside the R 6 corner arcs (latch end y 603.7)
HUB_RELEASE_X = (hub.X0 + 17.0, hub.X1 - 17.0)           # release slots on the inner side of the clips, clear of the corner bosses

def hub_base(red):
    """each hub box on its own rail (mains: B, DC: A) with two full clips, release slots through the floor"""
    rail = RAIL_B if red else RAIL_A
    m = hub.red_base() if red else hub.dc_base()
    for x0, x1 in HUB_CLIP_X: m = m + clip(x0, x1, rail)
    for xc in HUB_RELEASE_X: m = m - release_cut(xc, rail, hub.FLOOR_Z + hub.T + 1)
    return m

def parts():
    """[(name, layer colour, world manifold, print manifold)]"""
    flip = lambda m: m.rotate((180, 0, 0))
    side = lambda m: m.rotate((0, 90, 0))                 # clips: constant section along x -> print on the section face
    rb, db = hub_base(True), hub_base(False)
    out = [("Mains Hub Base", COL_MAINS, rb, rb),
           ("Mains Hub Lid", COL_MAINS, hub.red_lid(), flip(hub.red_lid())),
           ("DC Hub Base", COL_DC, db, db),
           ("DC Hub Lid", COL_DC, hub.dc_lid(), flip(hub.dc_lid())),
           ("DC Duct", COL_DC, dc_duct(), dc_duct()), ("DC Duct Lid", COL_DC, dc_lid(), flip(dc_lid())),
           ("Data Duct", COL_DATA, data_duct(), data_duct()), ("Data Duct Lid", COL_DATA, data_lid(), flip(data_lid())),
           ("Fan DC Duct", COL_DC, fan_dc_duct(), fan_dc_duct()), ("Fan DC Duct Lid", COL_DC, fan_dc_lid(), flip(fan_dc_lid())),
           ("Fan Data Duct", COL_DATA, fan_data_duct(), fan_data_duct()), ("Fan Data Duct Lid", COL_DATA, fan_data_lid(), flip(fan_data_lid()))]
    for k, xc in enumerate((-339.0 + hub.LRS_DX, -174.0 + hub.LRS_DX)):   # 25 mm in from the LRS-350 ends
        m = psu_cradle(xc); out.append((f"DIN PSU24 Cradle {k + 1}", COL_DIN, m, side(m)))
    for k, xc in enumerate(PSU5_CRADLE_X):
        m = psu5_cradle(xc); out.append((f"DIN PSU5 Cradle {k + 1}", COL_DIN, m, side(m)))
    for k, xh in enumerate(OCTO_HOLDER_X):
        m = octopus_holder(xh); out.append((f"DIN Octopus Holder {k + 1}", COL_DIN, m, side(m)))
    m = pi_holder(); out.append(("DIN Pi Holder", COL_DIN, m, side(m)))
    on_back = lambda m: m.rotate((0, 90, 0))              # fan holders: back face of the plate on the bed, block on top, holes vertical
    for k, yc in enumerate(FAN_YC):
        m = fan_holder(yc); out.append((f"Fan Holder {k + 1}", COL_DIN, m, on_back(m)))
    return out
