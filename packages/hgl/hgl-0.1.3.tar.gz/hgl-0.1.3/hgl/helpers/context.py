#!/usr/bin/python
import numpy as np
from hgl.context.gtkglarea_context import context
from hgl.calculate.box import plane_from_width_and_height
from hgl.calculate.box import box_from_line


def simple_primitive_context(inherited_context):
    class custom_context(context):
        box_index_list = []
        box_vertex_list = []
        points = 0
        location = (0.0, 0.0, -10.0)

        def __init__(self, shader_programs=None, version=(4, 5), points=None, lines=None):
            if lines is not None:
                self.add_line_list(lines)
            self.load_point_buffer()
            super(custom_context, self).__init__(
                shader_programs=shader_programs,
                version=version)


        def add_line_list(self, lines):
            for p1, p2 in lines:
                offset = 4 * self.points
                self.box_vertex_list += box_from_line(
                    line_start=p1, line_end=p2, width=0.035)
                self.box_index_list += 0+offset, 1+offset, 2+offset, 2+offset, 1+offset, 3+offset
                self.points += 1

        def add_point_list(self, points):
            for p in points:
                self.add_point(p)

        def add_point(self, pos):
            offset = 4 * self.points
            self.box_vertex_list += plane_from_width_and_height(
                centre=(pos[0], pos[1], pos[2]),
                plane_width_centre=0.3,
                plane_height_centre=0.3)
            self.box_index_list += 0+offset, 1+offset, 2+offset, 2+offset, 1+offset, 3+offset
            self.points += 1

        def load_point_buffer(self):
            self.vertex_list = np.array(self.box_vertex_list, dtype=np.float32)
            self.index_list = np.array(self.box_index_list, dtype=np.uint32)

    return custom_context
