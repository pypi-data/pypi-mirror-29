import math
from hgl.calculate import X, Y, Z

def distance_between_all_points(points):
    if not points:
        return 0
    length = 0
    for pos in range(0, len(points)-1):
        length += distance_between_points(points[pos], points[pos + 1])
    return length


def distance_between_points(p1, p2):
    d1 = p2[0] - p1[0]
    d2 = p2[1] - p1[1]
    d3 = p2[2] - p1[2]
    return math.sqrt((d1 * d1) + (d2 * d2) + (d3 * d3))


def parallel_line(p1, p2, distance, offset):
    self.calculate_distance()
    x1p = self.p1[0] + offset * (self.p2[1] - self.p1[1]) / self.distance
    x2p = self.p2[0] + offset * (self.p2[1] - self.p1[1]) / self.distance
    y1p = self.p1[1] + offset * (self.p1[0] - self.p2[0]) / self.distance
    y2p = self.p2[1] + offset * (self.p1[0] - self.p2[1]) / self.distance
    return [x1p, y1p, self.p1[2]],  [x2p, y2p, self.p2[2]]

