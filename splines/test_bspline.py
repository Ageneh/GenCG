import os

import glfw
from OpenGL.GL import *

from splines.scene import Scene


class RenderWindow:

    def __init__(self):
        cwd = os.getcwd()

        if not glfw.init():
            return

        os.chdir(cwd)
        # glfw.window_hint(glfw.DEPTH_BITS, 32)

        # define desire frame rate
        self.frame_rate = 100

        # make a window
        self.width, self.height = 640, 740
        self.aspect = self.width / float(self.height)
        self.window = glfw.create_window(self.width, self.height, "B-Spline-Kurve", None, None)
        if not self.window:
            glfw.terminate()
            return

        self.initGLFW()
        self.initGL()

        self.scene = Scene()

        self._shift = False
        self._exit = False
        self._render = False

    # DONE
    def initGL(self):
        glViewport(0, 0, self.width, self.height)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glMatrixMode(GL_MODELVIEW)

    # DONE
    def initGLFW(self):
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.on_key)
        glfw.set_mouse_button_callback(self.window, self.on_click)

    # DONE
    def run(self):
        glfw.set_time(0.0)
        t = 0.0
        while not glfw.window_should_close(self.window) and not self._exit:
            # update everx x seconds
            currT = glfw.get_time()
            if currT - t > 1.0 / self.frame_rate:
                # update time
                t = currT
                # clear
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                # render
                self.scene.render()

                glfw.swap_buffers(self.window)
                # Poll for and process events
                glfw.poll_events()

        # end
        glfw.terminate()

    # DONE
    def on_click(self, window, button, action, mods):
        _pos = lambda _x, _y: _x / _y * 2 - 1
        x, y = glfw.get_cursor_pos(window)

        if action == glfw.RELEASE:
            if button == glfw.MOUSE_BUTTON_LEFT:
                x = _pos(x, self.width)
                y = -_pos(y, self.height)

                self.scene.add_point([x, y])

    # DONE
    def on_key(self, window, key, scancode, action, mods):
        degree = self.scene.get_degree()
        pointcount = self.scene.get_pointcount()

        if key == glfw.KEY_ESCAPE:
            if action == glfw.RELEASE:
                self._exit = True
            return
        elif key == glfw.KEY_LEFT_SHIFT or key == glfw.KEY_RIGHT_SHIFT:
            self._shift = True if action == glfw.PRESS else False
            return
        elif key == glfw.KEY_M:
            if action == glfw.RELEASE:
                return
            if self._shift:
                self.scene.increase(Scene.PARAM_POINTS)
            else:
                if pointcount > 2:
                    # needs to be at least 1 or else last section will be cut off
                    self.scene.decrease(Scene.PARAM_POINTS)
            return
        elif key == glfw.KEY_K:
            if action == glfw.RELEASE:
                return
            # changing curve degree
            if self._shift:
                self.scene.increase(Scene.PARAM_DEGREE)
            else:
                self.scene.decrease(Scene.PARAM_DEGREE)
            return
        elif key == glfw.KEY_R:
            # reset points
            if action == glfw.RELEASE:
                return
            self.scene.reset_errythang()
            return
