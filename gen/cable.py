"""Cable feed parts (world mm): wide drag chain for CAN, 24/5 V, sensors, USB, network (y 290..330) and its end brackets.

Chain: N_LINKS (11) links, pitch CHP, fixed end under the acrylic plate at X_FIXED (upper run), moving end on the 2040 of the tray
(lower run), 180 deg arc at the front. Links are printed as built (chain frame, plates vertical), lids upside down (chain_link.Link), brackets and channel
parts are rotated so that their flat mounting face lies on the bed.
"""
import math
import numpy as np
from manifold3d import Manifold, CrossSection
from chain_link import Link
from cable_base import box, cyl_z, cyl_y, cyl_x, hex_z, hex_x, _plate_y, _sides, _ccw, _prism_x   # re-exported (cable.box etc.)

# ============================================================ geometry that comes from the model (docs/DESIGN.md)
CH_ZT = 102.0                        # underside of the acrylic plate = top of chain upper run and channel
CHAIN_Y = 310.0                      # centre of the chain lane y 290..330 (2040 on the tray)
CHAIN_ZU, CHAIN_ZL = 87.25, 37.75    # pivot height upper / lower run -> arc radius 24.75: with full-height stop corners the joints
                                     # stick out in the arc (searched: links z 25.22..101.79 in all poses; straight runs 96.25 / 28.75)
X_MOVING_EXT = -83.5                 # moving end with the tray fully out; the groove exit then sits over the tray duct (x -60..-35)
TRAVEL = 396.0
X_FIXED = X_MOVING_EXT + TRAVEL / 2   # fixed end, middle of the travel (x 116.5)

# ============================================================ drag chain
N_LINKS = 11
CHP, CHR, CHT = 29.5, 9.0, 3.0       # pitch, plate radius (height 18), plate thickness
CH_YO = (17.0, 20.0)                 # outer plate |y|
CH_YI = (13.7, 16.7)                 # inner plate |y|, 0.3 mm to the outer plate



# ---- link + clamp: shared code chain_link.Link (same mechanism as the thin chain), wide parameter set.
# Pitch 29.5, R 9, webs 14.5..17.5 and plate y bands as on the user component "Chain Link (new)" (data/chain_link_user.json);
# full-height stop corners (anti-sag of the long free upper run), clamp bow flush in a notch of the inner plates, hooks in grooves
# on the outer faces of the inner plates. Inner clear width 27.4, clear height 12.5 (bar z -9..-6.5, lid stub from z 6).
LINK = Link(R=CHR, pitch=CHP, y_in=CH_YI[0], t=CHT, w0=14.5, w1=17.5, bar_t=2.5,
            groove_z=(1.5, 4.0), groove_d=0.8, cap_t=2.0, arm_w=1.5, arm_z0=1.2, hook_lead=(0.2, 1.3))

def link():
    return LINK.link()

def lid():
    return LINK.lid()

def lid_print():
    return LINK.lid_print()

def hinge_sweep(max_deg, step=1.0):
    return LINK.hinge_sweep(max_deg, step)

def chain_pivots(x_m, n=N_LINKS, x_f=X_FIXED, chp=CHP, zu=CHAIN_ZU, zl=CHAIN_ZL):
    """(x, z) of the n+1 pivots; chord pitch chp; the last pivot sits at x_m on the lower run"""
    rc = (zu - zl) / 2; zc = (zu + zl) / 2
    def dense(xc):
        pts = [(x_f, zu), (xc, zu)]
        pts += [(xc - rc * math.sin(math.radians(a)), zc + rc * math.cos(math.radians(a))) for a in range(1, 180)]
        pts += [(xc, zl), (xc + 1500.0, zl)]
        P = np.array(pts); seg = np.hypot(*np.diff(P, axis=0).T); s = np.concatenate([[0], np.cumsum(seg)])
        t = np.arange(0, s[-1], 0.05)
        return np.stack([np.interp(t, s, P[:, 0]), np.interp(t, s, P[:, 1])], axis=1)
    def march(xc):
        D = dense(xc); idx = 0; out = [D[0]]
        for _ in range(n):
            d = np.hypot(D[idx:, 0] - D[idx, 0], D[idx:, 1] - D[idx, 1])
            hit = np.argmax(d >= chp)
            if d[hit] < chp: raise ValueError("chain path too short")
            idx += int(hit); out.append(D[idx])
        return np.array(out)
    lo, hi = x_m - 500.0, x_f + 60.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if march(mid)[-1, 0] < x_m: lo = mid
        else: hi = mid
    return march((lo + hi) / 2), (lo + hi) / 2

def travel_scan(shapes, x_ext, n, x_f, chp, zu, zl, travel=TRAVEL, step=1.0):
    """whole travel in `step` mm: z range of all links (+ lids) and the arc front in drawer coordinates (x - s).
    Uses the vertices of the link shapes in their local (x, z) frame, so it is exact for the vertex extremes and fast."""
    XZ = np.unique(np.round(np.vstack([np.asarray(m.to_mesh().vert_properties)[:, [0, 2]] for m in shapes]), 4), axis=0)
    r = dict(zlo=(1e9, 0.0), zhi=(-1e9, 0.0), front=(1e9, 0.0))
    for s in np.arange(0.0, travel + 1e-9, step):
        P, _ = chain_pivots(x_ext + s, n=n, x_f=x_f, chp=chp, zu=zu, zl=zl)
        for k in range(n):
            a, b = P[k], P[k + 1]; d = (b - a) / np.linalg.norm(b - a)
            z = a[1] + d[1] * XZ[:, 0] + d[0] * XZ[:, 1]
            x = a[0] + d[0] * XZ[:, 0] - d[1] * XZ[:, 1] - s
            if z.min() < r["zlo"][0]: r["zlo"] = (float(z.min()), float(s))
            if z.max() > r["zhi"][0]: r["zhi"] = (float(z.max()), float(s))
            if x.min() < r["front"][0]: r["front"] = (float(x.min()), float(s))
    return r

def chain_links(x_m):
    """[(name, kind, world manifold)] for the pose with the moving end at x_m"""
    P, xc = chain_pivots(x_m)
    lk, ld = link(), lid()
    out = []
    for k in range(N_LINKS):
        a, b = P[k], P[k + 1]; d = (b - a) / np.linalg.norm(b - a)
        M = np.array([[d[0], 0, -d[1], a[0]], [0, 1, 0, CHAIN_Y], [d[1], 0, d[0], a[1]]])
        out.append((f"Chain Link {k + 1:02d}", "Link", lk.transform(M)))
        out.append((f"Chain Lid {k + 1:02d}", "Lid", ld.transform(M)))
    return out, P, xc

# ============================================================ chain end brackets (world)
def bracket_fixed():
    """under the acrylic plate: M3 from above through the plate into nuts in the bracket, cable tunnel into the channel"""
    px, pz = X_FIXED, CHAIN_ZU
    x0, x1 = px + CHP - LINK.W1, px + 44.0        # body face = counterpart of the inner-plate stop of the first link (like a web)
    body = box(x0, x1, 290.0, 330.0, pz - CHR, CH_ZT)
    fun = [(px + 9.0, 296.8), (px + 9.0, 323.2), (px + 17.0, 313.0), (x1 + 1, 313.0), (x1 + 1, 297.0), (px + 17.0, 297.0), (px + 9.0, 296.8)]
    zf = pz - 4.0                                 # funnel floor (was 88.5 at pivot 92.5)
    body = body - Manifold.extrude(CrossSection([_ccw(fun[:-1])]), CH_ZT + 1 - zf).translate((0, 0, zf))
    for x in (px + 20.0, px + 36.0):
        body = body - cyl_z(x, 323.0, pz - CHR - 1, CH_ZT + 1, 3.4, 16) - hex_z(x, 323.0, pz - CHR - 1, pz - CHR + 2.7)
    return body + LINK.fork(px, pz, x0, CHAIN_Y)

GROOVE_R, GROOVE_W = 24.0, 18.0         # centre-line radius (> R_fest 22 of the cable), groove width

def bracket_moving(x_m=X_MOVING_EXT):
    """on top of the 2040 of the tray: M3 into hammer nuts in its two slots (y 300 / 320); the cables leave in a quarter turn
    (centre-line R 24) through the +y face into the tray duct (x -60..-35)"""
    pz = CHAIN_ZL
    xa = x_m + LINK.O0                    # body face = counterpart of the outer stop corner of the last link
    x1 = xa + GROOVE_R + GROOVE_W / 2 + 3.0
    body = box(xa, x1, 290.0, 330.0, 25.0, pz + CHR)
    ro, ri = GROOVE_R + GROOVE_W / 2, GROOVE_R - GROOVE_W / 2
    zf = pz + LINK.BAR[3]                 # groove floor level with the top of the link bar (link cavity)
    ring = cyl_z(xa, 330.0, zf, pz + CHR + 1, 2 * ro, 96) - cyl_z(xa, 330.0, zf - 1.0, pz + CHR + 2, 2 * ri, 96)
    cut = ring ^ box(xa, x1 + 1, 289.0, 331.0, zf - 1.0, pz + CHR + 2)
    body = body - cut - box(xa - 1, xa + 0.5, 330.0 - ro - 0.5, 330.0 - ri + 0.5, zf, pz + CHR + 1)
    for dx, y in ((20.0, 300.0), (4.0, 320.0)):
        body = body - cyl_z(xa + dx, y, pz - CHR - 1, pz + CHR + 1, 3.4, 16) - cyl_z(xa + dx, y, pz + 4.0, pz + CHR + 1, 6.4, 16)
    return body + LINK.tongue(x_m, pz, xa, CHAIN_Y)

def flat(m):
    """print orientation of parts with the mounting face on top (z = 102 / 102): rotate 180 deg about x"""
    return m.rotate((180, 0, 0))
