#!/usr/bin/env python
import os
import sys
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *

from kivy.graphics.opengl import glEnable

from hgl.context.template import template_context

class Renderer(template_context, Widget):
    def __init__(self, **kwargs):
        shaders = glShader()
        glEnable(0x8642) #GL_VERTEX_PROGRAM_POINT_SIZE
        glEnable(0x8861) #GL_POINT_SPRITE

        self.instructions = InstructionGroup()
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find(shaders.line_shader)
        self.point_texture = resource_find(settings.path_root + '/images/textures/png/point2.png')

        self.draw_points = RenderContext(compute_normal_mat=True)
        self.draw_points.shader.source = resource_find(shaders.point_shader)

        self.draw_lines = RenderContext(compute_normal_mat=True)
        self.draw_lines.shader.source = resource_find(shaders.line_shader)

        self.instructions.add(self.draw_points)
        self.instructions.add(self.draw_lines)

        self.w = workspace({})
        self.w.load(settings.path_root + '/models/xml/fabricad.xml')

        super(Renderer, self).__init__(**kwargs)
        self.canvas.add(self.instructions)
        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)

        # Clock.schedule_interval(self.update_glsl, 1 / 60.)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def update(self, *largs):
        aspect = self.width / float(self.height)
        projection_mat = Matrix()
        projection_mat.perspective(50.0, aspect, 10.0, 750.0)
        model = Matrix().look_at(
            0.0, 0.0, 20.0,
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0)
        self.canvas['projection_mat'] = projection_mat
        self.canvas['modelview_mat'] = model

        self.draw_points['projection_mat'] = projection_mat
        self.draw_points['modelview_mat'] = model

        self.draw_lines['projection_mat'] = projection_mat
        self.draw_lines['modelview_mat'] = model

    def line_mesh(self):

        PushMatrix()
        vertex_format = [
            ('vertex_pos', 3, 'float'),
            ('vertex_color', 4, 'float'),
        ]

        for layer_step in self.w.layers:
            if layer_step.visible:
                for packet in layer_step.data[2:3]:
                    #if packet.data_type == VERTEX_TYPE_LINE:
                    #draw_shader_lines_test(packet.vertices_vbo, packet.indices_vbo)

                    UpdateNormalMatrix()
                    self.mesh = Mesh(
                        vertices=packet.vertices,
                        indices=packet.indices,
                        fmt=vertex_format,
                        mode='triangles',
                    )
        PopMatrix()


    def setup_scene(self):
        self.w.calculate()
        Color(0, 0, 0, 1)
        with self.draw_lines:
            self.line_mesh()

        with self.draw_points:
            self.point_mesh()
    
    def point_mesh(self):
        PushMatrix()
        vertex_format = [
            ('vertex_pos', 3, 'float'),
        ]
        #Translate(0, 0, -3)
        pos = 0
        vertices = []
        indices = []
        for l in self.w.layers:
            for item in l.primitives:
                for n in l.draw_point_array:
                    vertices.append(n[0])
                    vertices.append(n[1])
                    vertices.append(n[2])
                    indices.append(pos)
                    pos += 1
        #~ vertices = [0,0,0]
        #~ indices = [0]
        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=vertices,
            indices=indices,
            fmt=vertex_format,
            mode='points',
        )

        self.mesh.texture = Image(self.point_texture).texture
        PopMatrix()


class RendererApp(App):
    def build(self):
        return Renderer()

if __name__ == "__main__":
    RendererApp().run()
