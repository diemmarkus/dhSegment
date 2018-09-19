import numpy as np
from .binarization import threshold, bwClean
from .polygon_detection import find_polygonal_regions, fitLineToPoints

def findSeparators(sepProb: np.ndarray):

    sb = threshold(sepProb)
    sb = bwClean(sb)

    polys = find_polygonal_regions(sb, 0.001)

    lines = list()

    for p in polys:

        pts = p.T
        lines.append(fitLineToPoints(pts))



    # least squares
    return lines

