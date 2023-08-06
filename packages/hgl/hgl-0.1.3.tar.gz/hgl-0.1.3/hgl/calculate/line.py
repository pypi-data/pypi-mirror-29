#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import math
sys.path.append(os.path.abspath('../../'))
from hgl.settings import X, Y, Z

def vector(p1, p2):
    """Given two points return vector direction of first point heading towards the second point

    Args:
      p1 (point): starting point
      p2 (point): ending point

    Returns:
      vector: direction of x,y,z 

    Links:
    Images:"""
    d1 = p2[X] - p1[X]
    d2 = p2[Y] - p1[Y]
    d3 = p2[Z] - p1[Z]
    return d1, d2, d3


def mid_point(p1, p2):
    """ return the point inbetween the start and finish of the line """
    return [(p1[0]+p2[0])/2.0, (p1[1]+p2[1])/2.0, (p1[2]+p2[2])/2.0]


def vector_normalised(p1, p2):
    """Given two points return normalised vector direction of first point heading towards the second point

    Args:
      p1 (point): starting point
      p2 (point): ending point

    Returns:
      vector: normalised direction of x,y,z 

    Links:
    Images:"""
    d1 = p2[X] - p1[X]
    d2 = p2[Y] - p1[Y]
    d3 = p2[Z] - p1[Z]
    length = math.sqrt((d1 * d1) + (d2 * d2) + (d3 * d3))
    return d1 / length, d2 / length, d3 / length

def dominate_direction(p1, p2):
    v = vector_normalised(p1, p2)
    m = max(seq)
    nv = [0, 0, 0]
    for a in v:
        if v[a] > v[a + 1]:
            nv[a] = 1
    return nv

def magnitude(v):
    """ calculate magnitude of a vectors """
    return math.sqrt(abs(v[0] * v[0]) + abs(v[1] * v[1]) + abs(v[2] * v[2]))

def shrink_line(p1, p2, ratio):
    """Given two points calculate the distance and generate a new point inside
    the line at either end to shrink the line

    Args:
      p1 (point): starting point
      p2 (point): ending point
      ration: (normalised value)

    Returns:
      p1 (point): new starting point
      p2 (point): new ending point

    Links:
    Images:"""
    distance_between_points(p1, p2)
    return point_on_line(p1, p2, ratio), point_on_line(p1, p2, 1 - ratio)

def distance_between_points(p1, p2):
    """Given two points return the length or distance of the line

    Args:
      p1 (point): starting point
      p2 (point): ending point

    Returns:
      int: length of line

    Links:
    Images:"""
    d1 = p2[X] - p1[X]
    d2 = p2[Y] - p1[Y]
    d3 = p2[Z] - p1[Z]
    return math.sqrt((d1 * d1) + (d2 * d2) + (d3 * d3))

def distance_between_points_xyz(p1, p2):
    """Given two points return distance between each axes 

    Args:
      p1 (point): starting point
      p2 (point): ending point

    Returns:
      vector: distance of x, y and z 

    Links:
    Images:"""
    d1 = p2[X] - p1[X]
    d2 = p2[Y] - p1[Y]
    d3 = p2[Z] - p1[Z]
    return d1, d2, d3

def parallel_line(p1, p2, distance, offset):
    """Given start and end point of line and length of line, create a second parallel line which is offset

    Args:
      p1 (point): starting point
      p2 (point): ending point
      distance (float): distance of line
      offset (float): offset distance from first line

    Returns:
      list: start point and end point of new line [[x,y,z], [x,y,z]]

    Links:
    Images:"""
    #~ print p1
    #~ print p2
    #~ print offset
    #~ print distance
    if distance is 0.0:
        return p1, p2
    try:
        x1p = p1[X] + offset * (p2[Y] - p1[Y]) / distance
        x2p = p2[X] + offset * (p2[Y] - p1[Y]) / distance
        y1p = p1[Y] + offset * (p1[X] - p2[X]) / distance
        y2p = p2[Y] + offset * (p1[X] - p2[X]) / distance
    except ValueError:
        # TODO load an error message instead
        print(p1)
        print(p2)
        print(distance)
        
    except ZeroDivisionError:
        x1p = x2p = y1p = y2p = 0
    return [x1p, y1p, p1[Z]],  [x2p, y2p, p2[Z]]

def dot_product(v1, v2, nd=3):
    result = 0
    for i in range(0, nd):
        result += v1[i] * v2[i]
    return result

def angle_of_line(p1, p2):
    xDiff = p2[0] - p1[0]
    yDiff = p2[1] - p1[1] 
    return math.degrees(math.atan2(yDiff, xDiff))

def order_points(p1, p2, nd=3):
    """Given two points swap each axes where p1 > p2 

    Args:
      p1 (point): starting point
      p2 (point): ending point
      nd (int optional): number of axes to compare defaults to 3 ie x, y, z
    Returns:
      list: returns same points with axes ordered [[x,y,z], [x,y,z]]

    Links:
    Images:"""

    for i in range(0, nd):
        if p1[i] > p2[i]:
            t1 = p1[i]
            p1[i] = p2[i]
            p2[i] = t1
    return p1, p2

def point_on_line(p1, p2, t=0.5):
    """
        #t=0 returns first point t=1 returns last point values in between are long the line
        returns a new point cordinate
    """

    direction = (p2[X] - p1[X],
                 p2[Y] - p1[Y],
                 p2[Z] - p1[Z])

    return [p1[X] + (direction[X] * t),
            p1[Y] + (direction[Y] * t),
            p1[Z] + (direction[Z] * t)]
        
def point_on_line_constrain(p1, p2, t=0.5):
    """
        #t=0 returns first point t=1 returns last point values in between are long the line
        returns a new point cordinate
    """
    direction = (p2[X] - p1[X],
                 p2[Y] - p1[Y],
                 p2[Z] - p1[Z])

    if t and t > 0.0 and t <= 1.0:
        return [p1[X] + (direction[X] * t),
                p1[Y] + (direction[Y] * t),
                p1[Z] + (direction[Z] * t)]
    else:
        return None

def points_on_line(p1, p2, p3, steps=20):
    direction1 = (p2[X] - p1[X],
                  p2[Y] - p1[Y],
                  p2[Z] - p1[Z])
    direction2 = (p3[X] - p2[X],
                  p3[Y] - p2[Y],
                  p3[Z] - p2[Z])

    #steps = 4
    jump = 1.0 / steps
    points = []
    for step in range(0, steps):
        t = jump * step
        if t and t > 0.0 and t <= 1.0:
            start = (p1[X] + (direction1[X] * t),
                     p1[Y] + (direction1[Y] * t),
                     p1[Z] + (direction1[Z] * t))

            end = (p2[X] + (direction2[X] * t),
                   p2[Y] + (direction2[Y] * t),
                   p2[Z] + (direction2[Z] * t))
            
            direction = (end[X] - start[X],
                         end[Y] - start[Y],
                         end[Z] - start[Z])

            points.append([start[X] + (direction[X] * t),
                           start[Y] + (direction[Y] * t),
                           start[Z] + (direction[Z] * t)])
    return points

#~ def line_line_intersection(p1, p2, p3, p4):
    #~ v1 = vector(p1, p2)
    #~ v2 = vector(p3, p4)
    #~ 
    #~ d = (v1[0] * v2[1]) - (v1[1] * v2[0])
    #~ print 't - %s' % dot_product(v1, v2)
    #~ print 'd = %s' % d
    #~ #r = (p1[1] - p3[1]) * (p4[0] - p3[0]) - (p1[0] - p3[x]) * p4[1] - 
    #~ d = (p2[0] - p1[0])
    #~ a = vector(p1, p3)
    #~ b = a[0] * v1[0], a[1] * v1[1], a[2] * v2[2]
    #~ c = v1[0] * v2[0], v1[1] * v2[1], v1[2] * v2[2]
    #~ #u1
    #~ 
#~ 
    #~ print b 
    #~ print c
    #~ #t = vector(p1, p3) * s / (r * s)
    
#http://paulbourke.net/geometry/pointlineplane/
#line line intersection test
def line_line_intersection_2d(p1, p2, p3, p4):
    """Given the start and end points of two line calculate if the line intersect

    Args:
      p1 (point): first line start
      p2 (point): first line end
      p3 (point): second line start
      p4 (point): second line end
      
    Returns:
      distance: return None if no intersection or distance along the line the intersection occurred

    Links:
    
    Images:"""
    a = (p4[X] - p3[X]) * (p1[Y] - p3[Y]) - (p4[Y] - p3[Y]) * (p1[X] - p3[X])
    b = (p2[X] - p1[X]) * (p1[Y] - p3[Y]) - (p2[Y] - p1[Y]) * (p1[X] - p3[X])
    c = (p4[Y] - p3[Y]) * (p2[X] - p1[X]) - (p4[X] - p3[X]) * (p2[Y] - p1[Y])

    if c == 0:
        return None

    ac = a / c
    bc = b / c  

    if bc <= 0.0 or bc >= 1.0:
        return None
    if ac <= 0.0 or ac >= 1.0:
        return None
    return (p3[X] + (p4[X] - p3[X]) * bc,
            p3[Y] + (p4[Y] - p3[Y]) * bc,
            p1[Z])


def ray_line_intersection_2d(ray_start, ray_end, line_start, line_end):
    """ calculate if a ray intersects with a line """
    a = (line_end[X] - line_start[X]) * (ray_start[Y] - line_start[Y]) - (line_end[Y] - line_start[Y]) * (ray_start[X] - line_start[X])
    b = (ray_end[X] - ray_start[X]) * (ray_start[Y] - line_start[Y]) - (ray_end[Y] - ray_start[Y]) * (ray_start[X] - line_start[X])
    c = (line_end[Y] - line_start[Y]) * (ray_end[X] - ray_start[X]) - (line_end[X] - line_start[X]) * (ray_end[Y] - ray_start[Y])

    if c == 0:
        return None

    ac = a / c
    bc = b / c  

    if bc <= 0.0:
        return None
    if ac <= 0.0 or ac >= 1.0:
        return None
    return (line_start[X] + (line_end[X] - line_start[X]) * bc,
            line_start[Y] + (line_end[Y] - line_start[Y]) * bc,
            ray_start[Z])


def ray_ray_intersection_2d(ray1_start, ray1_end, ray2_start, ray2_end):
    """ Given two rays see if they intersect, if they dont return none else return the point of intesection
    Args:
      ray1_start (point): ray1 start point
      ray1_end (point): ray1 end point
      ray2_start (point): ray2 start point
      ray2_end (point): ray2 end point
      
    Returns:
      point: intersection point or None
    """
    a = (ray2_end[X] - ray2_start[X]) * (ray1_start[Y] - ray2_start[Y]) - (ray2_end[Y] - ray2_start[Y]) * (ray1_start[X] - ray2_start[X])
    b = (ray1_end[X] - ray1_start[X]) * (ray1_start[Y] - ray2_start[Y]) - (ray1_end[Y] - ray1_start[Y]) * (ray1_start[X] - ray2_start[X])
    c = (ray2_end[Y] - ray2_start[Y]) * (ray1_end[X] - ray1_start[X]) - (ray2_end[X] - ray2_start[X]) * (ray1_end[Y] - ray1_start[Y])

    if c == 0:
        return None

    ac = a / c
    bc = b / c  

    if bc <= 0.0:
        return None
    #~ if ac <= 0.0 or ac >= 1.0:
        #~ return None
    return (ray2_start[X] + (ray2_end[X] - ray2_start[X]) * bc,
            ray2_start[Y] + (ray2_end[Y] - ray2_start[Y]) * bc,
            ray1_start[Z])

def ray_line_intersection_2d_distance(ray_start, ray_end, line_start, line_end):
    """ calculate if a ray intersects with a line return distance not the point of intersection"""
    a = (line_end[X] - line_start[X]) * (ray_start[Y] - line_start[Y]) - (line_end[Y] - line_start[Y]) * (ray_start[X] - line_start[X])
    b = (ray_end[X] - ray_start[X]) * (ray_start[Y] - line_start[Y]) - (ray_end[Y] - ray_start[Y]) * (ray_start[X] - line_start[X])
    c = (line_end[Y] - line_start[Y]) * (ray_end[X] - ray_start[X]) - (line_end[X] - line_start[X]) * (ray_end[Y] - ray_start[Y])

    if c == 0:
        return None

    ac = a / c
    bc = b / c  

    if bc <= 0.0 or bc >= 1.0:
        return None
    if ac <= 0.0:
        return None
    return bc


def ray_plane_intersection(line_start, line_end, point_on_plane, direction_vector=(0.0, 0.0, 1.0)):
    """Given a line project a ray from start to infinity and determine if the line hits the plane

    Args:
      line_start (point): line start
      line_end (point): line end
      point_on_plane (point): point on the plane
      direction_vector (vector): direction of plane
      
    Returns:
      distance: return distance along line that intersection occurred or None if no intersection

    Links:
    
    Images:"""

    a1 = dot_product((
        (point_on_plane[X] - line_start[X]),
        (point_on_plane[Y] - line_start[Y]),
        (point_on_plane[Z] - line_start[Z])), direction_vector)
    if a1 == 0:
        return None

    a2 = dot_product((
        (line_end[X] - line_start[X]),
        (line_end[Y] - line_start[Y]),
        (line_end[Z] - line_start[Z])), direction_vector)

    if a2 == 0:
        return None

    #~ intersection = a1 / a2
    #~ if intersection >= 0.0 and intersection <= 1.0:
        #~ return intersection
    return a1 / a2

def line_plane_intersection(line_start, line_end, point_on_plane, direction_vector=(0.0, 0.0, 1.0)):
    """Given line start and end point and point and direction of a plane determine if the line hits the plane

    Args:
      line_start (point): line start
      line_end (point): line end
      point_on_plane (point): point on the plane
      direction_vector (vector): direction of plane
      
    Returns:
      distance: return distance along line that intersection occurred or None if no intersection

    Links:
    
    Images:"""
    intersection =ray_plane_intersection(line_start, line_end, point_on_plane, direction_vector=(0.0, 0.0, 1.0))

    #intersection = a1 / a2
    if intersection >= 0.0 and intersection <= 1.0:
        return intersection
    return None


#reduce every thing to a single triangle
#http://en.wikipedia.org/wiki/B%C3%A9zier_curve
#http://en.wikipedia.org/wiki/B%C3%A9zier_curve
#Quadratic Bezier Curve
def points_on_curve(points, steps=20):
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
                    new_points.append([tmp_points[start][X] + (direction[X] * t),
                                       tmp_points[start][Y] + (direction[Y] * t),
                                       tmp_points[start][Z] + (direction[Z] * t)])
            tmp_points = new_points
        if new_points:
            results.append(new_points[0])
    results.append(points[-1])
    return results


#http://en.wikipedia.org/wiki/B%C3%A9zier_curve
def points_on_curve_test(points, steps=20):
    results = []
    for p in range(2, len(points)):
        results += points_on_line(points[p-2], points[p-1], points[p], 40)
    return results
