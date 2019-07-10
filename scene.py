from OpenGL.GL import *
from OpenGL.arrays import vbo
from numpy import linspace, array

MIN = "min"
MAX = "max"

RANGE = 10  # pixel range


class Scene:
    PARAM_DEGREE = "degree"
    PARAM_POINTS = "pointCount"

    # DONE
    def __init__(self, w, h):
        self.valueLimits = {
            Scene.PARAM_DEGREE: {
                MIN: 1,
                MAX: lambda: len(self.points),
            },
            Scene.PARAM_POINTS: {
                MIN: 1,
                MAX: lambda: 50,
            },
        }
        self.values = {
            Scene.PARAM_DEGREE: 3,
            Scene.PARAM_POINTS: 2,
        }
        self.points = []
        self.spline_points = []
        self.knot_vector = []
        self.width, self.height = w, h
        self.reset_errythang()

    # DONE
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)

        myVbo = vbo.VBO(array(self.points, 'f'))
        myVbo.bind()

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, myVbo)
        glLineWidth(1.)
        glColor([0.7, 0.7, 0.7])
        glPointSize(5.0)
        glDrawArrays(GL_POINTS, 0, len(self.points))

        if len(self.points) > 1:
            glDrawArrays(GL_LINE_STRIP, 0, len(self.points))

        if len(self.points) >= self.get_param(self.PARAM_DEGREE):
            spline = vbo.VBO(array(self.spline_points, 'f'))
            spline.bind()

            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(2, GL_FLOAT, 0, spline)
            glLineWidth(6.)
            glColor([.0, .0, 1.0])
            glDrawArrays(GL_LINE_STRIP, 0, len(self.spline_points))
            spline.unbind()

        myVbo.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)

        glFlush()

    # DONE
    def calc_curve(self):
        if self.get_degree() > len(self.points):
            # hide spline/don't calculate spline while not enough points have been set
            return

        degree = self.get_degree()

        self.spline_points = []
        self.knot_vector = self.calc_knot_vector()

        limit_in_knot_vector = len(self.knot_vector) - degree

        for i in range(degree - 1, limit_in_knot_vector):
            if self.knot_vector[i] == self.knot_vector[i + 1]:
                # avoid going past idx of last val (see calc_knot_vector)
                continue
            for t in linspace(self.knot_vector[i], self.knot_vector[i + 1], self.get_pointcount()):
                self.spline_points.append(
                    self.deboor(degree, self.points, self.knot_vector, i, t)
                )

    # DONE
    def calc_knot_vector(self):
        # n:=degree=4, k:=len(points)=5
        # => [ [0]*d, 1,2, [n-(2k-1)]*d ]
        # => [ 0, 0, 0, 0, 1, 2, 3, 3, 3, 3 ]
        # =>            |        |
        # => idx:      n-1    len()-n
        # S.284
        degree = self.get_degree()
        points_len = len(self.points)

        _d = points_len - (degree - 2)

        knot_vector = [0] * degree
        knot_vector += [idx for idx in range(1, _d)]
        knot_vector += [_d] * degree

        print("knot_vector: {}".format(str(knot_vector)))

        return knot_vector

    def deboor(self, degree, control_points, knot_vector, i, t):
        # d:=degree=4, p:=len(points)=5
        # => len(knot) => (d+p)+1=4+5+1=10
        # => knot_idx_end=len(knot) - len(points)-1
        # S.
        # n = len(knot_vector) - len(controlpoints) - 1

        if degree <= 0:
            # if i is out of bounds
            if i == len(control_points):
                return array(control_points[i - 1])
            if i < 0:
                # avoid going past last layer
                return array(control_points[0])
            return array(control_points[i])

        alpha = self.calc_alpha(knot_vector, degree, i, t)

        b1 = self.deboor(degree - 1, control_points, knot_vector, i - 1, t)
        b2 = self.deboor(degree - 1, control_points, knot_vector, i, t)

        return (1 - alpha) * b1 + alpha * b2

    # DONE
    def calc_alpha(self, knot_vector, degree, i, t):
        diff = len(knot_vector) - len(self.points) - degree
        if knot_vector[i] < knot_vector[i + diff]:
            return (t - knot_vector[i]) / (knot_vector[i + diff] - knot_vector[i])
        return 0

    # DONE
    def increase(self, param):
        if param not in self.values.keys():
            return
        if param in self.valueLimits.keys():
            if self.get_param(param) >= self.valueLimits[param][MAX]():  # degree has to be at least 2
                return
        self.values[param] += 1
        self.calc_curve()
        print("{} increased to: {}".format(param, str(self.values[param])))

    # DONE
    def decrease(self, param):
        if param not in self.values.keys():
            return
        # if self.values[param] < 2:  # degree has to be at least 2
        #     return
        if param in self.valueLimits.keys():
            if self.get_param(param) <= self.valueLimits[param][MIN]:  # degree has to be at least 2
                return
        self.values[param] -= 1
        self.calc_curve()
        print("{} decreased to: {}".format(param, str(self.values[param])))

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
        self.calc_curve()

    # DONE
    def add_point(self, point):
        self.points.append(point)

        # # ========================================= # #
        # # used to increase point count in point add # #
        # # -> seems a bit better                     # #
        # self.increase(Scene.PARAM_POINTS)           # #
        # # ========================================= # #

        self.calc_curve()
        print("point count: {}".format(str(len(self.points))))
        print("max degree: {}".format(str(self.valueLimits[Scene.PARAM_DEGREE][MAX]())))

    # DONE
    def point_in_region(self, x, y):
        def in_range(val, start, end):
            return start <= val <= end

        _points_in_range = []
        points = self.points
        dist_x = RANGE / float(self.width)
        dist_y = RANGE / float(self.height)

        for idx, p in enumerate(points):
            if in_range(p[0], x - dist_x, x + dist_x) and in_range(p[1], y - dist_y, y + dist_y):
                _points_in_range.append(idx)

        return _points_in_range

    def _recalc_degree(self):
        max = self.valueLimits[Scene.PARAM_DEGREE][MAX]()
        if self.get_degree() > len(self.points):
            self.set_param(Scene.PARAM_DEGREE, max)

    # DONE
    def remove_point(self, x, y):
        points = self.points

        rm_point = self.point_in_region(x, y)
        if not rm_point:
            return

        points.remove(points[rm_point[0]])
        self.points = points
        self._recalc_degree()
        self.calc_curve()

    # DONE
    def reset_errythang(self):
        self.points = []
        self.spline_points = []
        self.knot_vector = []
        print "values: ", self.values
