#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from decimal import Decimal, ROUND_HALF_UP
sys.path.append(os.path.abspath('../../'))
from hgl.settings import X, Y, Z

def total_grid_lines_normalised(major_scale, minor_scale, width, height, depth=0):
    """Given a width height and depth calculate the total grid lines that will fit in an area

    Args:
      width  (number): box  width
      height (number): box height
      depth  (number): box depth 0 for rectangle

    Returns:
      vector: direction of wr, ht, dt normalised
    """
    result = total_grid_lines(major_scale=major_scale, minor_scale=minor_scale, width=width, height=height, depth=depth)
    print(result)
    return (
        1.0 / result[0],
        1.0 / result[1],
        0 if result[2] == 0 else 1.0 / result[2])


def total_grid_lines(major_scale, minor_scale, width, height, depth=0):
    """Given a width height and depth calculate the total grid lines that will fit in an area

    Args:
      width  (number): box  width
      height (number): box height
      depth  (number): box depth 0 for rectangle

    Returns:
      vector: direction of wr, ht, dt
    """
    return int(width / minor_scale), int(height / minor_scale), int(depth / minor_scale)


def grid_snap(point, size, snap=True):
    """Given a point in space snap it to the nearest grid line
    Args:
      point  (list): x,y,z point in space
      size (number): small grid lines
      snap  (boolean): weather to actually snap the point or not

    Returns:
      point: x, y, z
    """
    if snap is False:
        return point
    if size == 0.0:
        return point

    return [
        Decimal((point[0] / size)).quantize(0, ROUND_HALF_UP) * size,
        Decimal((point[1] / size)).quantize(0, ROUND_HALF_UP) * size,
        Decimal((point[2] / size)).quantize(0, ROUND_HALF_UP) * size]


def grid_uniform(width, height, size=10):
    if width > height:
        aspect = width / height
        return size, size * aspect
    else:
        aspect = height / width
        return size * aspect, size
