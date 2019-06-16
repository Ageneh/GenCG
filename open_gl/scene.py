import numpy as np
from OpenGL.GL import *
from OpenGL.arrays import vbo


class Scene:
    """ OpenGL 2D scene class """

    # initialization
    def __init__(self, width, height):
        # time
        self.t = 0
        self.showVector = True
        self.point = np.array([0, 0])
        self.vector = np.array([10, 10])
        self.point_size = 2
        self.width = width
        self.height = height
        self.angle = 0.
        self.axis = np.array([0., 1., 0.])
        self.actOri = 1.
        self.color = (.5, .5, .5)
        glPointSize(self.point_size)
        glLineWidth(self.point_size)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)

    # step
    def step(self):
        # move point
        self.point = self.point + 0.1 * self.vector

        # check borders
        if self.point[0] < -self.width / 2:  # point hits left border
            # mirror at n = [1,0]
            n = np.array([1, 0])
            self.vector = self.mirror(self.vector, n)
        elif self.point[0] > self.width / 2:  # point hits right border
            # mirrot at n = [-1,0]
            n = np.array([-1, 0])
            self.vector = self.mirror(self.vector, n)
        elif self.point[1] < -self.height / 2:  # point hits upper border
            # mirrot at n = [0,1]
            n = np.array([0, 1])
            self.vector = self.mirror(self.vector, n)
        elif self.point[1] > self.height / 2:  # point hits lower border
            # mirrot at n = [0,-1]
            n = np.array([0, -1])
            self.vector = self.mirror(self.vector, n)

    # mirror a vector v at plane with normal n
    def mirror(self, v, n):
        # normalize n
        normN = n / np.linalg.norm(n)
        # project negative v on n
        l = np.dot(-v, n)
        # mirror v
        mv = v + 2 * l * n
        return mv

    def draw(self, vbo_data):
        glClear(GL_COLOR_BUFFER_BIT)
        r, g, b = self.color
        glColor(r, g, b)  # Color of object

        # glColor(0.6, 0.0, 0.8)

        my_vbo = vbo.VBO(np.array(vbo_data, 'f'))
        my_vbo.bind()
        glMultMatrixf(self.actOri * self.rotate(self.angle, self.axis))
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glVertexPointer(3, GL_FLOAT, 24, my_vbo)
        glNormalPointer(GL_FLOAT, 24, my_vbo + 12)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDrawArrays(GL_TRIANGLES, 0, len(vbo_data))
        my_vbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glFlush()

    # render
    def render(self, vbo_data):
        self.draw(vbo_data)

    def rotate(self, angle, axis):
        c, mc = np.cos(angle), 1 - np.cos(angle)
        s = np.sin(angle)
        l = np.sqrt(np.dot(np.array(axis), np.array(axis)))
        x, y, z = np.array(axis) / l
        r = np.array(
            [
                [x * x * mc + c, x * y * mc - z * s, x * z * mc + y * s, 0],
                [x * y * mc + z * s, y * y * mc + c, y * z * mc - x * s, 0],
                [x * z * mc - y * s, y * z * mc + x * s, z * z * mc + c, 0],
                [0, 0, 0, 1]
            ]
        )
        return r.transpose()

    def scale(self, scale):
        scalef = 1 + scale / 100.
        glScale(scalef, scalef, scalef)

    def translate(self, x, y):
        glTranslate(x, y, 0)
