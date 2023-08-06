#!/usr/bin/python
import os
import gc
import math
import ctypes
import OpenGL
import numpy as np
from OpenGL.GL import shaders
from OpenGL import GL
from PIL import Image
from hgl.helpers.defaults import triangle
from hgl.helpers.defaults import simple_vertex_shader
from hgl.helpers.defaults import simple_fragment_shader

# PYOPENGL_PLATFORM="osmesa"


class template_context(object):
    # camera properties
    viewport = 0, 0, 400, 400  # size of your screen / window drawing area
    viewport_centre = 200, 200  # size of your screen / window drawing area
    viewport_aspect = viewport[2] / viewport[3]
    field_of_view = math.radians(45.0)
    f = 1.0/math.tan(field_of_view/2.0)
    lookat = (0.0, 0.0, 0.0)
    location = (0.0, 0.0, -20.0)
    near_plane = 0.5
    far_plane = 100.0

    #https://stackoverflow.com/questions/12758570/pyopengl-passing-transformation-matrix-into-shader
    projection_matrix = np.array([
        f/viewport_aspect, 0.0 , 0.0,                                             0.0,
        0.0,               f,    0.0,                                             0.0,
        0.0,               0.0,  (near_plane+far_plane)/(near_plane-far_plane),   -1.0,
        0.0,               0.0,  2.0*far_plane*near_plane/(near_plane-far_plane), 0.0
    ], np.float32)

        # modelview matrix
    model_view_matrix = np.array([
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, location[2],1.0
    ], np.float32)


    # test triangle
    vertex_size = 3
    vertex_data_size = 3
    vertex_stride = vertex_size * 4
    vertex_list = triangle

    index_list = None

    texture_id = None
    texture_offset = 0

    default_vertex_shader = simple_vertex_shader
    default_fragment_shader = simple_fragment_shader

    # default_vertex_shader = ["""
    #     #version 330
    #     uniform mat4 modelview_mat;
    #     uniform mat4 projection_mat;
    #     in vec3 vertex_pos;
    #     void main()
    #     {
    #         vec4 pos = vec4(vertex_pos, 1.0);
    #         gl_Position = projection_mat * modelview_mat * pos;
    #         //gl_Position = vec4(vertex_pos, 1.0);
    #     }"""]

    # default_fragment_shader = ["""
    #     #version 330
    #     out vec4 fragColor;
    #     void main()
    #     {
    #         fragColor = vec4(1.0, 0.0, 0.0, 1.0);
    #     }"""]
    shader = None

    def __init__(self, version=(4, 5)):
        raise NotImplementedError

    def __call__(self, version=(4, 5)):
        self.__init__(version)

    def widget_error(self, widget):
        pass

    def info(self):
        print("Using %s display manager" % os.getenv('XDG_SESSION_TYPE'))
        print("PYOPENGL_PLATFORM env = %s " % os.getenv('PYOPENGL_PLATFORM', 'Not set'))

        for plugin in OpenGL.PlatformPlugin.all():
            if plugin.loaded:
                print('PYOPENGL Using %s ' % plugin.name)

    def test_opengl_methods(self):
        if bool(GL.glGenVertexArrays) is False:
            print('glGenVertexArrays not available on this machine')

    def setup_view_matrices(self):
        self.projection_matrix = np.array([
            self.f/self.viewport_aspect, 0.0, 0.0,                                             0.0,
            0.0,               self.f,    0.0,                                             0.0,
            0.0,               0.0,  (self.near_plane+self.far_plane)/(self.near_plane-self.far_plane),   -1.0,
            0.0,               0.0,  2.0*self.far_plane*self.near_plane/(self.near_plane-self.far_plane), 0.0
        ], np.float32)

            # modelview matrix
        self.model_view_matrix = np.array([
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, self.location[2], 1.0
        ], np.float32)

    def update(self):
        self.test_opengl_methods()
        self.setup_view_matrices()
        vs = shaders.compileShader(
            self.default_vertex_shader,
            GL.GL_VERTEX_SHADER)
        fs = shaders.compileShader(
            self.default_fragment_shader,
            GL.GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(vs, fs)

        # Create a new Vertex Array Object
        self.vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vertex_array_object)

        # Generate a new array buffers for our vertices
        self.vertex_buffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertex_buffer)

        # Get position variable form the shader and store
        self.position = GL.glGetAttribLocation(self.shader, 'vertex_pos')
        GL.glEnableVertexAttribArray(self.position)

        # matrix_model_view = GL.glGetFloatv(GL.GL_MODELVIEW_MATRIX)
        # matrix_projection = GL.glGetFloatv(GL.GL_PROJECTION_MATRIX)
        self.matrix_model_view_loc = GL.glGetUniformLocation(self.shader, b"modelview_mat")
        self.matrix_projection_loc = GL.glGetUniformLocation(self.shader, b"projection_mat")
# // connect the uv coords to the "vertTexCoord" attribute of the vertex shader
# glEnableVertexAttribArray(gProgram->attrib("vertTexCoord"));
# glVertexAttribPointer(gProgram->attrib("vertTexCoord"), 2, GL_FLOAT, GL_TRUE,  5*sizeof(GLfloat), (const GLvoid*)(3 * sizeof(GLfloat)));


        GL.glVertexAttribPointer(
            index=self.position,
            size=3,
            type=GL.GL_FLOAT,
            normalized=GL.GL_FALSE,
            stride=self.vertex_stride,
            pointer=ctypes.c_void_p(0))

        # if we want to draw with an index these extra steps are required
        if self.index_list is not None:
            self.index_buffer = GL.glGenBuffers(1)
            # GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.index_buffer)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
            GL.glBufferData(
                GL.GL_ELEMENT_ARRAY_BUFFER,
                self.index_list.nbytes,
                self.index_list,
                GL.GL_STATIC_DRAW)

        # because this is just for quick demos and will likely be overridden
        # give easy way of enabling a texture
        if self.texture_id is not None:
            self.tex_uniform = GL.glGetUniformLocation(self.shader, 'quad_texture')
            self.tex_coord = GL.glGetAttribLocation(self.shader, 'texture_pos')
            GL.glEnableVertexAttribArray(self.tex_coord)
            GL.glVertexAttribPointer(
                index=self.tex_coord,
                size=2,
                type=GL.GL_FLOAT,
                normalized=GL.GL_FALSE,
                stride=self.vertex_stride,
                pointer=ctypes.c_void_p(3*4))

        # Copy data to the buffer
        # data size, vertex length
        buffer_size = 4 * len(self.vertex_list)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            buffer_size,
            self.vertex_list,
            GL.GL_STATIC_DRAW)

        # Unbind buffers once done
        GL.glBindVertexArray(0)
        if self.texture_id is not None:
            GL.glDisableVertexAttribArray(self.tex_coord)
        GL.glDisableVertexAttribArray(self.position)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)

    def draw_data(self):
        if self.texture_id:
            GL.glActiveTexture(GL.GL_TEXTURE0)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
            GL.glUniform1i(self.tex_uniform, 0)
        GL.glBindVertexArray(self.vertex_array_object)
        if self.index_list is None:
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        else:
            #  use draw elements if we have an index instead of draw array
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_list), GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)

    def draw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glUseProgram(self.shader)

        GL.glUniformMatrix4fv(self.matrix_model_view_loc, 1, GL.GL_FALSE, self.model_view_matrix)
        GL.glUniformMatrix4fv(self.matrix_projection_loc, 1, GL.GL_FALSE, self.projection_matrix)
        self.draw_data()

        GL.glUseProgram(0)
        GL.glFlush()

    def render(self):
        self.draw()

    def save(self, filename='/tmp/pyopengl_context.png'):
        """Draw the context and read the pixels one by one,
        pass to pil as image an save"""
        self.draw()

        buffer = (GL.GLubyte * (4 * self.viewport[2] * self.viewport[3]))(0)

        GL.glReadPixels(
            0,
            0,
            self.viewport[2],
            self.viewport[3],
            GL.GL_RGBA,
            GL.GL_UNSIGNED_BYTE,
            buffer)

        # Use PIL to convert raw RGB buffer and flip the right way up
        image = Image.frombytes(
            mode="RGBA",
            size=(self.viewport[2], self.viewport[3]),
            data=buffer)

        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        image.save(filename)
        image.close()
        buffer = None
        self.quit()
        return filename

    def quit(self):
        gc.collect()

    def run(self):
        raise NotImplementedError

    def test(self):
        raise NotImplementedError
