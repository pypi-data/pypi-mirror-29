#!/usr/bin/python
# noqa: E402
# PYOPENGL_PLATFORM="osmesa"
import os
import sys
import pytest

from hgl.context.gtkglarea_context import context

from tests.helper import versions
from tests.helper import contexts
from tests.helper import fixture_root


@pytest.mark.parametrize("version", versions)
@pytest.mark.parametrize("test_ctx, name", contexts)
def test_gtkgl_context_renders(name, test_ctx, version):
    actual_results = '/tmp/%s.png' % sys._getframe().f_code.co_name
    actual_results = '%s_%s_%d.%d.png' % (
        sys._getframe().f_code.co_name,
        name,
        version[0],
        version[1])
    expected_results = '%s/red_triangle.png' % fixture_root 
    context(version=version).save(filename=actual_results)
    assert pytest.idiff(actual_results, expected_results) is True


# def test_gtkgl_40_context_renders():
#     actual_results = '/tmp/%s.png' % sys._getframe().f_code.co_name
#     expected_results = '%s/red_triangle.png' % fixture_root
#     context(version=(4, 0)).save(filename=actual_results)
#     assert pytest.idiff(actual_results, expected_results) is True


# def test_gtkgl_43_context_renders():
#     actual_results = '/tmp/%s.png' % sys._getframe().f_code.co_name
#     expected_results = '%s/red_triangle.png' % fixture_root
#     context(version=(4, 3)).save(filename=actual_results)
#     assert pytest.idiff(actual_results, expected_results) is True


# def test_gtkgl_45_context_renders():
#     actual_results = '/tmp/test_gtkgl_45_context_renders.png'
#     expected_results = '%s/red_triangle.png' % fixture_root
#     context(version=(4, 5)).save(filename=actual_results)
#     assert pytest.idiff(actual_results, expected_results) is True


if __name__ == '__main__':
    # context(version=(4, 5)).run()
    # context(version=(4, 5)).save(filename='/tmp/test.png')
    test_gtkgl_context_renders()
    # test_gtkgl_40_context_renders()
    # test_gtkgl_43_context_renders()
    # test_gtkgl_45_context_renders()
