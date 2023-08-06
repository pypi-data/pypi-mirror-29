# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as _build_ext

class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())

with open('README.org') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

requirements = [
    'pyopengl',
    'numpy',
    'pillow',
    'pysdl2'
#    'pygame-sdl'
]

dependency_links=[
#    'https://github.com/renpy/pygame_sdl2/archive/master.zip#egg=pygame_sdl2'
    # 'https://github.com/renpy/pygame_sdl2/tarball/master#egg=pygame-sdl2'
    # 'https://github.com/olymk2/pygame-sdl2/tarball/master#egg=pygame-sdl2'
#    'git+ssh://git@github.com/renpy/pygame_sdl2.git/@master#egg=pygame_sdl2'
    'https://bitbucket.org/marcusva/py-sdl2/downloads/PySDL2-0.9.5.zip'
]

setup(
    name='hgl',
    version='0.1.3',
    description='Simple OpenGL helper library for testing code and writting examples with minimal fuss',
    long_description=readme,
    author='Oliver Marks',
    author_email='oly@digitaloctave.com',
    url='https://github.com/olymk2/hgl',
    license=license,
    package_data={'hgl': ['README.org', 'LICENSE']},
    packages=find_packages(exclude=('tests', 'docs')),
    cmdclass={'build_ext':build_ext},
    install_requires=requirements,
    dependency_links=dependency_links,
    setup_requires=['cython', 'numpy', 'pytest-runner'],
    tests_require=['pytest-inomaly', 'pytest-cov', 'pytest']
)
