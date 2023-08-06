#!/usr/bin/python
# noqa: E402
# PYOPENGL_PLATFORM="osmesa"
import os
import sys
import pytest
import numpy as np
from OpenGL import GL
from tests.helper import versions
from tests.helper import contexts
from tests.helper import fixture_root
from hgl.helpers.defaults import simple_texture_fs
from hgl.helpers.defaults import simple_texture_vs
from hgl.helpers.defaults import square, triangle_uv
from hgl.libs.textures import load_texture


@pytest.mark.parametrize("version", versions)
@pytest.mark.parametrize("test_ctx, name", contexts)
def test_change_vertex_array(name, test_ctx, version):
    filename = '%s_%s_%d.%d.png' % (
        sys._getframe().f_code.co_name,
        name,
        version[0],
        version[1])
    actual_results = '/tmp/%s' % (filename)
    expected_results = '%s/%s' % (
        fixture_root,
        'red_square.png')

    class custom_context(test_ctx):
        vertex_list = square

        def draw_data(self):
            GL.glBindVertexArray(self.vertex_array_object)
            GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, 4)
            GL.glBindVertexArray(0)

    new_ctx = custom_context(version=version)
    new_ctx.save(filename=actual_results)
    new_ctx.quit()
    assert pytest.idiff(actual_results, expected_results) is True


@pytest.mark.parametrize("version", versions)
@pytest.mark.parametrize("test_ctx, name", contexts)
def test_extend_for_texture(name, test_ctx, version):
    filename = '%s_%s_%d.%d.png' % (
        sys._getframe().f_code.co_name,
        name,
        version[0],
        version[1])
    actual_results = '/tmp/%s' % (filename)
    expected_results = '%s/%s' % (
        fixture_root,
        'textured_triangle.png')

    class custom_context(test_ctx):
        vertex_list = triangle_uv
        vertex_size = 5
        vertex_stride = 4 * vertex_size

        default_vertex_shader = simple_texture_vs
        default_fragment_shader = simple_texture_fs

        def update(self):
            self.texture_id = load_texture(filename=os.path.abspath('./tests/textures/testing.png'))
            super(custom_context, self).update()

    my_ctx = custom_context(version=version)
    my_ctx.save(filename=actual_results)
    my_ctx.quit()
    #Seems there are very slight difference when rendering the texture
    assert pytest.idiff(actual_results, expected_results, tolerance=0.01) is True

if __name__ == '__main__':
    test_change_vertex_array()
