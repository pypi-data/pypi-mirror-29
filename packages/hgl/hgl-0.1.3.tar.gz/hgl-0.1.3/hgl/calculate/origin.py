#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import math
sys.path.append(os.path.abspath('../../'))
from hgl.settings import X, Y


def rotate(point, angle):
    """"""
    ang = angle * math.pi / 180
    sin_angle = math.sin(ang)
    cos_angle = math.cos(ang)

    #~ float xnew = p.x * c - p.y * s;
    #~ float ynew = p.x * s + p.y * c;
    #~ print point
    newx = point[X] * cos_angle - point[Y] * sin_angle
    newy = point[X] * sin_angle + point[Y] * cos_angle
    return [
        newx,
        newy,
        0
    ]  # [x,y,z]

def mirror(point, x=1, y=-1):
    """"""
    return [
        point[X] * x,
        point[Y] * y,
        0
    ]
