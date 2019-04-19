from abc import ABC, abstractmethod
from math import sqrt, tan

from numpy import add, cross, divide, dot, subtract
from numpy import float64, int64


def toPoint(v):
	if type(v) in (tuple, list):
		return Point(v)
	else:
		return v

def isNumber(n):
	return type(n) in (int, int64, float64, float) or str(n).isnumeric()


### OBJECTS


class ObjectAbstract(ABC):

	def __init__(self):
		self.vectorToPoint = lambda a, b: b - a

	@abstractmethod
	def intersectionParameter(self, ray):
		pass

	@abstractmethod
	def normalAt(self, p):
		pass


class Ray:

	def __init__(self, origin, direction):
		def check(v):
			if type(v) in (tuple, list):
				return Point(v)
			else:
				return v

		self.origin = check(origin)
		self.direction = check(direction)

	def __repr__(self):
		return "Ray({}, {})".format(repr(self.origin), repr(self.direction))

	def __str__(self):
		return

	def pointAtParameter(self, t):
		if not str(t).isnumeric(): return None
		return self.origin + self.direction * t


class Sphere(ObjectAbstract):

	def __init__(self, center, radius):
		super().__init__()
		self.center = center  # point
		self.radius = radius  # scalar

	def __repr__(self):
		return "Sphere({}, {})".format(repr(self.center), self.radius)

	def intersectionParameter(self, ray):
		co = self.center - ray.origin
		v = co.dot(ray.direction)
		discriminant = v * v - co.dot(co) + self.radius * self.radius

		if discriminant < 0:
			return None
		else:
			return v - sqrt(discriminant)

	def normalAt(self, p):
		return self.vectorToPoint(self.center, p).normalized()


class Plane(ObjectAbstract):

	def __init__(self, point, normal):
		super().__init__()
		self.point = point  # point
		self.normal = normal.normalized()  # vector

	def __repr__(self):
		return "Plane({}, {})".format(repr(self.point), repr(self.normal))

	def intersectionParameter(self, ray):
		op = ray.origin - self.point
		a = op.dot(self.normal)
		b = ray.direction.dot(self.normal)
		if b:
			return -a / b
		else:
			return None

	def normalAt(self, p):
		return self.normal


class Triangle(ObjectAbstract):

	def __init__(self, a, b, c):
		super().__init__()
		self.a = a  # point
		self.b = b  # point
		self.c = c  # point
		self.u = self.b - self.a  # direction vector
		self.v = self.c - self.a  # direction vector

	def __repr__(self):
		return "Triangle({}, {}, {})".format(repr(self.a), repr(self.b), repr(self.c))

	def intersectionParameter(self, ray):
		w = ray.origin
		dv = ray.direction.cross(self.v)
		dvu = dv.dot(self.u)

		if dvu == 0.0:
			return 0

		wu = w.cross(self.u)
		r = dv.dot(w) / dvu
		s = wu.dot(ray.direction) / dvu
		if 0 <= r <= 1 and 0 <= s <= 1 and r + s <= 1:
			return wu.dot(self.v) / dvu
		else:
			return None

	def normalAt(self, p):
		return Point(cross(self.u, self.v)).normalized()


class Point:

	def __init__(self, x, *args):
		def check(n):
			return n if isNumber(n) else 0

		if isNumber(x):
			y, z = args[:2]
		else:
			x, y, z = x

		self.x = check(x)
		self.y = check(y)
		self.z = check(z)

	def vector(self):
		return self.x, self.y, self.z

	def scale(self, v):
		return

	def __repr__(self):
		return "Point({}, {}, {})".format(
				repr(self.x),
				repr(self.y),
				repr(self.z)
		)

	def __str__(self):
		return "P{}".format(repr(self.vector()))

	def __mul__(self, v):
		if type(v) in (tuple, list):
			v = Point(v[0], v[1], v[2])
		elif type(v) in (int, float):
			# multiply vector by scalar
			return Point(dot(self.vector(), v))

		# multiply vector by vector v
		return self.dot(v)

	def __truediv__(self, v):
		if type(v) in (tuple, list):
			v = Point(v[0], v[1], v[2])
		elif isNumber(v):
			return Point(divide(self.vector(), v))

		return divide(self.vector(), v.vector())

	def __add__(self, v):
		if type(v) in (tuple, list):
			v = Point(v[0], v[1], v[2])
		return Point(add(self.vector(), v.vector()))

	def __sub__(self, v):
		if type(v) in (tuple, list):
			v = Point(v[0], v[1], v[2])
		return Point(subtract(self.vector(), v.vector()))

	def dot(self, v):
		if type(v) is not Point:
			return None
		return dot(self.vector(), v.vector())

	def length(self) -> float:
		return sqrt(self * self)

	def normalized(self):
		return self / self.length()


class Camera:

	def __init__(self, position, fov, height, aratio):
		self.position = toPoint(position)
		self.fov = fov
		self.alpha = self.fov / 2
		self.height = 2 * tan(self.alpha)
		self.aratio = aratio
		self.width = aratio * height

	def __repr__(self):
		return "Camera({}, {}, {}, {})".format(
				self.position, self.fov,
				self.height, self.aratio
		)
