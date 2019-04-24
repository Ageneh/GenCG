import datetime
import random

from PIL import Image

from raytracer.objects import COLORS, Camera, HitPointData, ObjectAbstract, Ray, Sphere, Vector


class RayCaster:

	# TODO: implement illumination

	# TODO: implement transformation

	# TODO: implement recursive ray-casting

	# TODO: implement reflections

	# TODO: textures

	def __init__(self, resolution=200, camera=None, light=None, objects=None, maxlevel=3):
		'''
		:param resolution: can be a numeric value or collection of numeric values defining the resolution
		:param camera: the scene camera
		:param objects: a collection of all object of the scene
		'''
		self.maxlevel = maxlevel
		self.camera = camera
		self.light = light
		self.objects = objects if objects else []

		if type(resolution) in (tuple, list):
			if len(resolution) == 1:
				resolution = resolution[0], resolution[0]
		elif str(resolution).isnumeric():
			resolution = resolution, resolution
		self.imageWidth, self.imageHeight = resolution
		self.image = Image.new("RGB", (self.imageWidth, self.imageHeight))
		self.pixelWidth = self.camera.width / (self.imageWidth - 1)
		self.pixelHeight = self.camera.height / (self.imageHeight - 1)

		self.logfile = None
		self.times = []

	def add(self, other):
		if other is Camera:
			self.camera = other
		elif isinstance(other, ObjectAbstract):
			self.objects.append(other)

	def rays(self, e, f, xcomp, ycomp, raycount=1):
		if raycount == 1: return Ray(e, f + xcomp + ycomp)

		# TODO: multiple rays per pixel and average color

		rays = []
		l = 0.05

		for r in range(raycount):
			x_lambda = random.uniform(-l * self.pixelWidth, l * self.pixelWidth)
			x_lambda = Vector([x_lambda, 0, 0])

			y_lambda = random.uniform(-l * self.pixelHeight, l * self.pixelHeight)
			y_lambda = Vector([0, y_lambda, 0])

			rays.append(Ray(e, f + xcomp + x_lambda + ycomp + y_lambda))

		avg_ray = Vector(0, 0, 0)
		for r in rays:
			avg_ray = avg_ray + r

		avg_ray /= raycount
		return rays, avg_ray

	def calcRay(self, x, y):
		xcomp = self.camera.s.scale(x * self.pixelWidth - self.camera.width / 2)
		ycomp = self.camera.u.scale(y * self.pixelHeight - self.camera.height / 2)

		# return self.rays(self.camera.origin, self.camera.f, xcomp, ycomp)  # evtl . mehrere Strahlen pro Pixel
		return Ray(self.camera.origin, self.camera.f + xcomp + ycomp)  # evtl . mehrere Strahlen pro Pixel

	# TODO: multiprocessed rayscasting

	def castRays(self):
		if not self.camera:
			raise RuntimeError("Camera not defined yet.")

		self.logfile = open("./logs/log-{}.txt".format(datetime.datetime.now()), "w+", encoding="utf8")

		start = datetime.datetime.now()
		print("Casting start: {}".format(start))

		for x in range(self.imageWidth):
			self.logfile.write("x: " + str(x) + "\n")
			for y in range(self.imageHeight):
				ray = self.calcRay(x, y)
				# maxdist = self.intersect(1, ray)
				maxdist = float("inf")

				color = COLORS.BG_COLOR


				for object in self.objects:
					hitdist = object.intersectionParameter(ray)
					self.logfile.write("ray: " + str(ray) + " -> " + str(hitdist) + "\n")

					# self.logfile.write("y: " + str(y) + ": " + str(hitdist) + ", " + str(ray) + "\n")

					if hitdist:
						if 0 < hitdist < maxdist:
							maxdist = hitdist
							color = object.colorAt(ray)

					self.image.putpixel((x, y), color.value())

			self.logfile.write("\n" * 2)

		end = datetime.datetime.now()
		self.times = [start, end]
		print("Casting end: {}".format(end))
		print("Casting time: {}".format(end - start))

		self.logfile.close()

	def export(self):
		stamp = str(self.times[0])
		img_str = "./images/{}.jpg"
		self.image.save(
				img_str.format(stamp),
				"JPEG", quality=75)
		self.image.show()

	def traceRay(self, level, ray):
		hitPointData = self.intersect(level, ray)  # maxLevel = maximale Rekursions−Tiefe
		if hitPointData:
			return self.shade(level, hitPointData)
		return COLORS.BG_COLOR

	def shade(self, level, hitPointData):
		directColor = self.computeDirectLight(hitPointData)
		reflectedRay = self.computeReflectedRay(hitPointData)
		reflectColor = self.traceRay(level + 1, reflectedRay)
		# refractedRay = self.computeRefractedRay(hitPointData)
		# refractColor = self.traceRay(level+1, refractedRay)

		# return directColor + reflection * reflectedColor  # + refraction *  drefractedColor
		pass

	def computeDirectLight(self, hitPointData):
		pass

	def computeReflectedRay(self, hitPointData):
		pass

	def computeRefractedRay(self, hitPointData):
		pass

	def intersect(self, level, ray):
		if level > self.maxlevel:
			# if not intersection has been found after depth of maxlevel
			return None

		maxdist = float("inf")
		object = None

		for obj in self.objects:
			hitdist = obj.intersectionParameter(ray)
			if not hitdist: continue

			# on intersection with obj
			if 0 < hitdist < maxdist:
				maxdist = hitdist
				object = obj

		if not object:
			return None

		return HitPointData(object=object, ray=ray, distance=maxdist)


if __name__ == '__main__':
	sphere_pos = Vector(0, 20, 550)

	camera = Camera(
			origin=Vector(0, 20, -200),
			up=Vector(0, 1, 0),
			focus=Vector(0, 0, 1),
			fov=145,
			aratio=16 / 10
	)

	rc = RayCaster(resolution=100, camera=camera)
	rc.add(Sphere(sphere_pos, 1, COLORS.GREEN))

	rc.castRays()
	rc.export()
