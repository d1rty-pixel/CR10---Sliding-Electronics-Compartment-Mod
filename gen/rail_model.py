"""Display model of the bought DIN rails (purchased part: lives only in the document).

    ./venv/bin/python -I gen/rail_model.py      -> build/rails.json (rails L1, L2, R1 at tray.RAIL_A / RAIL_B / RAIL_R2)
Import in IngeTrazo: exec of gen/rail_import.py (replaces the meshes of the groups "DIN Rail L1/L2/R1 ...").

Model: Phoenix Contact NS 35/ 7,5 PERF 2000MM (item 0801733), steel galvanized, acc. to EN 60715. Datasheet drawing
(phoenixcontact.com/us/products/0801733, PDF of 2024-05-18, p. 3): width 35, depth 7.5, sheet 1, web 27 outside, slots
6.2 x 15 (full round ends as drawn), pitch 25, on the rail centre. Assumptions (not dimensioned in the datasheet): bend radius
inside 1.0 / outside 2.0 (= inside + sheet), flange ends cut square, slot pattern centred on the rail length (the real cut
position on the 2000-mm bar is arbitrary).
Section (y, z) from the rail centre and the rail bottom: web z 0..1 (|y| <= 13.5), walls |y| 12.5..13.5, flanges z 6.5..7.5
out to |y| 17.5 (flange underside flat from |y| 14.5: the clip hooks of tray._clip_cs start at |y| 16.2).
"""
import json, math, os, sys
import numpy as np
from manifold3d import Manifold, CrossSection

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tray
from cadio import planar_faces

W, H, T, WEB = 35.0, 7.5, 1.0, 27.0
SLOT_W, SLOT_L, PITCH = 6.2, 15.0, 25.0
RI = 1.0; RO = RI + T                     # bend radii (assumption)
ARC_SEG = 8                               # segments per 90 deg (R 1: chord 0.2 > near-vertex limit 0.1)
STEEL = (0.78, 0.79, 0.80)
Z0 = tray.RAIL_TOP - H                    # rail bottom on the tray floor (z 5)
# x ranges as placed in the document (docs/DESIGN.md, rail table; rails_box in cr10mod.py)
RAILS = (("L1", -361.5, 9.0, tray.RAIL_A), ("L2", -361.5, 9.0, tray.RAIL_B), ("R1", -320.0, -40.0, tray.RAIL_R2))   # L = power-supply side

def _arc(c, r, a0, a1):
    n = ARC_SEG * max(1, round(abs(a1 - a0) / 90.0))
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]

def section():
    """closed outline of the hat profile, counter-clockwise"""
    yb, zb = WEB / 2 - RO, RO             # centre of the bottom bends (11.5, 2)
    yt, zt = WEB / 2 + RI, H - T - RI     # centre of the top bends (14.5, 5.5)
    r = [(yb, 0.0)]
    r += _arc((yb, zb), RO, -90, 0)[1:]                  # outside bottom bend -> wall outer face y 13.5
    r += _arc((yt, zt), RI, 180, 90)                     # inside top bend -> flange underside z 6.5
    r += [(W / 2, H - T), (W / 2, H)]                    # flange tip, cut square
    r += _arc((yt, zt), RO, 90, 180)                     # outside top bend -> wall inner face y 12.5
    r += _arc((yb, zb), RI, 0, -90)                      # inside bottom bend -> web top z 1
    loop = r + [(-y, z) for y, z in reversed(r)]
    return CrossSection([loop])

def slot():
    """obround 6.2 x 15 in the (x, y) plane, centred on the origin, long axis x"""
    h = SLOT_L / 2 - SLOT_W / 2
    pts = _arc((h, 0.0), SLOT_W / 2, -90, 90) + _arc((-h, 0.0), SLOT_W / 2, 90, 270)
    return CrossSection([pts])

def rail(x0, x1, yc):
    L = x1 - x0
    m = Manifold.extrude(section(), L).transform(np.array([[0, 0, 1, x0], [1, 0, 0, yc], [0, 1, 0, Z0]], dtype=float))
    n = int((L / 2 - SLOT_L / 2) // PITCH)              # slots centre +- k * 25, all inside the rail
    xm = (x0 + x1) / 2
    cut = None
    for k in range(-n, n + 1):
        s = Manifold.extrude(slot(), T + 1.0).translate((xm + k * PITCH, yc, Z0 - 0.5))
        cut = s if cut is None else cut + s
    return m - cut, 2 * n + 1, L / 2 - n * PITCH - SLOT_L / 2

def main():
    out = []
    for name, x0, x1, yc in RAILS:
        m, ns, edge = rail(x0, x1, yc)
        bb = m.bounding_box()
        out.append(dict(rail=name, color=list(STEEL), faces=planar_faces(m)))
        print(f"{name}: x {bb[0]:.1f}..{bb[3]:.1f} y {bb[1]:.2f}..{bb[4]:.2f} z {bb[2]:.2f}..{bb[5]:.2f}, {ns} slots, "
              f"end web {edge:.1f}, vol {m.volume() / 1000:.1f} cm3, genus {m.genus()}, faces {len(out[-1]['faces'])}")
    os.makedirs("build", exist_ok=True)
    with open("build/rails.json", "w") as f: json.dump(out, f)

if __name__ == "__main__":
    main()
