#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from hgl.settings import X, Y, Z


def calculate_camera_plane_dimensions(viewport, location, near_plane, field_of_view, viewport_aspect):
    """ Given the camera location field of view and near plane calculate a rectangle that fits completely in the field of view """
    center_plane = location[Z] - near_plane
    if viewport[2] < viewport[3]:
        plane_width_origin = (math.atan(field_of_view / 2.0) * center_plane) 
        plane_height_origin = plane_width_origin * viewport_aspect
    else:
        plane_height_origin = (math.atan(field_of_view / 2.0) * center_plane) 
        plane_width_origin = plane_height_origin * viewport_aspect
    return plane_width_origin, plane_height_origin, 0
