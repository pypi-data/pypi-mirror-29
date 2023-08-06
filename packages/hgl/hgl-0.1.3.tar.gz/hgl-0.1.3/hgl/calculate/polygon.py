import os
import sys
import math
sys.path.append(os.path.abspath('../../'))
from hgl.settings import X, Y, Z

#rename to winding, is this even valid 

# todo work out what todo with this
def fill(points):
    """ test if this triangle is wound clockwise or anticlockwise
    
    Description:
        Given 3 points in order determin if they are wound clockwise or anticlockwise
    Args:
      p1 (point): First point
      p2 (point): Second point
      p3 (point): Third point

    Returns:
      bool: True if ccw, False otherwise

    Links:
        http://www.toptal.com/python/computational-geometry-in-python-from-theory-to-implementation
    """
    clockwise = -1
    new_points = []
    while clockwise < len(points)-2:
        new_points.append((
            points[clockwise],
            points[clockwise + 1],
            points[clockwise + 2]))
        clockwise += 2

    return new_points
