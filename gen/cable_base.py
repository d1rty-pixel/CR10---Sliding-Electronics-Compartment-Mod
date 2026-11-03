"""Small geometry helpers shared by the chain, tray and channel modules (world mm)."""
import math
import numpy as np
from manifold3d import Manifold, CrossSection


def box(x0, x1, y0, y1, z0, z1):
    return Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))

def cyl_z(x, y, z0, z1, d, seg=24):
    return Manifold.cylinder(z1 - z0, d / 2, d / 2, seg).translate((x, y, z0))

def cyl_y(x, z, y0, y1, d, seg=24):
    return Manifold.cylinder(y1 - y0, d / 2, d / 2, seg).rotate((-90, 0, 0)).translate((x, y0, z))

def cyl_x(y, z, x0, x1, d, seg=24):
    return Manifold.cylinder(x1 - x0, d / 2, d / 2, seg).rotate((0, 90, 0)).translate((x0, y, z))

def hex_z(x, y, z0, z1, af=5.7):
    r = af / math.sqrt(3)
    return Manifold.cylinder(z1 - z0, r, r, 6).translate((x, y, z0))

def hex_x(y, z, x0, x1, af=5.7):
    r = af / math.sqrt(3)
    return Manifold.cylinder(x1 - x0, r, r, 6).rotate((0, 90, 0)).translate((x0, y, z))

def _plate_y(cs, y0, y1):
    """cs in (x, z) extruded over y0..y1"""
    return Manifold.extrude(cs, y1 - y0).rotate((90, 0, 0)).translate((0, y1, 0))

def _sides(yr):
    return [tuple(sorted((s * yr[0], s * yr[1]))) for s in (-1, 1)]

def _ccw(poly):
    P = np.array(poly, dtype=float)
    area = 0.5 * np.sum(P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1])
    return P if area > 0 else P[::-1].copy()

def _prism_x(poly, x0, x1):
    """polygon in (y, z) extruded along x over x0..x1"""
    m = Manifold.extrude(CrossSection([_ccw(poly)]), x1 - x0)
    return m.transform(np.array([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=float)).translate((x0, 0, 0))
