"""Parametric drag chain link + clamp lid, shared by the thin and the wide chain (one code, two parameter sets).

Scheme of the user component "Chain Link (new)" (data/chain_link_user.json, pitch 29.5, R 9), rebuilt by rule:
pins on the rear (inner) plates, hole + snap slot in the front (outer) plates, joggle web between them, short closed bar on the
outer side of the bend, open inner side closed by an outer U clamp whose bow sits flush in a notch of the inner plates and whose
hooks engage grooves in the outer faces of the inner plates.
Chain frame: x along the chain, rear pivot at the origin, front pivot at (pitch, 0, 0), bar on -z, open side +z.

Inner plates (pins at the rear pivot) run to the front face of the web; on the bar half they reach back behind the pivot and stop
against the web of the previous link. Outer plates (hole at the front pivot) are square at the front on the bar half and stop
against the stepped rear of the next outer plate (bar half starts at R + OUT_GAP behind its pivot, open half only at the web);
that step leaves the clamp window on the open side. Square stop corners STOP_H high (anti-sag against hogging).
"""
import math
import numpy as np
from manifold3d import Manifold, CrossSection
from cable_base import box, cyl_y, _ccw, _plate_y


class Link:
    def __init__(self, R, pitch, y_in, t, w0, w1, gap=0.3, out_gap=0.2, in_gap=0.1, bar_x0=2.5, bar_t=2.0, stop_h=None,
                 pin_d=4.0, hole_d=4.4, slot_w=3.6, pin_in=0.8, pin_out=0.4, groove_z=(1.2, 3.2), groove_d=0.6,
                 cap_t=1.8, cap_fit=0.2, arm_w=1.2, arm_z0=1.0, stub_drop=3.0, hook_lead=(0.2, 1.1)):
        self.R, self.PITCH, self.Y_IN, self.T = R, pitch, y_in, t
        self.Y_INNER = (y_in, y_in + t)
        self.Y_GAP = (self.Y_INNER[1], self.Y_INNER[1] + gap)
        self.Y_OUTER = (self.Y_GAP[1], self.Y_GAP[1] + t)
        self.W0, self.W1 = w0, w1
        self.O0 = R + out_gap                                   # rear of the outer plate on the bar half
        self.INNER_EXT = pitch - w1 - in_gap                    # inner plate behind the pivot on the bar half
        self.BAR = (bar_x0, w0 - 0.5, -R, -R + bar_t)           # closed bar between the inner plates
        self.STOP_H = R if stop_h is None else stop_h
        self.PIN_D, self.HOLE_D, self.SLOT_W = pin_d, hole_d, slot_w
        self.PIN_Y = (self.Y_INNER[1] - pin_in, self.Y_OUTER[1] - pin_out)
        # clamp window on the open half, outer face of the inner plates: between the previous outer plate and the own web
        self.CLAMP_X = (R + 0.8, w0 - 0.3)
        self.GROOVE_Z, self.GROOVE_D = groove_z, groove_d
        self.CAP_T, self.CAP_FIT = cap_t, cap_fit
        self.CAP_Z = (R - cap_t, R)
        self.ARM_Y = (self.Y_INNER[1] + 0.2, self.Y_INNER[1] + 0.2 + arm_w)   # within the outer plate width
        self.STUB_Z = (R - stub_drop, self.CAP_Z[0])            # closes the opening between the inner plates
        self.ARM_Z0 = arm_z0
        self.HOOK_LEAD = hook_lead

    # ---- 2D helpers in (x, z)
    @staticmethod
    def circ(x, z, r, seg=48):
        return CrossSection.circle(r, seg).translate((x, z))

    @staticmethod
    def rect(x0, x1, z0, z1):
        return CrossSection.square((x1 - x0, z1 - z0)).translate((x0, z0))

    def plate(self, cs, yr):
        """cs extruded over both y bands +-yr"""
        m = Manifold()
        for y0, y1 in ((yr[0], yr[1]), (-yr[1], -yr[0])): m = m + _plate_y(cs, y0, y1)
        return m

    def pins(self, x, z):
        m = Manifold()
        for s in (-1, 1):
            ya, yb = s * self.PIN_Y[0], s * self.PIN_Y[1]
            m = m + cyl_y(x, z, min(ya, yb), max(ya, yb), self.PIN_D)
        return m

    def hole_cs(self, x, z, slot=+1):
        R = self.R
        sl = self.rect(x - self.SLOT_W / 2, x + self.SLOT_W / 2, z if slot > 0 else z - R - 1, z + R + 1 if slot > 0 else z)
        return self.circ(x, z, self.HOLE_D / 2, 24) + sl

    def inner_cs(self, px=0.0):
        R = self.R
        return self.circ(px, 0, R) + self.rect(px, self.W1, -R, R) + self.rect(px - self.INNER_EXT, px, -self.STOP_H, 0)

    def outer_cs(self, px, x0_bar, x0_open):
        """outer plate around the pivot px (hole); bar half from x0_bar, open half from x0_open, square stop corner in front"""
        R = self.R
        return (self.rect(x0_bar, px, -R, 0) + self.rect(x0_open, px, 0, R) + self.circ(px, 0, R)
                + self.rect(px, px + R, -self.STOP_H, 0)) - self.hole_cs(px, 0, +1)

    # ---- parts
    def link(self):
        """built from y slabs whose (x, z) sections meet exactly: unions of coplanar outer faces of mixed primitives leave slivers"""
        R, W0, W1 = self.R, self.W0, self.W1
        web = self.rect(W0, W1, -R, R)
        m = _plate_y(self.rect(*self.BAR), -self.Y_IN, self.Y_IN)
        m = (m + self.plate(self.inner_cs(), self.Y_INNER) + self.plate(self.rect(self.O0, W0, -R, 0) + web, self.Y_GAP)
             + self.plate(self.outer_cs(self.PITCH, self.O0, W0) + web, self.Y_OUTER))
        m = m + self.pins(0, 0)
        yi = self.Y_INNER[1]
        for s in (-1, 1):
            y0, y1 = sorted((s * (yi - self.GROOVE_D), s * (yi + 0.2)))
            m = m - box(self.CLAMP_X[0], self.CLAMP_X[1], y0, y1, self.GROOVE_Z[0], self.GROOVE_Z[1])
        return m - box(self.CLAMP_X[0], self.CLAMP_X[1], -yi - 0.5, yi + 0.5, self.CAP_Z[0] - self.CAP_FIT, R + 1)

    def lid(self):
        """U clamp over the open side, arms on the outer face of the inner plates inside the clamp window, hooks in the grooves;
        constant section along x: one (y, z) cross-section extruded once (no coplanar unions of separate solids)"""
        x0, x1 = self.CLAMP_X[0] + self.CAP_FIT, self.CLAMP_X[1] - self.CAP_FIT
        sq = lambda y0, y1, z0, z1: CrossSection.square((y1 - y0, z1 - z0)).translate((y0, z0))
        AY, GZ = self.ARM_Y, self.GROOVE_Z
        cs = sq(-AY[1], AY[1], *self.CAP_Z) + sq(-(self.Y_IN - 0.2), self.Y_IN - 0.2, self.STUB_Z[0], self.CAP_Z[0] + 0.1)
        for s in (-1, 1):
            ya, yb = sorted((s * AY[0], s * AY[1]))
            cs = cs + sq(ya, yb, self.ARM_Z0, self.CAP_Z[1])
            yi, yt = s * (AY[0] + 0.5), s * (self.Y_INNER[1] - self.GROOVE_D + 0.1)   # hook tip 0.1 short of the groove bottom
            lo, hi = self.HOOK_LEAD
            hook = [(yi, GZ[0] + lo), (yt, GZ[0] + hi), (yt, GZ[1] - 0.2), (yi, GZ[1] - 0.2)]   # ramp leads, flat face retains
            cs = cs + CrossSection([_ccw(hook)])
        return Manifold.extrude(cs, x1 - x0).transform(np.array([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=float))

    def lid_print(self):
        return self.lid().rotate((180, 0, 0))

    def bent(self, m, phi_deg):
        """m as the next link, pivot (pitch, 0, 0), bent by phi towards the open side (+z)"""
        c, s = math.cos(math.radians(phi_deg)), math.sin(math.radians(phi_deg))
        return m.transform(np.array([[c, 0, -s, self.PITCH], [0, 1, 0, 0], [s, 0, c, 0]]))

    def hinge_sweep(self, max_deg, step=1.0):
        """(first angle in 0..max_deg where two neighbours incl. clamps collide or None, stop engages within -1.5 deg)"""
        lk = self.link(); a = lk + self.lid()
        for k in range(int(max_deg / step) + 1):
            if (a ^ self.bent(a, k * step)).volume() > 1e-3: return k * step, None
        return None, (lk ^ self.bent(lk, -1.5)).volume() > 1e-3

    # ---- bracket interfaces (world: pivot at (px, pz), chain along x in the plane y = yc)
    def fork(self, px, pz, x0, yc):
        """outer plates with hole + slot (down) around the first pivot, stop corner above; reaches to x0 + 1 into the body"""
        R = self.R
        cs = (self.circ(px, pz, R) + self.rect(px, x0 + 1.0, pz - R, pz + R) + self.rect(px - R, px, pz, pz + self.STOP_H)
              - self.hole_cs(px, pz, -1))
        return self.plate(cs, self.Y_OUTER).translate((0, yc, 0))

    def tongue(self, px, pz, xa, yc):
        """inner plates with pins around the last pivot, reaching to xa + 1 into the body"""
        R = self.R
        cs = self.circ(px, pz, R) + self.rect(px, xa + 1.0, pz - R, pz + R)
        return self.plate(cs, self.Y_INNER).translate((0, yc, 0)) + self.pins(px, pz).translate((0, yc, 0))
