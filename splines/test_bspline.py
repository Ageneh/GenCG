import glfw
import numpy as np
import os
from OpenGL.GL import *
from OpenGL.arrays import vbo


class Scene:
    PARAM_DEGREE = "degree"
    PARAM_POINTS = "pointCount"

    def __init__(self):
        self.values = {
            Scene.PARAM_DEGREE: 3,
            Scene.PARAM_POINTS: 2,
        }
        self.valueLimits = {
            Scene.PARAM_DEGREE: {
                "min": 1,
                "max": lambda: self.get_pointcount(),
            },
            Scene.PARAM_POINTS: {
                "min": 1,
                "max": lambda: self.get_degree(),
            },
        }
        self.points = []
        self.curvepoints = []
        self.knotvector = []

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)

        myVbo = vbo.VBO(np.array(self.points, 'f'))
        myVbo.bind()

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, myVbo)

        glColor([0.0, 0.0, 0.0])
        glPointSize(5.0)

        glDrawArrays(GL_POINTS, 0, len(self.points))
        if len(self.points) > 1:
            glDrawArrays(GL_LINE_STRIP, 0, len(self.points))

        if len(self.points) >= self.get_param(self.PARAM_DEGREE):
            curveVbo = vbo.VBO(np.array(self.curvepoints, 'f'))
            curveVbo.bind()

            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(2, GL_FLOAT, 0, curveVbo)

            glColor([1.0, 0, 0])

            glDrawArrays(GL_LINE_STRIP, 0, len(self.curvepoints))
            curveVbo.unbind()

        myVbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)

        glFlush()

    # DONE
    def calc_curve(self):
        if self.get_degree() > len(self.points):
            print self.get_pointcount(), len(self.points), self.points
            return

        self.curvepoints = []

        degree = self.get_degree()
        self.knotvector = self.calc_knotvector(len(self.points), degree)

        m = len(self.knotvector) - 1

        for j in range(degree - 1, m - degree + 1):
            if self.knotvector[j] != self.knotvector[j + 1]:
                for t in np.linspace(self.knotvector[j], self.knotvector[j + 1], self.get_pointcount()):
                    p = self.deboor(degree, self.points, self.knotvector, j, t)
                    self.curvepoints.append(p)

    # DONE
    def calc_knotvector(self, points_len, degree):
        knotvector = []

        for t in range(degree):
            knotvector.append(0)
        for t in range(1, (points_len - (degree - 2))):  # (n - (k - 2))
            knotvector.append(t)
        for t in range(degree):  # (n - (k - 2))
            knotvector.append((points_len - (degree - 2)))

        return knotvector

    # DONE
    def deboor(self, degree, controlpoints, knotvector, j, t):
        n = len(knotvector) - len(controlpoints) - 1

        if degree == 0:
            if j == len(controlpoints):
                return np.array(controlpoints[j - 1])
            if j < 0:
                return np.array(controlpoints[0])
            return np.array(controlpoints[j])

        else:
            w1 = self.calc_w(knotvector, j, n - degree + 1, t)
            w2 = self.calc_w(knotvector, j, n - degree + 1, t)

            d1 = self.deboor(degree - 1, controlpoints, knotvector, j - 1, t)
            d2 = self.deboor(degree - 1, controlpoints, knotvector, j, t)

            return (1 - w1) * d1 + w2 * d2

    def calc_w(self, knotvector, i, n, t):
        if knotvector[i] < knotvector[i + n]:
            return (t - knotvector[i]) / (knotvector[i + n] - knotvector[i])
        return 0

    # DONE
    def increase(self, param):
        print self.get_param(param)
        if param not in self.values.keys():
            return

        if param in self.valueLimits.keys():
            if self.get_param(param) >= self.valueLimits[param]["max"]():  # degree has to be at least 2
                return

        self.values[param] += 1

    # DONE
    def decrease(self, param):
        if param not in self.values.keys():
            return
        if self.values[param] < 2:  # degree has to be at least 2
            return

        if param in self.valueLimits.keys():
            if self.get_param(param) <= self.valueLimits[param]["min"]:  # degree has to be at least 2
                return

        self.values[param] -= 1

    # DONE
    def get_degree(self):
        return self.get_param(self.PARAM_DEGREE)

    # DONE
    def get_pointcount(self):
        return self.get_param(self.PARAM_POINTS)

    # DONE
    def get_param(self, key):
        return self.values.get(key, None)

    # DONE
    def set_param(self, param, val):
        if param not in self.values.keys():
            return
        self.values[param] = val


class RenderWindow:
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

        # define desire frame rate
        self.frame_rate = 100

        # make a window
        self.width, self.height = 640, 640
        self.aspect = self.width / float(self.height)
        self.window = glfw.create_window(self.width, self.height, "B-Spline-Kurve", None, None)
        if not self.window:
            glfw.terminate()
            return

        self.initGLFW()
        self.initGL()

        self.scene = Scene()

        self.shiftFlag = False
        self.exitNow = False
        self.render = False

    def initGL(self):
        glViewport(0, 0, self.width, self.height)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glMatrixMode(GL_MODELVIEW)

    def initGLFW(self):
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.onKeyAction)
        glfw.set_mouse_button_callback(self.window, self.onClick)

    def run(self):
        glfw.set_time(0.0)
        t = 0.0
        while not glfw.window_should_close(self.window) and not self.exitNow:
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

    def onClick(self, window, button, action, mods):
        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                x, y = glfw.get_cursor_pos(window)
                x = x / self.width * 2 - 1
                y = - (y / self.height * 2 - 1)

                self.scene.points.append(np.array([x, y]))
                self.scene.increase(Scene.PARAM_POINTS)

                self.scene.calc_curve()

    def onKeyAction(self, window, key, scancode, action, mods):
        degree = self.scene.get_degree()
        pointcount = self.scene.get_pointcount()

        if key == glfw.KEY_ESCAPE:
            if action == glfw.RELEASE:
                self.exitNow = True
            return
        elif key == glfw.KEY_LEFT_SHIFT or key == glfw.KEY_RIGHT_SHIFT:
            self.shiftFlag = True if action == glfw.PRESS else False
            return
        elif key == glfw.KEY_M:
            if action == glfw.RELEASE:
                return
            print "m"
            if self.shiftFlag:
                self.scene.increase(Scene.PARAM_POINTS)
                print "increase point count"
            else:
                if pointcount > len(self.scene.knotvector):
                    self.scene.set_param(Scene.PARAM_POINTS, len(self.scene.knotvector))
                    print "set point count"

                if pointcount > 2:
                    self.scene.decrease(Scene.PARAM_POINTS)
                    print "decrease point count"
            return
        elif key == glfw.KEY_K:
            if action == glfw.RELEASE:
                return
            print "k"
            # changing curve degree
            if self.shiftFlag:
                self.scene.increase(Scene.PARAM_DEGREE)
                print "increase degree"
            else:
                self.scene.decrease(Scene.PARAM_DEGREE)
                print "decrease degree"

            self.scene.calc_curve()
            return


# main() function
def main():
    print("Simple glfw B-SPLINE")
    rw = RenderWindow()
    rw.run()


# call main
if __name__ == '__main__':
    main()
