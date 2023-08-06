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
def test_context_renders(name, test_ctx, version):
    filename = '%s_%s_%d.%d.png' % (
        sys._getframe().f_code.co_name,
        name,
        version[0],
        version[1])
    actual_results = '/tmp/%s' % (filename)
    expected_results = '%s/%s' % (
        fixture_root,
        'red_triangle.png')
    ctx = test_ctx(version=version)
    ctx.save(filename=actual_results)
    ctx.quit()
    ctx = None
    assert pytest.idiff(actual_results, expected_results) is True


if __name__ == '__main__':
    test_context_renders()
