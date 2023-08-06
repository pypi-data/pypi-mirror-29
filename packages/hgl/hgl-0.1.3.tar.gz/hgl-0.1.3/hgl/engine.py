from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL import GLX

try:
    from OpenGL.GLX import struct__XDisplay
except ImportError as err:
    from OpenGL.raw._GLX import struct__XDisplay


def default_states(color):
    glClearColor(color[0], color[1], color[2], color[3])
    #glClearColor(*settings.background_colour)
    glClear(GL_COLOR_BUFFER_BIT)
    glClearDepth(1.0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)

    # not available in newer opengl, will raise invalid enumerant
    # glEnable(GL_POINT_SPRITE)
    glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
    glEnable(GL_PROGRAM_POINT_SIZE)
    #~ glEnable(GL_POINT_SPRITE_ARB)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # glShadeModel(GL_SMOOTH)
    glDepthFunc(GL_LEQUAL)

    # glEnable( 0x8861 )
    # glEnable( 0x8642 )

    # glEnable(GL_TEXTURE_2D)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
