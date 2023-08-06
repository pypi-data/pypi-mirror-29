import os
import sys
import math
from hgl.settings import X, Y, Z


def is_counter_clockwise(p1, p2, p3):
    """ Given 3 points in order determin if they are wound clockwise or anticlockwise

    Args:
      p1 (point): First point
      p2 (point): Second point
      p3 (point): Third point

    Returns:
      bool: True if ccw, False otherwise

    Links:
        http://www.toptal.com/python/computational-geometry-in-python-from-theory-to-implementation
    """
    return (p2[X] - p1[X]) * (p3[Y] - p1[Y]) > (p2[Y] - p1[Y]) * (p3[X] - p1[X])


def is_clockwise(p1, p2, p3):
    """Given 3 points in order determin if they are wound clockwise or anticlockwise

    Args:
      p1 (point): First point
      p2 (point): Second point
      p3 (point): Third point

    Returns:
      bool: True if ccw, False otherwise

    Links:
        http://www.toptal.com/python/computational-geometry-in-python-from-theory-to-implementation
    """
    return (p2[X] - p1[X]) * (p3[Y] - p1[Y]) < (p2[Y] - p1[Y]) * (p3[X] - p1[X])
