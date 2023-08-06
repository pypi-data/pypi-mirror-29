#!/usr/bin/env python
import pygame_sdl2
from pygame_sdl2.locals import OPENGL, DOUBLEBUF

from OpenGL import GL

from hgl.context.template import template_context

# os.environ['SDL_VIDEODRIVER'] = 'dummy'
# os.environ['SDL_VIDEODRIVER'] = 'directfb'
# os.environ['SDL_VIDEODRIVER'] = "fbcon"
# os.environ['SDL_VIDEODRIVER'] = "aalib"


class context(template_context):
    """Basic opengl context using pygage widget"""
    def __init__(self, shader_programs=None, version=(3, 3)):
        pygame_sdl2.init()
        # https://github.com/renpy/pygame_sdl2.sdl2/issues/37
        # pygame_sdl2.display.gl_set_attribute(GL_ALPHA_SIZE, 8)

        pygame_sdl2.display.gl_set_attribute(
            pygame_sdl2.GL_CONTEXT_MAJOR_VERSION,
            version[0])
        pygame_sdl2.display.gl_set_attribute(
            pygame_sdl2.GL_CONTEXT_MINOR_VERSION,
            version[1])

        # SDL_GL_CONTEXT_PROFILE_CORE = 1
        # SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG = 2
        # pygame_sdl2.display.gl_set_attribute(pygame_sdl2.GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
        # pygame_sdl2.display.gl_set_attribute(pygame_sdl2.GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG)

        pygame_sdl2.display.set_mode(
            (self.viewport[2], self.viewport[3]),
            OPENGL | DOUBLEBUF
        )

        self.update()

    def info(self):
        print('Created SDL context')
        super(context, self).info()
        print('Pygame sdl2 version %s.%s.%s' % pygame_sdl2.get_sdl_version())
        print('Pygame sdl2 driver %s' % pygame_sdl2.display.get_driver())

    def save(self, filename='/tmp/gtkgl_context.png'):
        pygame_sdl2.display.flip()
        return super(context, self).save(filename=filename)

    def render(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        super(context, self).render()
        pygame_sdl2.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame_sdl2.event.get():
                if event.type == pygame_sdl2.QUIT:
                    running = False
            self.render()
        pygame_sdl2.quit()

    def quit(self):
        pygame_sdl2.display.quit()
        pygame_sdl2.quit()
        super(context, self).quit()
