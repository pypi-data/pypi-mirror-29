import numpy
from hgl.settings import X, Y, Z, LINE_WIDTH_ZOOM, LINE_WIDTH
from hgl.calculate.line import order_points
from hgl.calculate.line import parallel_line
from hgl.calculate.line import distance_between_points


def box_from_line(line_start, line_end, width=LINE_WIDTH):
    """ Given two points return a box parallel to the line
    Args:
      p1 (point): line start
      p2 (point): line end

    Returns:
      points: four points for the box edges

    Links:
    """
    distance = distance_between_points(line_start, line_end)
    p1, p3 = parallel_line(line_start, line_end, distance, width)
    p2, p4 = parallel_line(line_start, line_end, distance, -width)
    return p1 + p2 + p3 + p4


def from_points(points):
    """ Given a list of points return a box which contains all points

    Args:
      points (points): point array

    Returns:
      points: four points for the box edges

    Links:
    """
    x1, x2 = points[0][X], points[0][X]
    y1, y2 = points[0][Y], points[0][Y]
    z1, z2 = points[0][Z], points[0][Z]
    for point in points:
        if point[X] < x1:
            x1 = point[X]
        if point[X] > x2:
            x2 = point[X]

        if point[Y] < y1:
            y1 = point[Y]
        if point[Y] > y2:
            y2 = point[Y]

        if point[Z] < z1:
            z1 = point[Z]
        if point[Z] > z2:
            z2 = point[Z]

    return (
        (x1, y1, z1),
        (x2, y1, z1),
        (x2, y2, z1),
        (x1, y2, z1))

def plane_from_width_and_height(centre, plane_width_centre, plane_height_centre):
    top_left = (
        centre[0] + (0.0 * plane_height_centre) - (1.0 * plane_width_centre),
        centre[1] + (1.0 * plane_height_centre) - (0.0 * plane_width_centre),
        centre[2] + (0.0 * plane_height_centre) - (0.0 * plane_width_centre))
    top_right = (
        centre[0] + (0.0 * plane_height_centre) + (1.0 * plane_width_centre),
        centre[1] + (1.0 * plane_height_centre) + (0.0 * plane_width_centre),
        centre[2] + (0.0 * plane_height_centre) + (0.0 * plane_width_centre))
    bottom_left = (
        centre[0] - (0.0 * plane_height_centre) - (1.0 * plane_width_centre),
        centre[1] - (1.0 * plane_height_centre) - (0.0 * plane_width_centre),
        centre[2] - (0.0 * plane_height_centre) - (0.0 * plane_width_centre))
    bottom_right = (
        centre[0] - (0.0 * plane_height_centre) + (1.0 * plane_width_centre),
        centre[1] - (1.0 * plane_height_centre) + (0.0 * plane_width_centre),
        centre[2] - (0.0 * plane_height_centre) + (0.0 * plane_width_centre))
    return top_left + top_right + bottom_left + bottom_right


def box_size_from_line(p1, p2):
    """ Given two points from a line order them and generate the width and height of the box.
    Args:
      p1 (point): line start
      p2 (point): line end

    Returns:
      points: four points for the box edges

    Links:
    """
    p1, p2 = order_points(list(p1), list(p2))
    return p2[X] - p1[X], p2[Y] - p1[Y]


def box_points_from_line(p1, p2):
    """ Given two points from a line order them and generate four coordinates representing a box
    which encompasses the line

    Args:
      p1 (point): line start
      p2 (point): line end

    Returns:
      points: four points for the box edges

    Links:
    """
    p1, p2 = order_points(list(p1), list(p2))
    width = p2[X] - p1[X]
    height = p2[Y] - p1[Y]
    #~ self.points.append(handle.create([p1[X] ,p1[Y] + self.height, p1[Z]]))
    #~ self.points.append(handle.create([p1[X], p1[Y], p1[Z]]))
    #~ self.points.append(handle.create([p1[X] + self.width, p1[Y], p1[Z]]))
    #~ self.points.append(handle.create([p1[X] + self.width, p1[Y] + self.height, p1[Z]]))
    return (
        (p1[X], p1[Y] + height, p1[Z]),
        (p1[X] + width ,p1[Y] + height, p1[Z]),
        (p1[X], p1[Y], p1[Z]),
        (p1[X] + width ,p1[Y], p1[Z]))


def box_normalized_tile_offset(x_norm, y_norm, x_tile, y_tile, size=6):
    """ Given a x normal and y normal and x and y tile with in the box return the offset
    usefull for calculating texture uniform offsets in an a texture atlas

    Args:
        x_norm: either 0 or 1 for left or right of the box
        y_norm: either 0 or 1 for the top or bottom of the box
        x_tile: x tile offset to fetch
        y_tile: y tile offset to fetch
        size: number of tiles in the grid

    Returns:
      x_norm: adjusted x normal
      y_norm: adjusted y normal

    Links:
    """
    if x_tile and y_tile >= size:
        return None
    ratio = 1.0 / size
    return ((ratio * x_tile) + x_norm * ratio, (ratio * y_tile) + y_norm * ratio)


def box_tile(box, x=1, y=0):
    """ Given 4 points of a box offset along width and height to create new parallel boxes

    Args:

    Returns:

    Links:
    """
    x_offset = box.br[X] - box.tl[X]
    y_offset = box.br[Y] - box.tl[Y]
    return (
        (box.tl[X] + x_offset * x, box.tl[Y] + y_offset * y, box.tl[Z]),
        (box.tr[X] + x_offset * x, box.tr[Y] + y_offset * y, box.tr[Z]),
        (box.bl[X] + x_offset * x, box.bl[Y] + y_offset * y, box.bl[Z]),
        (box.br[X] + x_offset * x, box.br[Y] + y_offset * y, box.br[Z]))

def is_point_in_box(box, point):
    """ Given a list or array with 4 points determin if the given point is inside the box

    Args:
        box (list): array or list [[0,0], [1,1], [2,2], [3,3]] format

    Returns:
        bool: true or false

    Links:
    """
    #outside the x coordinates
    if point[X] < box[0][X] and point[X] < box[3][X]:
        return False

    #outside the x coordinates
    if point[Y] < box[0][Y] and point[Y] < box[3][Y]:
        return False

    return True


def external_point_direction(box, point):
    """ Given a list or array with 4 points determine which direction we need to travel in relation to the box

    Args:
        box (list): array or list [[0,0], [1,1], [2,2], [3,3]] format

    Returns:
        tuple : x_direction to move y_direction to move

    Links:
    """

    x_direction = 0
    y_direction = 0

    #outside the x coordinates
    if point[X] < box[0][X]:
        x_direction = -1
    if point[X] > box[3][X]:
        x_direction = 1

    #outside the x coordinates
    if point[Y] < box[0][Y]:
        y_direction = -1

    if point[Y] > box[3][Y]:
        y_direction = 1
    return x_direction, y_direction


def inside_bounding_box(self, point, box):
    """test if point is within bounding box

    Args:
        point (list): X, Y, Z points
        box (list): minx, maxx, miny, maxy
            2d bounding box top left and bottom right coordinate

    Returns:
        bool : 1 inside 0 outside

    Links:

    """
    if point[0] < self.bounds.mins.x:
        return 0
    if point[0] > self.bounds.maxs.x:
        return 0

    if point[1] < self.bounds.mins.y:
        return 0
    if point[1] > self.bounds.maxs.y:
        return 0
    return 1


def generate_2d_bounding_box_from_points_iter(points):
    """from a list of points calculate the upper and low bounds
    Args:
       points (list): list of points with x,y,z cordinates

    Returns:
       points (list) : 4 points of a rectangle
    """
    print(points)
    xmax = max(p[X] for p in points)
    ymax = max(p[Y] for p in points)
    zmax = max(p[Z] for p in points)

    xmin = min(p[X] for p in points)
    ymin = min(p[Y] for p in points)
    zmin = min(p[Z] for p in points)

    return (xmin, ymin, 0.0), (xmax, ymax, 0.0)


def box_from_point(point, size=10.0):
    return numpy.array(
        [
            point[X] - size, point[Y] + size, point[Z],
            point[X] + size, point[Y] + size, point[Z],
            point[X] - size, point[Y] - size, point[Z],
            point[X] + size, point[Y] - size, point[Z]
        ],
        dtype=numpy.float64)
