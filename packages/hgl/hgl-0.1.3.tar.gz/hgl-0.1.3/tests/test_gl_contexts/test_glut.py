#!/usr/bin/python
# noqa: E402
# PYOPENGL_PLATFORM="osmesa"
import os
import sys
import pytest

from tests.helper import versions
from tests.helper import contexts
from tests.helper import fixture_root
try:
    from hgl.context.glut_context import context
except NotImplementedError:
    pytest.skip(
        "Skipping glut, hit a not implemented error probably font related")



@pytest.mark.parametrize("version", versions)
@pytest.mark.parametrize("test_ctx, name", contexts)
def test_glut_context_renders(name, test_ctx, version):
    actual_results = '%s_%s_%d.%d.png' % (
        sys._getframe().f_code.co_name,
        name,
        version[0],
        version[1])
    # actual_results = '/tmp/%s.png' % name
    expected_results = '%s/red_triangle.png' % fixture_root
    context(version=version).save(filename=actual_results)
    assert pytest.idiff(actual_results, expected_results) is True

#def test_glut_33_context_r# enders():
#     actual_results = '/tmp/%s.png' % sys._getframe().f_code.co_name
#     expected_results = '%s/red_triangle.png' % fixture_root
#     context().save(filename=actual_results)
#     assert pytest.idiff(actual_results, expected_results) is True


# def test_glut_40_context_renders():
#     actual_results = '/tmp/%s.png' % sys._getframe().f_code.co_name
#     expected_results = '%s/red_triangle.png' % fixture_root
#     context(version=(4, 0)).save(filename=actual_results)
#     assert pytest.idiff(actual_results, expected_results) is True


# def test_glut_43_context_renders():
#     actual_results = '/tmp/%s.png' % sys._getframe().f_code.co_name
#     expected_results = '%s/red_triangle.png' % fixture_root
#     context(version=(4, 3)).save(filename=actual_results)
#     assert pytest.idiff(actual_results, expected_results) is True


# # currently seg faults
# def test_glut_45_context_renders():
#     actual_results = '/tmp/%s.png' % sys._getframe().f_code.co_name
#     expected_results = '%s/red_triangle.png' % fixture_root
#     context(version=(4, 5)).save(filename=actual_results)
#     assert pytest.idiff(act
#                        ual_results, expected_results) is True


if __name__ == '__main__':
    test_glut_context_renders()
    # test_glut_40_context_renders()
    # test_glut_43_context_renders()
    # test_glut_45_context_renders()
