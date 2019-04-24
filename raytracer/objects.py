from abc import ABC, abstractmethod
from math import sqrt, tan

from numpy import add, cross, divide, dot, power, subtract
from numpy import float64, int64


def isnumber(n) -> bool:
	return type(n) in (int, int64, float64, float) or str(n).isnumeric()


### OBJECTS


class Color:

	def __init__(self, r=0, g=0, b=0):
		self.rgb = r, g, b

	def __repr__(self):
		return "Color({})".format(",".join(map(repr, self.rgb)))

	def value(self):
		return self.rgb


class COLORS:
	BLACK = Color()
	BG_COLOR = BLACK
	RED = Color(r=255)
	GREEN = Color(g=255)
	BLUE = Color(b=255)
	WHITE = Color(r=255, g=255, b=255)


class Vector:

	def __init__(self, x, *args):
		def check(n):
			return n if isnumber(n) else 0

		if isnumber(x):
			y, z = args[:2]
		else:
			x, y, z = x

		self.x = check(x)
		self.y = check(y)
		self.z = check(z)

	def __repr__(self):
		return "Point({}, {}, {})".format(
				repr(self.x),
				repr(self.y),
				repr(self.z)
		)

	def __str__(self):
		return "P{}".format(repr(self.vector()))

	def __mul__(self, v):
		if iscoll(v):
			v = Vector(v[0], v[1], v[2])
		elif isnumber(v):
			# multiply vector by scalar
			return Vector(dot(self.vector(), v))

		# multiply vector by vector v
		return self.dot(v)

	def __truediv__(self, v):
		if iscoll(v):
			v = Vector(v[0], v[1], v[2])
		elif isnumber(v):
			return Vector(divide(self.vector(), v))

		return divide(self.vector(), v.vector())

	def __add__(self, v):
		if iscoll(v):
			v = Vector(v[0], v[1], v[2])
		return Vector(add(self.vector(), v.vector()))

	def __sub__(self, v):
		if iscoll(v):
			v = Vector(v[0], v[1], v[2])
		return Vector(subtract(self.vector(), v.vector()))

	def __pow__(self, exponent, modulo=None):
		return Vector(power(self.vector(), exponent))

	def vector(self):
		'''
		:return: a tuple made up of x, y and z coordinates.
		-> (x, y, z)
		'''
		return self.x, self.y, self.z

	def scale(self, v):
		'''
		:param v: a scalar used to scale the vector
		:return: a new scaled vector
		'''
		if not isnumber(v):
			return None
		return self.__mul__(v)

	def dot(self, v):
		'''
		:param v: is a Vector object
		:return: the scalar product of two Vectors => self • v
		'''
		if type(v) is not Vector:
			return None
		return dot(self.vector(), v.vector())

	def cross(self, v):
		if iscoll(v):
			v = Vector(v)
		return Vector(cross(self.vector(), v.vector()))

	def length(self) -> float:
		'''
		:return: the length of a Vector
		Calculates the length as follows:
		-> sqrt(<v,v>) = sqrt(sum(x^2 + y^2 + z^2))
		'''
		return sqrt(self * self)

	def vectortopoint(self, p):
		return p - self.vector()

	def normalized(self):
		'''
		:return: the normalized Vector by dividing the Vector by its length
		'''
		return self / self.length()


class ObjectAbstract(ABC):

	def __init__(self, color=COLORS.WHITE):
		# self.vectorToPoint = lambda a, b: b - a
		self.color = color
		pass

	@abstractmethod
	def intersectionParameter(self, ray):
		"""
		:param ray: a Ray which is tested for intersecting the object
		:return:
		"""
		pass

	@abstractmethod
	def normalAt(self, p) -> Vector:
		'''
		:param p: any point from which the normal of the Object is calculated
		:return: a new normal vector object at the given point
		'''
		pass

	def colorAt(self, ray):
		# TODO: calculate shaded color
		return self.color


class Ray:

	def __init__(self, origin, direction):
		def check(v):
			if iscoll(v):
				return Vector(v)
			else:
				return v

		self.origin = check(origin)
		self.direction = check(direction)

	def __repr__(self):
		return "Ray({}, {})".format(repr(self.origin), repr(self.direction))

	def __str__(self):
		return "R({}, {})".format(str(self.origin), str(self.direction))

	def pointAtParameter(self, t) -> Vector:
		if not isnumber(t):
			return None
		return self.origin + self.direction * t


class Light(Vector):

	def __init__(self, x, *args, intensity=1.0, color=COLORS.WHITE):
		super().__init__(x, *args)
		self.intensity = intensity
		self.color = color


class Sphere(ObjectAbstract):

	def __init__(self, center, radius, color):
		super().__init__(color=color)
		self.center = center  # point
		self.radius = radius  # scalar

	def __repr__(self):
		return "Sphere({}, {})".format(repr(self.center), self.radius)

	def intersectionParameter(self, ray):
		"""
		:return:
		"""
		co = self.center - ray.origin
		v = co.dot(ray.direction)
		discriminant = v ** 2 - co.dot(co) + self.radius ** 2

		if discriminant < 0:
			return None
		else:
			return v - sqrt(discriminant)

	def normalAt(self, p) -> Vector:
		cp = p - self.center
		# return cp / cp.length()
		return cp.normalized()


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

	def normalAt(self, p) -> Vector:
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
		return Vector(cross(self.u, self.v)).normalized()


class Camera:

	def __init__(self, origin=Vector(0, 0, 0), up=Vector(0, 1, 0), focus=Vector(0, 0, 1), fov=45, aratio=10 / 16):
		self.origin = origin
		self.fov = fov
		self.up = up
		self.focus = focus

		self.alpha = self.fov / 2
		self.height = 2 * tan(self.alpha)
		self.aratio = aratio
		self.width = aratio * self.height

		self.f = (focus - self.origin).normalized()
		self.s = self.f.cross(up).normalized()
		self.u = self.s.cross(self.f)

	def __repr__(self):
		# return "Camera({})".format(", ".join(map(repr, self.__args)))
		return "Camera(origin={}, up={}, focus={}, fov={}, aratio={})".format(
				self.origin, self.up, self.up, self.focus, self.fov, self.aratio
		)

	def __str__(self):
		# return "Cam({})".format(", ".join(map(str, self.__args)))
		return "Cam(e={}, up={}, f={}, fov={}, rat={})".format(
				self.origin, self.up, self.up, self.focus, self.fov, self.aratio
		)


class HitPointData:

	def __init__(self, ray=None, object=None, distance=None):
		self.ray = ray
		self.object = object
		self.distance = distance


#### HELPERS


def topoint(v) -> Vector:
	if iscoll(v):
		return Vector(v)
	else:
		return v


def iscoll(e) -> bool:
	return type(e) in (tuple, list)
