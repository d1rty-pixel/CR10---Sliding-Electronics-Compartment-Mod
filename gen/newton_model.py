"""Motion data for the Newton extension of IngeTrazo: drag-chain hinges and drawer slide travel.

    ./venv/bin/python -I gen/newton_model.py    -> build/newton.json
Import in IngeTrazo: exec of gen/newton_import.py (sets bodies, references, joints and limits in the document).

Chains: one hinge per link at the generator pivots of the extended pose (cable.chain_pivots at X_MOVING_EXT), axis -Y so
that bending into the arc is positive. Hinge limits are absolute bend angles between neighbouring links, converted to
the modelled pose (the joint's 0). Backwards: first contact of two neighbouring links in the CAD geometry (Link.bent,
overlap > 1e-3 mm3). Forwards: the arc's need + FREE_SLACK_DEG, a stand-in for the stiffness of the cables, which the
model lacks; the links themselves collide only at CAD_FWD_DEG (incl. clamps), which let the arc collapse (T-045, T-046).
Slides: retracting is +X. Each stage (outer->middle, middle->inner) moves half the travel; the travel ends at the frame
stop found by gen/travel_sim.py (393.5 < TRAVEL 396, docs/DESIGN.md).
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cable
import cable_thin
import travel_sim

# bisected with Link.bent on 2026-11-05; redo when the link geometry changes
STOP_DEG = {"wide": -0.65, "thin": -0.79}
CAD_FWD_DEG = {"wide": 96.0, "thin": 97.2}
FREE_SLACK_DEG = 15.0               # user's pick from the headless sag comparison 2026-11-05
FRAME_STOP = 393.5                  # drawer frame hits the base before TRAVEL (travel_sim, T-006)


def chain(tag, pivots, lane_y, link_prefix, lid_prefix, fixed, moving):
    P = [(float(x), float(z)) for x, z in pivots]
    heading = [math.atan2(b[1] - a[1], b[0] - a[0]) for a, b in zip(P, P[1:])]
    # bend at pivot k between segment k-1 and segment k; the fixed bracket continues the upper run straight
    bend = [0.0] + [math.degrees((heading[k - 1] - heading[k] + math.pi) % (2 * math.pi) - math.pi)
                    for k in range(1, len(heading))]
    upper = max(-b for b in bend) + FREE_SLACK_DEG
    if upper > CAD_FWD_DEG[tag]:
        raise SystemExit(f"{tag}: forward limit {upper:.1f} beyond the link collision {CAD_FWD_DEG[tag]}")
    links = []
    for k in range(len(P) - 1):
        theta = -bend[k]            # axis -Y: bending downwards into the arc is positive
        links.append(dict(link=f"{link_prefix}{k + 1:02d}", lid=f"{lid_prefix}{k + 1:02d}",
                          pivot=[P[k][0], lane_y, P[k][1]], bend_deg=theta,
                          lower_deg=STOP_DEG[tag] - theta, upper_deg=upper - theta))
    end = [P[-1][0], lane_y, P[-1][1]]
    return dict(tag=tag, fixed=fixed, moving=moving, axis=[0, -1, 0], links=links, end=end)


def main():
    wide, _ = cable.chain_pivots(cable.X_MOVING_EXT)
    thin, _ = cable.chain_pivots(cable_thin.X_MOVING_EXT, n=cable_thin.N_LINKS, x_f=cable_thin.X_FIXED,
                                 chp=cable_thin.PITCH, zu=cable_thin.ZU, zl=cable_thin.ZL)
    out = dict(
        slide=dict(axis=[1, 0, 0], stage_mm=FRAME_STOP / 2, travel_mm=FRAME_STOP),
        chains=[chain("wide", wide, cable.CHAIN_Y, "Chain Link ", "Chain Lid ", "Chain Bracket Fixed", "Chain Bracket Moving"),
                chain("thin", thin, cable_thin.CHAIN_Y, "Thin Link ", "Thin Lid ", "Thin Bracket Fixed", "Thin Bracket Moving")],
        lanes_y=[[290.0, 330.0], list(cable_thin.LANE_Y)],
        # the same parts travel_sim moves with the drawer
        moving_tops=list(travel_sim.MOVING_TOPS), moving_layers=list(travel_sim.MOVING_LAYERS),
        middle=list(travel_sim.MIDDLE), inner=list(travel_sim.INNER), outer=list(travel_sim.OUTER))
    for c in out["chains"]:
        for l in c["links"]:
            if not l["lower_deg"] <= 0 <= l["upper_deg"]:
                raise SystemExit(f"{l['link']}: modelled bend {l['bend_deg']:.2f} outside the hinge range")
    os.makedirs("build", exist_ok=True)
    with open("build/newton.json", "w") as f:
        json.dump(out, f, indent=1)
    for c in out["chains"]:
        print(c["tag"], " ".join(f"{l['bend_deg']:.1f}" for l in c["links"]))


if __name__ == "__main__":
    main()
