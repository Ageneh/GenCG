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
from OpenGL.raw.GLU import gluLookAt
from numpy import sqrt, arccos, cross, dot

from scene import Scene

POINTS = []
orthoN = 1.5

colors = {
    glfw.KEY_K: (0.0, 0.0, 0.0, 1.0),
    glfw.KEY_B: (0.0, 0.0, 1.0, 1.0),
    glfw.KEY_G: (0.0, 1.0, 0.0, 1.0),
    glfw.KEY_R: (1.0, 0.0, 0.0, 1.0),
    glfw.KEY_Y: (1.0, 1.0, 0.0, 1.0),  # yellow on Z for qwerty
    glfw.KEY_Z: (1.0, 1.0, 0.0, 1.0),  # yellow on Z for qwertz
    glfw.KEY_W: (1.0, 1.0, 1.0, 1.0),
}


class RenderWindow:
    """GLFW Rendering window class"""

    def __init__(self):
        cwd = os.getcwd()  # save current working directory
        if not glfw.init(): return  # Initialize the library

        self.projection = {
            glfw.KEY_O: self.projectionorthogonal,
            glfw.KEY_P: self.projectionperspective,
        }

        # make a window
        self.width, self.height = 600, 600
        self.aspect = self.width / float(self.height)
        self.window = glfw.create_window(self.width, self.height, "2D Graphics", None, None)
        if not self.window:
            glfw.terminate()
            return

        self.scene = Scene(self.width, self.height)  # create 3D
        self.setBGColor = False
        self.exitNow = False  # exit flag
        self.animation = False  # animation flag
        self.pressed = False
        self.movement = False
        self.mouseLeft = False
        self.mouseRight = False
        self.rotationVal = (0, 0, 0)
        self.startPos = (0, 0)
        self.scalefactor = 0
        self.frame_rate = 100  # define desired frame rate

        # set window callbacks
        os.chdir(cwd)  # restore cwd
        self.initGLFW()
        self.initGL()
        self.scene.translate(0, -1)

    # DONE
    def initGLFW(self):
        glfw.set_mouse_button_callback(self.window, self.onMouseButton)
        glfw.set_key_callback(self.window, self.onKeyboard)
        glfw.set_window_size_callback(self.window, self.onSize)
        glfw.set_cursor_pos_callback(self.window, self.onMouseMove)
        glfw.set_scroll_callback(self.window, self.onScroll)
        glfw.window_hint(glfw.DEPTH_BITS, 32)  # buffer hints
        glfw.make_context_current(self.window)  # Make the window's context current

    # DONE
    def initGL(self):
        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)

        glClearColor(1.0, 1.0, 1.0, 1.0)

        glLightfv(GL_LIGHT0, GL_POSITION, [-1, 2, 1.0, 1.0])

        glEnable(GL_COLOR_MATERIAL)
        glMateriali(GL_FRONT, GL_SHININESS, 128)
        glShadeModel(GL_SMOOTH)
        glFrontFace(GL_CCW)
        glEnable(GL_BLEND)

        glEnable(GL_CULL_FACE)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glEnable(GL_NORMALIZE)
        glEnable(GL_AUTO_NORMAL)
        glEnable(GL_BLEND)
        gluLookAt(
            0.0, 2.0, 2,
            0, 0, 0.0,
            0.0, 1.0, 0.0
        )

        self.projectionperspective()

    # DONE
    def onMouseButton(self, win, button, action, mods):

        # print("mouse button: ", win, button, action, mods)
        # if button == glfw.MOUSE_BUTTON_LEFT:
        #     if action == glfw.PRESS:
        #         self.pressed = True
        #     elif action == glfw.RELEASE:
        #         self.pressed = False
        #         self.scene.rotate(self.scene.angle, self.scene.axis)
        #         self.scene.angle = 0

        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                self.mouseLeft = True
            elif action == glfw.RELEASE:
                self.mouseLeft = False
                self.scene.rotate()
                self.scene.angle = 0
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            if action == glfw.PRESS:
                self.mouseRight = True
            elif action == glfw.RELEASE:
                self.mouseRight = False

        # if action == glfw.PRESS:
        #     if button == glfw.MOUSE_BUTTON_LEFT:
        #         self.mouseLeft = True
        #     if button == glfw.MOUSE_BUTTON_RIGHT:
        #         self.mouseRight = True
        # elif action == glfw.RELEASE:
        #     if button == glfw.MOUSE_BUTTON_LEFT:
        #         self.mouseLeft = False
        #         # self.scene.rotate()
        #         self.scene.rotate(self.scene.angle, self.scene.axis)
        #         self.scene.angle = 0
        #     if button == glfw.MOUSE_BUTTON_RIGHT:
        #         self.mouseRight = False

    # DONE
    def onMouseMove1(self, window, x, y):
        r = min(self.width, self.height) / 2.0

        if self.mouseLeft:
            rotation_current_point = self.projectontosphere(x, y, r)

            if rotation_current_point == self.rotationVal:
                return

            self.scene.rotationAngle = arccos(dot(self.rotationVal, rotation_current_point))
            self.scene.rotation_axis = cross(self.rotationVal, rotation_current_point)

        if self.mouseRight:
            x_dir, y_dir = x - self.startPos[0], self.startPos[1] - y
            self.scene.translate(x_dir / self.width, y_dir / self.height)

        self.rotationVal = self.projectontosphere(x, y, r)
        self.startPos = (x, y)

        return self.rotationVal

    # DONE
    def onMouseMove(self, window, x, y):
        r = min(self.width, self.height) / 2.0

        if self.mouseLeft:
            moveP = self.projectontosphere(x, y, r)
            self.scene.angle = arccos(dot(self.rotationVal, moveP))
            self.scene.axis = cross(self.rotationVal, moveP)

        if self.mouseRight:
            movementDelta = x - self.movement[0], self.movement[1] - y
            xDelta, yDelta = movementDelta
            self.scene.translate(xDelta / self.width, yDelta / self.height)

        self.rotationVal = self.projectontosphere(x, y, r)
        # print("moved", self.movement, x, y)
        self.movement = (x, y)

        # r = min(self.width, self.height) / 2.0
        # if self.pressed:
        #     moveP = self.projectontosphere(x, y, r)
        #     self.scene.angle = arccos(dot(self.startP, moveP))
        #     self.scene.axis = cross(self.startP, moveP)
        # self.startP = self.projectontosphere(y, y, r)
        return self.rotationVal

    # DONE
    def onScroll(self, window, x, y):
        # self.scene.translate(10 * (x / self.width), 0)
        self.scalefactor += y if y > 0 else -(self.scalefactor - y)
        self.scene.scale(self.scalefactor)

    # DONE
    def onKeyboard(self, win, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE:
            self.exit_now = True
            return
        elif key == glfw.KEY_LEFT_SHIFT or key == glfw.KEY_RIGHT_SHIFT:
            self.setBGColor = True if action == glfw.PRESS else False
            return
        elif key in self.projection.keys():
            self.projection[key]()
            return
        elif key == glfw.KEY_H:
            if action == glfw.RELEASE:
                self.scene.hasShadow = not self.scene.hasShadow
            return
        elif key in colors.keys():
            r, g, b, a = colors.get(key)
            if self.setBGColor:
                glClearColor(r, g, b, a)
            else:
                self.scene.color = (r, g, b)
            return

    # DONE
    def onSize(self, win, width, height):
        # print("onsize: {}, {}, {}".format(win, width, height))
        self.width = width
        self.height = height
        self.aspect = width / float(height)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if width <= height:
            glOrtho(-orthoN, orthoN, -orthoN * (height / width), orthoN * (height / width), -orthoN, orthoN)
        else:
            glOrtho(-orthoN * (width / height), orthoN * (width / height), -orthoN, orthoN, -orthoN, orthoN)
        glMatrixMode(GL_MODELVIEW)

        pass

    # DONE
    def projectontosphere(self, x, y, r):
        x, y = x - self.width / 2., y - self.height / 2.
        a = min(r ** 2, x ** 2 + y ** 2)
        z = sqrt(r ** 2 - a)
        l = sqrt(x ** 2 + y ** 2 + z ** 2)
        return x / l, y / l, z / l

    # DONE
    def projectionorthogonal(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        n = 1.5
        if self.width <= self.height:
            glOrtho(
                -n, n,
                -n * self.height / self.width, n * self.height / self.width,
                -2.0, 5.0
            )
        else:
            glOrtho(
                -n * self.width / self.height, n * self.width / self.height,
                -n, n,
                -2.0, 5.0
            )

        glMatrixMode(GL_MODELVIEW)

    # DONE
    def projectionperspective(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.width <= self.height:
            n = 0.5
            glFrustum(
                -n, n,
                -n * self.height / self.width, n * self.height / self.width,
                n, n * 10
            )
        else:
            n = 1.5
            glFrustum(
                -n * self.width / self.height, n * self.width / self.height,
                -n, n,
                n, n * 10
            )

        glMatrixMode(GL_MODELVIEW)

    # DONE
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

                self.scene.render(vbo)

                glfw.swap_buffers(self.window)
                # Poll for and process events
                glfw.poll_events()
        # end
        glfw.terminate()
