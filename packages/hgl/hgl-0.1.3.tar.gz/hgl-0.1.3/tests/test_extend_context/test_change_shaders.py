#!/usr/bin/python
# noqa: E402
# PYOPENGL_PLATFORM="osmesa"
import sys
import pytest

from tests.helper import versions
from tests.helper import contexts
from tests.helper import fixture_root


@pytest.mark.parametrize("version", versions)
@pytest.mark.parametrize("test_ctx, name", contexts)
def test_change_shaders(name, test_ctx, version):
    filename = '%s_%s_%d.%d.png' % (
        sys._getframe().f_code.co_name,
        name,
        version[0],
        version[1])
    actual_results = '/tmp/%s' % (filename)
    expected_results = '%s/%s' % (
        fixture_root,
        'yellow_triangle.png')

    class custom_context(test_ctx):
        default_fragment_shader = ["""
            #version 330
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(1.0, 1.0, 0.0, 1.0);
            }"""]

    new_ctx = custom_context(version=version)
    new_ctx.save(filename=actual_results)
    new_ctx.quit()
    assert pytest.idiff(actual_results, expected_results) is True


if __name__ == '__main__':
    test_change_shaders()
