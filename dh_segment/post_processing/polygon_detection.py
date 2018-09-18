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

    l = DkLine(params[0], params[1])
    l.setDefaults(np.array([miy, may], dtype=float))

    return l


class DkLine:

    k = 0
    d = 0
    dx = np.array([])

    def __init__(self, k, d):
        self.k = k
        self.d = d
        self.dx = np.array([])

    def setDefaults(self, x: np.array):
        self.dx = x

    def line(self, x: np.array = None):
        
        if x is None:
            x = self.dx
        
        y = self.k*x + self.d
        return [x, y]

    def scale(self, sxy):
        self.dx *= sxy
        self.d *= sxy

    def isEmpty(self):
        return self.k == 0 & self.d == 0
