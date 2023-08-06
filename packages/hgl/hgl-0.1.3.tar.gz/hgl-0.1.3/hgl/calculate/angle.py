#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import math
sys.path.append(os.path.abspath('../../'))
from hgl.settings import X, Y, Z
from hgl.calculate.line import vector, dot_product, distance_between_points, point_on_line


def angle(p1, p2, p3):
    #center to arc start and centre to arc end
    vector1 = vector(p1, p2)
    vector2 = vector(p1, p3)

    dp = dot_product(vector1, vector2)
    #print 'angle dp = ' + str(dp)
    #print "diestance 1 = " +str(distance_between_points(p1, p2))
    #print "distance 2 = " +str(distance_between_points(p1, p3))
    angle = math.acos(dp / (distance_between_points(p1, p2) * distance_between_points(p1, p3)))
    #print angle
    if angle == 0:
        return 360
    return (angle) * 180 / math.pi

def rotate(point, radius, angle, centre=(0,0,0)):
    """"""
    a1 = angle * (3.1415926 / 180)
    x = radius * math.cos(a1) + point[0]
    y = radius * math.sin(a1) + point[1]
    z = 0 
    return [x,y,z]


def calculate_squircle_segments(centre, length, direction, radius, segments=8):
    points = []
    #http://slabode.exofire.net/circle_draw.shtml
    offset = length / 2
    if direction == (1, 0, 0):
        start_angle = 1.5707963
        centre1 = centre[X] - offset, centre[Y], centre[Z]
        centre2 = centre[X] + offset, centre[Y], centre[Z]
    else:
        start_angle = 0
        centre1 = centre[X], centre[Y] + offset, centre[Z]
        centre2 = centre[X], centre[Y] - offset, centre[Z]

    end_angle = 3.1415926
    theta = end_angle / (segments - 1)

    tangetial_factor = math.tan(theta)  # precalculate the sine and cosine
    radial_factor = math.cos(theta)

    x = float(radius) * math.cos(start_angle)  # we start at angle = 0 
    y = float(radius) * math.sin(start_angle)
    for centre in (centre1, centre2):
        for ii in range(0, int(segments)):
            points.append((x + centre[X], y + centre[Y], centre[Z]))

            tx = -y
            ty = x

            x += tx * tangetial_factor
            y += ty * tangetial_factor

            x *= radial_factor
            y *= radial_factor
        x = float(radius) * math.cos(start_angle + end_angle)  # we start at angle = 0 
        y = float(radius) * math.sin(start_angle + end_angle)
    return points


def calculate_circle_segments(center, radius, segments=8):
    """Given center point and radius, and number of segment generate points for a circle
    Args:
        center (point): circle center point
        radius (int): size of the circle
        segments (int): number of points to return
    Returns:
        list: list of points on the circle

    Links:http://slabode.exofire.net/circle_draw.shtml
    Images:"""

    points = []
    if radius > 0:
        segments = segments * math.ceil(math.sqrt(radius))  # adjust to increase the number of segments
        theta = 2 * 3.1415926 / segments
        c = math.cos(theta)  # precalculate the sine and cosine
        s = math.sin(theta)
        x = radius  # we start at angle = 0 
        y = 0
        for ii in range(0, int(segments)):
            points.append((x + center[X], y + center[Y], center[Z]))
            t = x
            x = c * x - s * y
            y = s * t + c * y
    return points

def calculate_segments(center, start_angle, end_angle, radius, segments=8):
    """Given center point and start angle and end angle draw a arc with supplied radius generating required points
    Args:
        center (point): circle center point
        start_angle (float): start angle
        end_angle (float): end angle
        radius (int): size of the circle
        segments (int): number of points to return
    Returns:
        list: list of points in the arc

    Links:http://slabode.exofire.net/circle_draw.shtml
    Images:"""

    points = []
    theta = end_angle / (segments - 1)
    tangetial_factor = math.tan(theta)  # precalculate the sine and cosine
    radial_factor = math.cos(theta)

    x = float(radius) * math.cos(start_angle)  # x start pos based on start angle and radius
    y = float(radius) * math.sin(start_angle)  # y start pos based on start angle and radius
    for ii in range(0, int(segments)):
        points.append((x + center[X], y + center[Y], center[Z]))
        tx = -y
        ty = x

        x += tx * tangetial_factor
        y += ty * tangetial_factor
        x *= radial_factor
        y *= radial_factor
    return points
