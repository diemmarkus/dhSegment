import numpy as np
from .binarization import threshold, bwClean
from .polygon_detection import find_polygonal_regions, fitLineToPoints, DkPoly, DkLine
# from matplotlib import pyplot as plt
import cv2

def findSeparators(sepProb: np.ndarray):

    sb = threshold(sepProb)
    sb = bwClean(sb)

    polys = find_polygonal_regions(sb, 0.001)

    lines = list()

    for p in polys:

        pts = p.T
        # least squares
        lines.append(fitLineToPoints(pts))

    return lines

def findPages(pgProb: np.ndarray, seps: list = list()):

    # defines how flexible we are w.r.t separator/page ratio
    # i.e. 0.8 indicates that the spearator has to be at least 80% of the poly's max x/y diff
    sepRatio = 0.8

    pg = threshold(pgProb)
    pg = bwClean(pg, 15)

    polys = find_polygonal_regions(pg, 0.01)

    fSeps = list()

    for pl in polys:
        ply = DkPoly(pl)

        pmx = ply.maxSide()
        pmy = ply.maxSide(1)

        # find matching separators
        for s in seps:

            if s in fSeps:
                continue

            smx = s.maxSide()
            smy = s.maxSide(1)



            if (smx > smy and smx > sepRatio * pmx) or (smy > smx and smy > sepRatio*pmy):
                fSeps.append(s)
                print("separator added because: %d > %d" % ((smx, sepRatio*pmx) if smx > smy else (smy, sepRatio*pmy)))


    drawSeparators(pg, fSeps)

    # now compute pages w.r.t the separators
    sPolys = find_polygonal_regions(pg, 0.01)
    rects = polyToRect(sPolys)

    return rects

def polyToRect(polys):

    rects = list()

    for p in polys:


        b = cv2.minAreaRect(p)
        b = cv2.boxPoints(b)
        b = np.vstack((b, b[0,:]))  # close the poly
        rects.append(DkPoly(b))

    return rects


def drawSeparators(img: np.ndarray, seps: list = list()):

    for s in seps:

        l = s.lineCv((0, img.shape[0]))
        
        # remember: we have x, y flipped
        cv2.line(img, l[0], l[1], (0, 0, 0), 1)
