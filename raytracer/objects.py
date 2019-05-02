from abc import abstractmethod

from numpy import abs, add, cross, divide, dot, multiply, sqrt, subtract, sum, tan
from numpy import array, float64, ndarray
from numpy.linalg import norm


class HitPointData:

	# magic

	def __init__(self, ray=None, object=None, distance=None):
		self.ray = ray
		self.object = object
		self.distance = distance
		self.intersection = ray.point_at(self.distance)
		self.normal = object.normalat(self.intersection)
		self.reflected = ray.direction.reflect(self.normal).normalized()

	def __iter__(self):
		for d in self.data(): yield d
		raise StopIteration

	# behaviour

	def data(self) -> tuple:
		return self.ray, self.object, self.distance, self.intersection, self.normal, self.reflected


class Color:
	_MIN, _MAX = 0, 255
	_d = {"r": 0, "g": 1, "b": 2, }


	def smaller(self, x) -> bool:
		return x < self._MIN

	def bigger(self, x) -> bool:
		return x > self._MAX

	# magic

	def __add__(self, other):
		r, g, b = self.rgb + other.rgb
		return Color(r, g, b)

	__radd__ = __add__

	def __mul__(self, other):
		if isinstance(other, (int, float64, float)):
			r, g, b = self.rgb * other
		else:
			r, g, b = self.rgb * other.rgb
		return Color(r, g, b)

	__rmul__ = __mul__

	def __sub__(self, other):
		r, g, b = self.rgb - other.rgb
		return Color(r, g, b)

	__rsub__ = __sub__

	def __iter__(self):
		for v in self.rgb: yield v
		raise StopIteration

	def __getitem__(self, item: (int, str)):
		if isinstance(item, str):
			if item in self._d.keys():
				return self.rgb[self._d[item]]
		return self.rgb[item]

	def __str__(self):
		return "Color{}".format(str(tuple(self.rgb)))

	__repr__ = __str__

	def __init__(self, r=175, g=175, b=175):
		self.rgb = self.check(r, g, b)

	# behaviour

	def check(self, r=125, g=125, b=125):
		rgb = []
		for v in (r, g, b):
			if self.smaller(v):
				v = self._MIN
			elif self.bigger(v):
				v = self._MAX
			rgb.append(int(v))
		return array(list(rgb))

	def items(self):
		return tuple(self.rgb)

	torgb = items


class isMaterial:

	@abstractmethod
	def getcolor(self, p=None) -> Color:
		pass

	@abstractmethod
	def calccolor(self, c_in=None, shaded=False, phi=.0, theta=.0, intensity=1) -> Color:
		pass


class Material(isMaterial):

	# magic

	def __init__(self, color: Color, ambLvl=0.3,
				 diffLvl=0.5, specLvl=0.5, surface=0):
		self.color = color
		self.setlevels(ambLvl=ambLvl, diffLvl=diffLvl, specLvl=specLvl)

	# behaviour

	def setlevels(self, ambLvl=0.3, diffLvl=0.5, specLvl=0.5, surface=0):
		self.ambLvl = ambLvl
		self.diffLvl = diffLvl
		self.specLvl = specLvl
		self.surface = surface
		return self

	def getcolor(self, p=None):
		return self.color

	def calcshaded(self, c_in: Color):
		# return self.color + c_in * self.diffLvl
		return self.color * self.diffLvl

	def calccolor(self, c_in=None, phi=.0, theta=.0, intensity=1, p=None, shaded=False) -> Color:
		if shaded:
			return self.calcshaded(c_in)

		res = self.color * intensity * self.ambLvl
		res = res + self.color * intensity * self.diffLvl * phi
		res = res + self.color * intensity * self.specLvl * (theta ** self.surface)

		return res


class Vector:

	# magic

	def __getitem__(self, item: (int, slice)):
		return self.xyz[item]

	def __iter__(self):
		for i in self.xyz: yield i
		raise StopIteration

	def __add__(self, other):
		return Vector(add(self.xyz, other.xyz))

	__radd__ = __add__

	def __sub__(self, other):
		return Vector(subtract(self.xyz, other.xyz))

	__rsub__ = __sub__

	def __mul__(self, other):
		if isinstance(other, (float, float64, int)):
			return Vector(multiply(self.xyz, other))
		return Vector(multiply(self.xyz, other.xyz))

	__rmul__ = __mul__

	def __truediv__(self, other):
		if isinstance(other, (float, float64, int)):
			return Vector(divide(self.xyz, other))
		return Vector(divide(self.xyz, other.xyz))

	__rdiv__ = __truediv__

	def __int__(self):
		return self.dot(self)

	def __str__(self):
		return "Vector({})".format(str(self.xyz))

	__repr__ = __str__

	def __init__(self, x, y=0, z=0):
		if isinstance(x, Vector):
			x, y, z = x.items()
		elif type(x) in (tuple, list, array, ndarray):
			x, y, z = x
		self.xyz = array([x, y, z])

	# behaviour

	scale = __mul__  # s must be a scalar/int/float

	def items(self):
		return self.xyz

	def dot(self, other):
		return dot(self.xyz, other.xyz)

	def cross(self, other):
		return Vector(cross(self.xyz, other.xyz))

	def length(self):
		return norm(self.xyz)

	def normalized(self):
		return self / self.length()

	def reflect(self, axis):
		axis = axis.normalized()
		return self - multiply(self.dot(axis), 2 * axis)  # (S48)

	def vectorto(self, b):
		# a vector from self (point a) to point b
		return b - self


class isTexture:

	@abstractmethod
	def getcolor(self, p=None) -> Color:
		pass

	@abstractmethod
	def calccolor(self, p: Vector, phi=.0, theta=.0, intensity=1, shaded=False) -> Color:
		pass


class CheckerBoard(isTexture):

	def __init__(self, first: Material, second: Material, size=3,
				 ambLvl=0.3, diffLvl=0.5, specLvl=0.5, surface=0, c_in=None):
		self.firstMat = first
		self.firstMat.setlevels(ambLvl, diffLvl, specLvl)
		self.secondMat = second
		self.secondMat.setlevels(ambLvl, diffLvl, specLvl)
		self.size = size
		self.ambLvl = ambLvl
		self.diffLvl = diffLvl
		self.specLvl = specLvl
		self.surface = surface

	def getmat(self, p=None) -> Material:
		v = p.scale(1.0 / self.size)

		material = self.firstMat
		if sum(list(map(lambda x: abs(int(x + .5)), v.xyz))) % 2:
			material = self.secondMat
		return material


	def calccolor(self, p: Vector, phi=.0, theta=.0, intensity=1, shaded=False, c_in=None):
		return self.getmat(p).calccolor(phi=phi, theta=theta, intensity=intensity, shaded=shaded, c_in=c_in)


class Ray:

	# magic

	def __init__(self, origin: Vector, direction: Vector):
		self.origin = origin
		self.direction = direction.normalized()

	def __str__(self):
		return "Ray({}, {})".format(str(self.origin), str(self.direction))

	__repr__ = __str__

	# behaviour

	def point_at(self, t: (int, float, float64)) -> Vector:
		return self.origin + self.direction * t


class Light:

	# magic

	def __str__(self):
		return "Light({}, {}, {})".format(
				str(self.origin),
				str(self.color),
				str(self.intensity), )

	def __init__(self, origin: Vector, color: Color, intensity=1.0):
		self.origin = origin
		self.color = color
		self.intensity = intensity


class Camera:

	# magic

	def __init__(self, origin: Vector, up: Vector, focus: Vector, fov: (int, float, float64), res=(200, 200)):
		self.origin = origin
		self.up = -1 * up
		self.focus = focus
		self.fov = fov

		resW, resH = res
		self.alpha = self.fov / 2
		self.height = 2 * tan(self.alpha)
		self.aratio = resH / resW
		self.width = self.aratio * self.height

		self.f = self.origin.vectorto(self.focus).normalized()
		self.s = self.f.cross(up).normalized()
		self.u = self.s.cross(self.f)

	def __str__(self):
		return "Camera({})".format(", ".join([
			str(self.origin), str(self.up),
			str(self.focus), str(self.fov)
		]))

	__repr__ = __str__


# RENDER OBJECTS START

class Sphere:

	# magic

	def __repr__(self):
		return "Sphere({}, {})".format(repr(self.center), self.radius)

	__str__ = __repr__

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

	def __hash__(self):
		return hash((self.items(), self.material))

	def __init__(self, center: Vector, radius: (int, float, float64), material: Material):
		self.center = center  # point
		self.radius = radius  # radius
		self.material = material  # scalar

	# behaviour

	# DONE
	def intersectionparameter(self, ray: Ray) -> float:
		"""
		:return: discriminant
		"""
		co = self.center - ray.origin
		v = co.dot(ray.direction)
		discriminant = v * v - co.dot(co) + self.radius * self.radius

		if discriminant < 0:
			return None
		else:
			return v - sqrt(discriminant)

	def items(self):
		return self.center, self.radius

	def normalat(self, p: Vector) -> Vector:
		return self.center.vectorto(p).normalized()


class Plane:

	# magic

	def __repr__(self):
		return "Plane({}, {})".format(repr(self.origin), repr(self.normal))

	__str__ = __repr__

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

	def __hash__(self):
		return hash((self.items(), self.material))

	def __init__(self, origin: Vector, normal: Vector, material: Color):
		self.origin = origin  # point
		self.normal = normal.normalized()  # vector
		self.material = material

	# behaviour

	def intersectionparameter(self, ray: Ray) -> float:
		op = ray.origin - self.origin
		a = op.dot(self.normal)
		b = ray.direction.dot(self.normal)
		if b:
			return -a / b
		else:
			return None

	def items(self):
		return self.origin, self.normal

	def normalat(self, p=None) -> Vector:
		return self.normal


class Triangle:

	# magic

	def __repr__(self):
		return "Triangle({}, {}, {})".format(repr(self.a), repr(self.b), repr(self.c))

	__str__ = __repr__

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()

	def __hash__(self):
		return hash((self.items(), self.material))

	def __init__(self, a: Vector, b: Vector, c: Vector, material: Color):
		self.material = material
		self.a = a  # point
		self.b = b  # point
		self.c = c  # point
		self.u = self.b - self.a  # direction vector
		self.v = self.c - self.a  # direction vector

	# behaviour

	def intersectionparameter(self, ray) -> float:
		w = ray.origin - self.a
		dv = ray.direction.cross(self.v)
		dvu = dv.dot(self.u)

		if dvu == 0.0:
			return None

		wu = w.cross(self.u)
		r = dv.dot(w) / dvu
		s = wu.dot(ray.direction) / dvu
		if 0 <= r <= 1 and 0 <= s <= 1 and r + s <= 1:
			return wu.dot(self.v) / dvu
		else:
			return None

	def items(self):
		return self.a, self.b, self.c

	def normalat(self, p=None) -> Vector:
		return Vector(self.u.cross(self.v).normalized())

# RENDER OBJECTS END


if __name__ == '__main__':
	v1 = Vector(2, 3, 4)
	v2 = Vector(2, 5, 2)

	print(v1, v2)
	print(v1 * v2)
	print(v1.dot(v2))

	r = Ray(v1, Vector(1, 1, 0))
	print(r)
	print(r.point_at(5))
	print(v1.vectorto(v2))

	col1 = Color(2, 5, 73)
	col2 = Color(200, 100, 73)

	print(col2 + col2)

	arr = array([2, 3, 4])
	arr1 = array([2, 3, 4])
	print(dot(arr, arr1))
	print(arr - arr1)
