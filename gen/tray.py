"""Printed parts inside the tray (world mm, tray fully out): 230 V junction box, 24/5 V duct, data/bus duct, DIN rail holders.

Separation: mains only inside the red hub box (power_hub.py: WAGO 221-413 for L / N, 221-414 for PE, fed from the thin chain),
low voltage DC in the yellow hub box and the yellow duct, data and bus lines in the green duct along the wide chain. Purchased parts
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
COL_MAINS, COL_DC, COL_DATA, COL_DIN = (0.85, 0.1, 0.1), (0.95, 0.8, 0.1), (0.15, 0.6, 0.25), (0.25, 0.25, 0.28)

def _yz_prism(cs, x0, x1):
    """cross-section in (y, z) extruded along x over x0..x1"""
    return Manifold.extrude(cs, x1 - x0).transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=float))

def _sq(y0, y1, z0, z1):
    return CrossSection.square((y1 - y0, z1 - z0)).translate((y0, z0))

def _screw_down(x, y, z_top, depth=3.0):
    """M3 countersunk-ish hole from the top of a floor (z_top) down to the tray floor"""
    return cyl_z(x, y, FLOOR_Z - 1, z_top + 1, 3.4, 16) + Manifold.cylinder(depth, 1.7, 3.3, 16).translate((x, y, z_top - depth + 0.01))

# ============================================================ ducts (U channel with snap lid, finger slots)
DUCT_W, DUCT_H, DUCT_T = 20.0, 20.0, 1.6
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
    d = _bead_grooves_x(_duct_x(*DATA["x"], DATA["yc"]), *DATA["x"], DATA["yc"])
    return _floor_screws(d, [(x, DATA["yc"]) for x in DATA["screws"]])

def dc_duct():
    """open front end, closed rear end"""
    xa, xb = DC["x"]; yc = DC["yc"]
    h, t, zf, zt = DUCT_W / 2, DUCT_T, FLOOR_Z + 2.0, FLOOR_Z + DUCT_H
    d = box(xa, xb, yc - h, yc + h, FLOOR_Z, zt) - box(xa - 1, xb - t, yc - h + t, yc + h - t, zf, zt + 1)
    for k in range(int((xb - xa - 10) // SLOT_PITCH)):
        x = xa + 5 + SLOT_PITCH * (k + 0.5)
        d = d - box(x - SLOT_W / 2, x + SLOT_W / 2, yc - h - 1, yc + h + 1, zt - SLOT_D, zt + 1)
    d = _bead_grooves_x(d, xa, xb - t, yc)
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
    return _lid_x(*DATA["x"], DATA["yc"])

def dc_lid():
    """lid over the whole length"""
    return _lid_x(DC["x"][0], DC["x"][1] - DUCT_T - 0.3, DC["yc"])   # stops short of the closed rear end wall

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

def octopus_holder(xh):
    """bar across the logic rail under one hole column of the Octopus (holes 150 x 90, board bottom z 31)"""
    x0, x1 = xh - 5.0, xh + 5.0
    m = _yz_prism(_clip_cs(RAIL_R2) + _sq(352.0, 452.0, CLIP_TOP - 1.0, 20.0), x0, x1)
    for y in (357.0, 447.0):
        m = m + (cyl_z(xh, y, 19.0, 31.0, 7.0, 24) - cyl_z(xh, y, 23.0, 32.0, 2.8, 16))
    return m - release_cut(xh, RAIL_R2, 21.0)

# logic rail R2 (x -305..-40): Pi 4 at the front, Octopus at the rear end close to the 4 fans (stepper drivers in the
# strongest airflow; swapped 2026-11-03, before: Octopus x -300..-140, Pi x -125..-40)
PI_YC = RAIL_R2                       # Pi 4 centred over the logic rail (hole pattern centre)
PI_X0 = -300.0                        # Pi board -x edge (board 85 long, holes 3.5 in, 58 apart)
OCTO_X0 = -200.0                      # Octopus board -x edge (board 160 long, hole columns 5 in, 150 apart)
OCTO_HOLDER_X = (OCTO_X0 + 5.0, OCTO_X0 + 155.0)

def pi_holder():
    """plate under the Pi 4 (holes 58 x 49, M2.5), board bottom z 31; release slots inside the clips, clear of the standoffs"""
    x0, x1, yc = PI_X0, PI_X0 + 65.0, PI_YC
    m = clip(x0, x0 + 14.0, RAIL_R2) + clip(x1 - 14.0, x1, RAIL_R2) + box(x0, x1, yc - 28.0, yc + 28.0, CLIP_TOP - 1.0, 19.0)
    m = m - box(x0 + 14.0, x1 - 14.0, yc - 18.0, yc + 18.0, CLIP_TOP - 1, 20.0)          # window, saves material
    for x in (PI_X0 + 3.5, PI_X0 + 61.5):
        for y in (yc - 24.5, yc + 24.5):
            m = m + (cyl_z(x, y, 18.9, 31.0, 6.0, 24) - cyl_z(x, y, 22.0, 32.0, 2.2, 16))
    for xc in (x0 + 10.0, x1 - 10.0): m = m - release_cut(xc, RAIL_R2, 20.0)
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
           ("Data Duct", COL_DATA, data_duct(), data_duct()), ("Data Duct Lid", COL_DATA, data_lid(), flip(data_lid()))]
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
