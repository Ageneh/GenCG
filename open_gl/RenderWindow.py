"""
/*******************************************************************************
 *
 *            #, #,         CCCCCC  VV    VV MM      MM RRRRRRR
 *           %  %(  #%%#   CC    CC VV    VV MMM    MMM RR    RR
 *           %    %## #    CC        V    V  MM M  M MM RR    RR
 *            ,%      %    CC        VV  VV  MM  MM  MM RRRRRR
 *            (%      %,   CC    CC   VVVV   MM      MM RR   RR
 *              #%    %*    CCCCCC     VV    MM      MM RR    RR
 *             .%    %/
 *                (%.      Computer Vision & Mixed Reality Group
 *
 ******************************************************************************/
/**          @copyright:   Hochschule RheinMain,
 *                         University of Applied Sciences
 *              @author:   Prof. Dr. Ulrich Schwanecke
 *             @version:   0.9
 *                @date:   03.06.2019
 ******************************************************************************/
/**         RenderWindow.py
 *
 *          Simple Python OpenGL program that uses PyOpenGL + GLFW to get an
 *          OpenGL 3.2 context and display some 2D animation.
 ****
"""

import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *

from lab.scene import Scene

POINTS = []


class RenderWindow:
    """GLFW Rendering window class"""

    def __init__(self):

        # save current working directory
        cwd = os.getcwd()

        # Initialize the library
        if not glfw.init():
            return

        # restore cwd
        os.chdir(cwd)

        # version hints
        # glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, 3)
        # glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, 3)
        # glfw.WindowHint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        # glfw.WindowHint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # buffer hints
        glfw.window_hint(glfw.DEPTH_BITS, 32)

        # define desired frame rate
        self.frame_rate = 100

        # make a window
        self.width, self.height = 600, 600
        self.aspect = self.width / float(self.height)
        self.window = glfw.create_window(self.width, self.height, "2D Graphics", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)

        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        # lLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 1.0, 0.0))
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.3, 0.3, 1.0, 0.0))
        # glLightfv(GL_LIGHT0, GL_SPECULAR, (0.4, 0.4, 1.0, 0.0))

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)

        glLightfv(GL_LIGHT0, GL_POSITION, [-1, 2, 1.0, 1.0])

        # glEnable(GL_COLOR_MATERIAL)
        # glMateriali(GL_FRONT, GL_SHININESS, 128)
        glShadeModel(GL_SMOOTH)
        glFrontFace(GL_CCW)
        glEnable(GL_BLEND)

        glEnable(GL_CULL_FACE)
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)

        glEnable(GL_NORMALIZE)
        glEnable(GL_AUTO_NORMAL)
        glEnable(GL_BLEND)

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # glOrtho(-self.width / 2, self.width / 2, -self.height / 2, self.height / 2, -1.5, 1.5)
        glOrtho(-1.5, 1.5, -1.5, 1.5, -1.5, 1.5)  # multiply with new p-matrix
        # glOrtho(-3, 3, -2, 2, 1, -1)

        glMatrixMode(GL_MODELVIEW)

        # set window callbacks
        glfw.set_mouse_button_callback(self.window, self.onMouseButton)
        glfw.set_key_callback(self.window, self.onKeyboard)
        glfw.set_window_size_callback(self.window, self.onSize)

        # create 3D
        self.scene = Scene(self.width, self.height)

        # exit flag
        self.exitNow = False

        # animation flag
        self.animation = False

    def onMouseButton(self, win, button, action, mods):
        print("mouse button: ", win, button, action, mods)

    def onKeyboard(self, win, key, scancode, action, mods):
        print("keyboard: ", win, key, scancode, action, mods)
        if action == glfw.PRESS:
            # ESC to quit
            if key == glfw.KEY_ESCAPE:
                self.exitNow = True
            if key == glfw.KEY_LEFT:
                glRotate(5, 0, 1, 0)
            if key == glfw.KEY_RIGHT:
                glRotate(-5, 0, 1, 0)
            if key == glfw.KEY_UP:
                glRotate(5, 1, 0, 0)
            if key == glfw.KEY_DOWN:
                glRotate(-5, 1, 0, 0)

    def onSize(self, win, width, height):
        print("onsize: ", win, width, height)
        self.width = width
        self.height = height
        self.aspect = width / float(height)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if width <= height:
            glOrtho(-1.5, 1.5,
                    -1.5 * height / width, 1.5 * height / width,
                    -1.0, 1.0)
        else:
            glOrtho(-1.5 * self.aspect, 1.5 * self.aspect,
                    -1.5, 1.5,
                    -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)

    def run(self, vbo):
        glfw.set_time(0.0)
        time = 0.0
        while not glfw.window_should_close(self.window) and not self.exitNow:
            # update every x seconds
            now = glfw.get_time()
            if now - time > 1.0 / self.frame_rate:
                # update time
                time = now
                # clear
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                # render scene
                if self.animation:
                    self.scene.step()
                self.scene.render(vbo)

                glfw.swap_buffers(self.window)
                # Poll for and process events
                glfw.poll_events()
        # end
        glfw.terminate()
