#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import array, float64


def generate_bounds_from_point(point, width, height):
    return array([
        [point[X] - width, point[Y] + height, point[Z]],
        [point[X] + width, point[Y] + height, point[Z]],
        [point[X] - width, point[Y] - height, point[Z]],
        [point[X] + width, point[Y] - height, point[Z]]],
        dtype=float64)

def generate_point_array(size=1):
    return array([
        [point[X] - width, point[Y] + height, point[Z]],
        [point[X] + width, point[Y] + height, point[Z]],
        [point[X] - width, point[Y] - height, point[Z]],
        [point[X] + width, point[Y] - height, point[Z]]],
        dtype=float64)
