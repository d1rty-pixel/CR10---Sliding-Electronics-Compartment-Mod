"""Display model of the bought fan Sanyo Denki San Ace 60L 9LG0624P4H001 (purchased part: lives only in the document).

    ./venv/bin/python -I gen/fan_model.py      -> build/fan60.json (4 fans at the positions of tray.FAN_YC / tray.FAN_X0)
Import in IngeTrazo: exec of gen/fan_import.py (replaces the meshes of the groups "Luefter 60x60x25 #1..4 (...)").

Catalogue San Ace 60L (C1137B001, p. 382): 60 +-0.5 square, 25 +-0.5 deep, flanges 4 +-0.3, 8 x d 4.3 on 50 x 50,
aluminium frame, plastic impeller, 7 blades (drawing), leads AWG26 300 mm red + / black - / yellow sensor / brown control,
lead exit at the side of the outlet flange. Assumptions (not dimensioned in the catalogue): bore d 57, hub d 32, frame body
between the flanges = circle r 32.5 cut by the square, flange corner radius 3, 4 spokes on the outlet side (one carries the
leads, turned to +y = into the gap between the holders), lead d 1.1, lead stub 2.5 mm beyond the frame.
Local frame: axis x, outlet face x = 0 (on the holder plate), intake face x = 25, centre y = z = 0.
"""
import json, math, os, sys
import numpy as np
from manifold3d import Manifold, CrossSection, JoinType

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tray
from cadio import planar_faces

S, D, FL, PITCH, HOLE = 60.0, 25.0, 4.0, 50.0, 4.3
BORE, HUB_R, BODY_R, CORNER_R = 57.0, 16.0, 32.5, 3.0
BLADES, LEAD_D = 7, 1.1
AL, BLACK = (0.74, 0.75, 0.77), (0.09, 0.09, 0.10)
LEADS = ((0.85, 0.1, 0.1), (0.08, 0.08, 0.08), (0.95, 0.8, 0.1), (0.45, 0.25, 0.1))   # red, black, yellow, brown

def ax_x(cs, x0, x1):
    """cross-section in (y, z) extruded along x"""
    return Manifold.extrude(cs, x1 - x0).transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=float))

def rsq(s, r):
    h = s / 2 - r
    return CrossSection.square((2 * h, 2 * h), True).offset(r, JoinType.Round, 2.0, 32) if r else CrossSection.square((s, s), True)

def frame():
    m = ax_x(rsq(S, CORNER_R), 0, FL) + ax_x(rsq(S, CORNER_R), D - FL, D)
    m = m + ax_x(CrossSection.circle(BODY_R, 96) ^ CrossSection.square((S, S), True), FL - 0.5, D - FL + 0.5)
    m = m - ax_x(CrossSection.circle(BORE / 2, 96), -1, D + 1)
    for sy in (-1, 1):
        for sz in (-1, 1):
            m = m - ax_x(CrossSection.circle(HOLE / 2, 24).translate((sy * PITCH / 2, sz * PITCH / 2)), -1, D + 1)
    stator = ax_x(CrossSection.circle(HUB_R, 60), 2.2, 5.0)          # 60 segments: no vertex within 0.1 of the spoke edges
    for k in range(4):                                                    # spokes at 0/90/180/270 deg, the one at +y carries the leads
        a = k * 90.0
        sp = CrossSection.square((BORE / 2 + 0.5 - HUB_R + 1.0, 3.0)).translate((HUB_R - 1.0, -1.5)).rotate(a)
        stator = stator + ax_x(sp, 2.2, 5.0)
    m = m + stator
    m = m - Manifold.cube((6.0, 3.0, 6.0)).translate((-1.0, S / 2 - 2.0, -3.0))    # lead notch in the outlet flange (+y side)
    return m

def impeller():
    m = ax_x(CrossSection.circle(HUB_R, 64), 5.5, D - 1.0)
    pitch = 38.0                                                          # blade angle to the rotation plane (display only)
    slab = Manifold.cube((D - 1.0 - 6.0, 2 * S, 2 * S)).translate((6.0, -S, -S))
    for k in range(BLADES):
        b = Manifold.cube((26.0, BORE / 2 - 0.6 - HUB_R + 1.0, 1.2)).translate((-13.0, HUB_R - 1.0, -0.6))   # chord x, span y, thick z
        b = b.rotate((0, pitch, 0)).translate(((D + 5.5) / 2, 0, 0)) ^ slab
        m = m + b.rotate((360.0 / BLADES * k, 0, 0))
    return m - ax_x(CrossSection.circle(HUB_R - 1.5, 48), D - 2.0, D)       # recessed hub cap on the intake side

def leads():
    out = []
    for i, col in enumerate(LEADS):
        z = (i - 1.5) * (LEAD_D + 0.15)                                # small gap: separate shells, no shared edges
        w = Manifold.cylinder(S / 2 + 2.5 - HUB_R + 1.0, LEAD_D / 2, LEAD_D / 2, 12).rotate((-90, 0, 0)).translate((1.2, HUB_R - 1.0, z))
        out.append((w, col))
    return out

def main():
    parts = [(frame(), AL, "Rahmen"), (impeller(), BLACK, "Laufrad")] + [(w, c, f"Litze {k + 1}") for k, (w, c) in enumerate(leads())]
    zc = tray.FAN_ZTOP - tray.FAN["size"] / 2
    out = []
    for k, yc in enumerate(tray.FAN_YC):
        for m, col, nm in parts:
            mw = m.translate((tray.FAN_X0, yc, zc))
            out.append(dict(fan=k + 1, part=nm, color=list(col), faces=planar_faces(mw)))
    os.makedirs("build", exist_ok=True)
    with open("build/fan60.json", "w") as f: json.dump(out, f)
    f0 = frame().translate((tray.FAN_X0, tray.FAN_YC[0], zc)).bounding_box()
    print("fan 1 frame bbox", [round(v, 1) for v in f0], "parts", len(out), "frame genus", frame().genus(), "impeller vol", round(impeller().volume() / 1000, 1))

if __name__ == "__main__":
    main()
