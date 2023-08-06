#!/usr/bin/python
# -*- coding: utf-8 -*-


def vector_multiply(vector, num):
    """Given two points return vector direction of first point heading towards the second point
    Args:
        point (point): point to multiply
        num (float): amount to multiply each vertex by

    Returns:
      vector: new vector

    Links:
    Images:"""
    return [p * num for p in vector]

def iterate_over_dimension(shapes, dimension=0):
    for shape in shapes:
        for point in shape.points:
            yield point[dimension]

def point_iterator(shapes):
    for shape in shapes:
        for point in shape.points:
            yield point[dimension]

def translate_points(shapes, offsets):
    for shape in shapes:
        for point in shape.points:
            point[0] = point[0] - offsets[0]
            point[1] = point[1] - offsets[1]
            point[2] = point[2] - offsets[2]
            

def center_on_point(point, points):
    #~ iterate_over_dimension(points, 0)
    x = min(iterate_over_dimension(points, 0))
    y = min(iterate_over_dimension(points, 1))
    z = min(iterate_over_dimension(points, 2))
    return (
        max(iterate_over_dimension(points, 0)) - min(iterate_over_dimension(points, 0)) / 2,
        max(iterate_over_dimension(points, 1)) - min(iterate_over_dimension(points, 1)) / 2,
        max(iterate_over_dimension(points, 2)) - min(iterate_over_dimension(points, 2)) / 2)

    
