from OpenGL.GL import *
from OpenGL.arrays.vbo import VBO
from numpy import cos, array, sin, sqrt, dot


class Scene:
    """ OpenGL 2D scene class """

    # DONE
    def __init__(self, width, height):
        self.point_size = 2
        self.width = width
        self.height = height
        self.angle = 0.
        self.axis = array([0., 1., 0.])
        self.color = (.5, .5, .5)
        self.hasShadow = False
        self.light = (10, 10, 10)
        self.p = [
            1., 0, 0, 0,
            0, 1., 0, -1. / self.light[1],
            0, 0, 1., 0,
            0, 0, 0, 0
        ]
        self.rotationStep = 1.0
        self.rotationAngle = 0.0
        self.initGL()

    # DONE
    def initGL(self):
        glPointSize(self.point_size)
        glLineWidth(self.point_size)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)

    # DONE
    def _drawshadow(self, vbo_data):
        glPushMatrix()
        glTranslatef(self.light[0], self.light[1], self.light[2])
        glMultMatrixf(self.p)
        tr_x, tr_y, tr_z = list(array(self.light) * -1)
        glTranslatef(tr_x, tr_y, tr_z)

        self._drawobject(vbo_data, shadow=True)  # draw object as shadow

        glPopMatrix()

    # DONE
    def _drawobject(self, vbo, shadow=False):
        my_vbo = VBO(array(vbo, 'f'))
        my_vbo.bind()

        glMultMatrixf(self.rotationStep * self.rotate())
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glVertexPointer(3, GL_FLOAT, 24, my_vbo)
        glNormalPointer(GL_FLOAT, 24, my_vbo + 12)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor3fv([0., 0., 0.]) if shadow else glColor3fv(self.color)
        glDrawArrays(GL_TRIANGLES, 0, len(vbo))

        my_vbo.unbind()

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glFlush()

    # DONE
    def _draw(self, vbo):
        self._drawobject(vbo)
        if self.hasShadow:
            self._drawshadow(vbo)

    # render
    # DONE
    def render(self, vbo):
        self._draw(vbo)

    # DONE
    def rotate(self):
        c, mc = cos(self.angle), 1 - cos(self.angle)
        s = sin(self.angle)
        l = sqrt(dot(array(self.axis), array(self.axis)))
        x, y, z = array(self.axis) / l
        r = array(
            [
                [x * x * mc + c, x * y * mc - z * s, x * z * mc + y * s, 0],
                [x * y * mc + z * s, y * y * mc + c, y * z * mc - x * s, 0],
                [x * z * mc - y * s, y * z * mc + x * s, z * z * mc + c, 0],
                [0, 0, 0, 1]
            ]
        )
        return r.transpose()

    # DONE
    def scale(self, scale):
        scalef = 1 + scale / 100.
        glScale(scalef, scalef, scalef)

    # DONE
    def translate(self, x, y):
        glTranslate(x, y, 0)
