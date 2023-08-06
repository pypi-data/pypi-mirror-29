#!/usr/bin/python
# noqa: E402
# PYOPENGL_PLATFORM="osmesa"
import sys
import pytest
from tests.helper import fixture_root
context = pytest.importorskip("hgl.context.pygame_context.context")


def test_pygame_33_context_renders():
    actual_results = '/tmp/%s.png' % sys._getframe().f_code.co_name
    expected_results = '%s/red_triangle.png' % fixture_root
    context().save(filename=actual_results)
    assert pytest.idiff(actual_results, expected_results) is True


def test_pygame_40_context_renders():
    actual_results = '/tmp/%s.png' % sys._getframe().f_code.co_name
    expected_results = '%s/red_triangle.png' % fixture_root
    context(version=(4, 0)).save(filename=actual_results)
    assert pytest.idiff(actual_results, expected_results) is True


def test_pygame_43_context_renders():
    actual_results = '/tmp/%s.png' % sys._getframe().f_code.co_name
    expected_results = '%s/red_triangle.png' % fixture_root
    context(version=(4, 3)).save(filename=actual_results)
    assert pytest.idiff(actual_results, expected_results) is True


def test_pygame_45_context_renders():
    actual_results = '/tmp/%s.png' % sys._getframe().f_code.co_name
    expected_results = '%s/red_triangle.png' % fixture_root
    context(version=(4, 5)).save(filename=actual_results)
    assert pytest.idiff(actual_results, expected_results) is True


if __name__ == '__main__':
    test_pygame_33_context_renders()
    test_pygame_40_context_renders()
    test_pygame_43_context_renders()
    test_pygame_45_context_renders()
