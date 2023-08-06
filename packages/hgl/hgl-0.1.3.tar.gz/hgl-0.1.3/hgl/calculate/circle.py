import math
from hgl.calculate.line import distance_between_points, point_on_line

phi = 2 * math.pi

def circle_length(radius):
    """ return the length of a circle given its radius"""
    return phi * radius


def orbit(origin, radius, time, axes=(1, 1, 0)):
    """Calculate point on circle from time and radius

    Args:
      origin (point): point to rotate around
      radius (float): radius of the circle
      time (float): time between 0 and 1 0.5 being 180 degrees
      axes (tuple): axes of rotation (1, 1, 0) to rotate around z

    Returns:
      point (point): new x y z point in time

    Links:
    
    Images:
    """
    #normalise phi, to get the angle in time
    angle = phi * time 
    rsa = radius * math.sin(angle)
    rca = radius * math.cos(angle)

    if axes[0] == 0:
        return (
            origin[0], 
            origin[1] + rca, 
            origin[2] + rsa)

    if axes[1] == 0:
        return (
            origin[0] + rca, 
            origin[1], 
            origin[2] + rsa)

    if axes[2] == 0:
        return (
            origin[0] + rsa, 
            origin[1] + rca, 
            origin[2])

def interpolate_points_from_centre(center, points, radius=2):
    """Create points for a larger circle by interpolating from the center outwards
    Args:
        center (point): circle center
        points (point list): list of points on circle circumference

    Returns:
        points (point list): new list of points interpolated from the center outwards

    Links:

    Images:
    """
    resulting_points = []
    current_radius = distance_between_points(center, points[0])
    radius_offset = (1 / current_radius) * radius

    for point in points:
        resulting_points.append(point_on_line(center, point, radius_offset))
    return resulting_points

def interpolate_between_points_from_centre(center, points, radius=2):
    """Create points for a larger circle by interpolating from the center outwards between two outer points in the circle.

    Args:
      center (point): circle center
      points (point list): list of points on circle circumference

    Returns:
      points (point list): new list of points interpolatee from the center outwards

    Links:

    Images:
    """ 
    resulting_points = []
    current_radius = distance_between_points(center, points[0])

    radius_offset = (1 / current_radius) * radius
    point_count = len(points) - 1
    for pos in range(0, point_count + 1):
        pos2 = pos + 1
        if pos == point_count:
            pos2 = 0
        middle = (
            (points[pos][0] + points[pos2][0]) * 0.5,
            (points[pos][1] + points[pos2][1]) * 0.5,
            (points[pos][2] + points[pos2][2]) * 0.5)

        resulting_points.append(point_on_line(center, middle, radius_offset))
    return resulting_points


def interpolate_points_between_outer_center(center, points, radius=2):
    """ create points for a larger circle by interpolating from the center outwards
    
    Args:
      center (point): circle center
      points (point list): list of points on circle circumference

    Returns:
      points (point list): new list of points interpolatee from the center outwards

    Links:
    
    Images:
    """ 
    resulting_points = []
    current_radius = distance_between_points(center, points[0])

    radius_offset = (1 / current_radius) * radius
    radius_offset = 0.2 #radius / current_radius
    point_count = len(points)-1
    pos = 0
    pos2 = 1
    for i in range(0, point_count):
        middle = (
            (points[pos][0] + points[pos2][0]) * 0.5,
            (points[pos][1] + points[pos2][1]) * 0.5,
            (points[pos][2] + points[pos2][2]) * 0.5)
        if i % 2 != 0:
            # move outside circle by same distance to edge from center


            end = point_on_line(center, middle, 2)
            p1 = point_on_line(points[pos], end, radius_offset)
            p2 = point_on_line(points[pos2], end, radius_offset)
            resulting_points.append(p1)
            resulting_points.append(p2)

        pos += 1
        pos2+=1
        if pos > point_count-1:
            pos=0
        if pos2 > point_count-1:
            pos2=0

    return resulting_points
