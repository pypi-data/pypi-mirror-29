#!/usr/bin/python
# -*- coding: utf-8 -*-

# usefull resources
#https://pomax.github.io/bezierinfo/

import os
import sys
import math

from hgl.calculate.point import vector_multiply
from hgl.settings import X, Y, Z

# http://stackoverflow.com/questions/5443653/opengl-coordinates-from-bezier-curves
# http://nccastaff.bournemouth.ac.uk/jmacey/RobTheBloke/www/opengl_programming.html#3
# http://www.pasteall.org/6266/python
# http://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy


def curve_simple(p1, p2, p3):
    return generate_quadratic_bezier_curve_points((p1, p2, p3))


def generate_quadratic_bezier_curve_points(points, steps=20):
    """Given a list of points interpolate between them by x steps generating the curve points
    for a Quadratic Bezier Curve

    Args:
      points (point list): List of point locations
      steps (int): number of points between each point

    Returns:
      points: returns list of new points

    Links:
        http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Quadratic_B.C3.A9zier_curves
    Images:"""


    jump = 1.0 / steps
    new_points = []
    results = [points[0]]
    for step in range(1, steps):
        t = jump * step
        tmp_points = points
        while len(tmp_points) > 1:
            new_points = []
            for end in range(1, len(tmp_points)):
                start = end - 1
                direction = (tmp_points[end][X] - tmp_points[start][X],
                             tmp_points[end][Y] - tmp_points[start][Y],
                             tmp_points[end][Z] - tmp_points[start][Z])
                if t and t>0.0 and t<=1.0:
                    new_points.append((tmp_points[start][X] + (direction[X] * t),
                                       tmp_points[start][Y] + (direction[Y] * t),
                                       tmp_points[start][Z] + (direction[Z] * t)))
            tmp_points = new_points
        if new_points:
            results.append(new_points[0])
    results.append(points[-1])
    return results


def generate_cubic_bezier_curve_points2(points, t1=0.1, steps=16):
    """Given a list of points interpolate between them by x steps generating the curve points
    for a Cubic Bezier Curve

    Args:
      points (point list): List of point locations
      steps (int): number of points between each point

    Returns:
      points: returns list of new points

    Links:
        http://en.wikipedia.org/wiki/Bézier_curve
        http://www.pasteall.org/6266/python
        http://html5tutorial.com/how-to-draw-n-grade-bezier-curve-with-canvas-api/
        http://html5tutorial.com/how-to-join-two-bezier-curves-with-the-canvas-api/
        http://pomax.github.io/bezierinfo/
    Images:"""

    t1_step = 1 / steps
    t1 = t1_step
    while t1 < 1:
        t1_pow_of_three = math.pow(t1, 3)
        t1_pow_of_two = math.pow(t1, 2)

        t2 = (1 - t1)
        t2_pow_of_three = math.pow(t2, 3)
        t2_pow_of_two = math.pow(t2, 2)


        part1 = vector_multiply(points[0], t2_pow_of_three)
        part2 = vector_multiply(points[1], 3 * t2_pow_of_two * t1)
        part3 = vector_multiply(points[2], 3 * t2 * t1_pow_of_two)
        part4 = vector_multiply(points[3], t1_pow_of_three)

        point = (part1[0] + part2[0] + part3[0] + part4[0],
                part1[1] + part2[1] + part3[1] + part4[1],
                part1[2] + part2[2] + part3[2] + part4[2])
        t1 += t1_step
    return results



def generate_cubic_bezier_curve_points(points, steps=16):
    if len(points) != 4:
        raise TypeError("Need exactly 4 points")
    return generate_bezier(points, steps)


def generate_bezier(points, steps=3):
    curve_lines = []
    for t in range(1, int(steps)):
        curve_lines.append(de_casteljau(points, t / steps))
    return curve_lines


def de_casteljau(points, t):
    """interpolate each control line to gain a point on the line and reduce the handles by one, repeat until a single point is left
    repeat incrementing the point on each iteration.

    Args:
      points (point list): List of point locations
      t (int): t point between 0 and 1, 0 is near first point 1 being closed to the second point

    Returns:
      points: returns list of new points

    Links:
        http://en.wikipedia.org/wiki/De_Casteljau's_algorithm

    Images:"""
    t1 = 1 - t

    end = len(points)
    if end == 1:
        return points[0]

    start = 0
    new_points = []
    for end in range(1, end):
        new_points.append([
            ((points[start][X] * t1) + (points[end][X] * t)),
            ((points[start][Y] * t1) + (points[end][Y] * t)),
            ((points[start][Z] * t1) + (points[end][Z] * t))])
        start += 1
    return de_casteljau(new_points, t)
