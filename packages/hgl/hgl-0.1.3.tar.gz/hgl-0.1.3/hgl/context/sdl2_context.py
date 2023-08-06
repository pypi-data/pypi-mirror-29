#!/usr/bin/env python
import sys
import sdl2
import ctypes
from sdl2 import video
from OpenGL import GL
from hgl.context.template import template_context

# os.environ['SDL_VIDEODRIVER'] = 'dummy'
# os.environ['SDL_VIDEODRIVER'] = 'directfb'
# os.environ['SDL_VIDEODRIVER'] = "fbcon"
# os.environ['SDL_VIDEODRIVER'] = "aalib"
import gc

class context(template_context):
    """Basic opengl context using pygage widget"""
    def __init__(self, shader_programs=None, version=(3, 3)):
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            print(sdl2.SDL_GetError())
            return -1

        self.window = sdl2.SDL_CreateWindow(
            b"SDL2 OpenGL Context",
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            self.viewport[2],
            self.viewport[3],
            sdl2.SDL_WINDOW_OPENGL)
        if not self.window:
            print(sdl2.SDL_GetError())
            return -1

        # Force OpenGL 3.3 'core' context.
        # Must set *before* creating GL context!
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, version[0])
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, version[1])
        video.SDL_GL_SetAttribute(
            video.SDL_GL_CONTEXT_PROFILE_MASK, video.SDL_GL_CONTEXT_PROFILE_CORE)
        self.context = sdl2.SDL_GL_CreateContext(self.window)

        self.update()

    def info(self):
        print('Created SDL context')
        super(context, self).info()
        print('Pygame sdl2 version %s.%s.%s' % pygame_sdl2.get_sdl_version())
        print('Pygame sdl2 driver %s' % pygame_sdl2.display.get_driver())

    def render(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        super(context, self).render()
        sdl2.SDL_GL_SwapWindow(self.window)

    def run(self):
        event = sdl2.SDL_Event()
        running = True
        while running:
            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                elif (event.type == sdl2.SDL_KEYDOWN and
                    event.key.keysym.sym == sdl2.SDLK_ESCAPE):
                    running = False
            self.render()

    def quit(self):
        sdl2.SDL_GL_DeleteContext(self.context)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()
        gc.collect()
