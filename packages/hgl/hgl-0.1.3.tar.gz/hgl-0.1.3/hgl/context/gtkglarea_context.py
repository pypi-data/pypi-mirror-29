#!/usr/bin/python
# noqa: E402
import gi
import time
import numpy as np

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject
from OpenGL import GLU
from OpenGL import GL
from hgl.context.template import template_context


class context(template_context):
    """Basic opengl context using gtkgl widget"""
    on_draw_displayed = False

    def __init__(self, shader_programs=None, version=(4, 5)):
        self.display = Gdk.Display.get_default()
        print(self.display)
        self.screen = Gdk.Screen.get_default()
        print(self.screen)
        self.visual = Gdk.Screen.get_rgba_visual(self.screen)

        self.window = Gtk.Window()
        print(self.window)
        self.window.set_default_size(self.viewport[2], self.viewport[3])

        Gtk.Widget.set_visual(self.window, self.visual)

        self.canvas = Gtk.GLArea()
        self.canvas.set_required_version(version[0], version[1])

        self.canvas.connect('unrealize', self.on_unrealize)
        self.canvas.connect('realize', self.on_realize)
        self.canvas.connect('render', self.on_draw)
        self.canvas.set_double_buffered(False)
        self.canvas.set_has_alpha(True)

        self.window.connect('delete_event', Gtk.main_quit)
        self.window.connect('destroy', lambda quit: Gtk.main_quit())

        self.window.add(self.canvas)
        self.window.show_all()
        self.info()

    def widget_error(self, widget):
        e = widget.get_error()
        if e:
            print(e)

    def info(self):
        print('Created GTKGLAREA context')
        super(context, self).info()
        canvas_context = self.canvas.get_context()
        canvas_context.make_current()
        print('Testing features')
        print('Detected Visuals')
        for current_visual in Gdk.Screen.list_visuals(self.screen):
            print("\t%s - %s" % (current_visual.get_depth(), current_visual.get_visual_type()))
        print('Selected Visuals')
        print("\t%s - %s" % (self.visual.get_depth(), self.visual.get_visual_type()))

        print('is composite %s' % Gdk.Screen.is_composited(self.screen))
        print(canvas_context.get_version())
        print('glcontext version %d.%d' % canvas_context.get_version())
        # print('glcontext legacy %s' % canvas_context.is_legacy())
        # print('glGenVertexArrays Available %s' % bool(glGenVertexArrays))
        print('Alpha Available %s' % bool(self.canvas.get_has_alpha()))
        print('Depth buffer Available %s' % bool(self.canvas.get_has_depth_buffer()))
        print(GL.GL_VENDOR)

        print(b'%s_%s_%s_%s' % (
            GL.glGetString(GL.GL_VENDOR).replace(b' ', b'_'), 
            GL.glGetString(GL.GL_VERSION).replace(b' ', b'_'), 
            GL.glGetString(GL.GL_RENDERER).replace(b' ', b'_'),
            GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).replace(b' ', b'_')))
        print('OpenGL Version %s' % GL.glGetString(GL.GL_VERSION).replace(b' ', b'_'))
        print('OpenGL Renderer %s' % GL.glGetString(GL.GL_RENDERER).replace(b' ', b'_'))
        print('Shader Language version %s' % GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).replace(b' ', b'_'))
        print('Finished feature detection')


    def on_unrealize(self, widget):
        context.make_current()
        return True

    def on_realize(self, widget):
        widget.make_current()
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.widget_error(widget)
        self.update()
        return True

    def on_draw(self, widget, *args):
        self.on_draw_displayed = True
        self.widget_error(widget)
        self.draw()
        return True

    def handle_events(self):
        while Gtk.events_pending():
            Gtk.main_iteration_do(blocking=True)

    def save(self, filename='/tmp/gtkgl_context.png'):
        self.canvas.queue_draw()
        while self.on_draw_displayed is False:
            self.handle_events()
        self.canvas.make_current()
        self.update()
        return super(context, self).save(filename=filename)
        self.quit()

    def run(self):
        Gtk.main()

    def quit(self):
        self.handle_events()
        self.window.hide()
        print(Gtk.main_level())
        Gtk.main_quit()
