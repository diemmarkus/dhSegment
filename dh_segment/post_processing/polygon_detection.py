#!/usr/bin/env python

import cv2
import numpy as np
import math
# from shapely import geometry


def find_polygonal_regions(image_mask: np.ndarray, min_area: float=0.1, n_max_polygons: int=math.inf):
    """
    Returns the coordinates of the shapes in a binary mask as polygons
    :param image_mask: Uint8 binary 2D array
    :param min_area: minimum area the polygon should have in order to be considered as valid
                (value within [0,1] representing a percent of the total size of the image)
    :param n_max_polygons: maximum number of boxes that can be found (default inf).
                        This will select n_max_boxes with largest area.
    :return: list of length n_max_polygons containing polygon's n coordinates [[x1, y1], ... [xn, yn]]
    """

    _, contours, _ = cv2.findContours(image_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours is None:
        print('No contour found')
        return None
    found_polygons = list()

    for c in contours:

        area = cv2.contourArea(c)
        # polygon = geometry.Polygon([point[0] for point in c])
        # area = polygon_area(c.T[0], c.T[1])

        # Check that polygon has area greater than minimal area
        if area >= min_area*np.prod(image_mask.shape[:2]):
            found_polygons.append(
                (np.array([point[0] for point in c]), area)
            )

    # sort by area
    found_polygons = [fp for fp in found_polygons if fp is not None]
    found_polygons = sorted(found_polygons, key=lambda x: x[1], reverse=True)

    if found_polygons:
        return [fp[0] for i, fp in enumerate(found_polygons) if i <= n_max_polygons]
    else:
        return None

def fitLineToPoints(pts):
    params = np.polyfit(pts[1], pts[0], 1)

    miy = min(pts[1])
    may = max(pts[1])

    l = DkLine(params[0], params[1], True)
    l.setDefaults(miy, may)

    return l

class DkVector:

    x = 0
    y = 0

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<Vector x:%.3f y:%.3f>" % self.coords()

    def coords(self):
        return (self.x, self.y)

    def length(self):
        """ Compute vector length """
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5
    
    def __imul__(self, o):
        """ scalar multiplication """
        self.x *= o
        self.y *= o

        return self

    def swap(self):
        xt = self.x
        self.x = self.y
        self.y = xt

class DkLine:

    k = 0
    d = 0
    _p1 = DkVector()
    _p2 = DkVector()
    swapped = False

    def __init__(self, k, d, swapped = False):
        self.k = k
        self.d = d
        self.swapped = swapped

    def setDefaults(self, x1: float, x2: float):
        self._p1 = DkVector(x1, self.map(x1))
        self._p2 = DkVector(x2, self.map(x2))
        
    def map(self, x):
        return self.k*x + self.d

    def lineCoords(self, xs = []):
        
        if not xs:
            xs = [self._p1.x, self._p2.x]
        
        pts = np.ndarray(shape=(2, len(xs)), dtype=float)
        ys = list()

        for x in xs:
            ys.append(self.map(x))
        
        return (xs, ys) if not self.swapped else (ys, xs)

    def line(self, xs=[]):

        l = self.lineCoords(xs)
        return list(map(list, zip(*l)))

    def lineCv(self, xs=[]):

        l = self.lineCoords(xs)
        l = list(map(list, zip(*l)))

        lcv = list()
        for v in l:
            lcv.append(tuple((int(v[0]), int(v[1]))))

        return lcv

    def scale(self, sxy):
        
        self._p1 = DkVector(self._p1.x*sxy, self.map(self._p1.x*sxy))
        self._p2 = DkVector(self._p2.x*sxy, self.map(self._p2.x*sxy))

        self.d *= sxy

    def isEmpty(self):
        return self.k == 0 & self.d == 0

    def maxSide(self, dimIdx: int = 0):

        if dimIdx == 0:
            return abs(self._p1.x-self._p2.x)
        else:
            return abs(self._p1.y-self._p2.y)

class DkPoly:
    
    pts = np.ndarray([])

    def __init__(self, pts: np.ndarray([]) = np.ndarray([])):
        self.pts = pts

    def maxSide(self, dimIdx: int = 0):

        lp = []
        md = 0

        for p in self.pts[dimIdx]:

            if lp:
                d = abs(p-lp)
                if d > md:
                    md = d

            lp = p

        return md

    def scale(self, sxy: float):

        for p in self.pts:
            p[0] *= sxy
            p[1] *= sxy
