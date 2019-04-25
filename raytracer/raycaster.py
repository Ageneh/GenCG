import datetime

from PIL import Image

from raytracer.objects import COLORS, Camera, HitPointData, ObjectAbstract, Ray, Sphere, Vector


# ################################
#
# TODO:ALLE OPERATIONEN MIT NUMPY
#
# ################################


class RayCaster:

	# TODO: implement illumination

	# TODO: implement transformation

	# TODO: implement recursive ray-casting

	# TODO: implement reflections

	# TODO: textures

	def __init__(self, resolution=200, camera=None, light=None, objects=None, maxlevel=3, multi=False):
		'''
		:param multi: None/False -> singlethreaded; numeric value -> number of divisions
		:param resolution: can be a numeric value or collection of numeric values defining the resolution
		:param camera: the scene camera
		:param objects: a collection of all object of the scene
		'''

		if multi and type(multi) is int and multi > 2:
			self.multi = multi - 1
		else:
			self.multi = False

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

	def calcRay(self, x, y):

		# def rays(e, f, xcomp, ycomp, raycount=1):
		# 	if raycount == 1: return Ray(e, f + xcomp + ycomp)
		#
		# 	# TODO: multiple rays per pixel and average color
		#
		# 	rays = []
		# 	l = 0.05
		#
		# 	for r in range(raycount):
		# 		x_lambda = random.uniform(-l * self.pixelWidth, l * self.pixelWidth)
		# 		x_lambda = Vector([x_lambda, 0, 0])
		#
		# 		y_lambda = random.uniform(-l * self.pixelHeight, l * self.pixelHeight)
		# 		y_lambda = Vector([0, y_lambda, 0])
		#
		# 		rays.append(Ray(e, f + xcomp + x_lambda + ycomp + y_lambda))
		#
		# 	avg_ray = Vector(0, 0, 0)
		# 	for r in rays:
		# 		avg_ray = avg_ray + r
		#
		# 	avg_ray /= raycount
		# 	return rays, avg_ray

		xcomp = self.camera.s.scale(x * self.pixelWidth - self.camera.width / 2)
		ycomp = self.camera.u.scale(y * self.pixelHeight - self.camera.height / 2)

		return Ray(self.camera.origin, self.camera.f + xcomp + ycomp)


	# TODO: multiprocessed rayscasting

	def castRays(self):
		if not self.camera:
			raise RuntimeError("Camera not defined yet.")

		start = datetime.datetime.now()

		if self.multi:
			self.multithreaded()
		else:
			for x in range(self.imageWidth):
				for y in range(self.imageHeight):
					ray = self.calcRay(x, y)
					maxdist = float("inf")

					color = COLORS.BG_COLOR

					for object in self.objects:
						hitdist = object.intersectionParameter(ray)

						if hitdist:
							if hitdist < maxdist:
								maxdist = hitdist
								color = object.colorAt(ray)

						self.image.putpixel((x, y), color.value())

		end = datetime.datetime.now()
		self.times = [start, end]
		print("Casting end: {}".format(end))
		print("Casting time: {}".format(end - start))


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

	def multiCalc(self, ranges):
		colors = []

		x_range, y_range = ranges

		for x in range(x_range[0], x_range[1]):

			for y in range(y_range[0], y_range[1]):
				print("multi: " + str(ranges) + "\t=>\t" + str(x) + "-" + str(y))

				ray = self.calcRay(x, y)
				maxdist = float("inf")

				color = COLORS.BG_COLOR

				for object in self.objects:
					hitdist = object.intersectionParameter(ray)

					if hitdist:
						if 0 < hitdist < maxdist:
							maxdist = hitdist
							color = object.colorAt(ray)

				colors.append(((x, y), color.value()))  # (x, y), RGB

		return colors

	def multithreaded(self):
		from multiprocessing.dummy import Pool as ThreadPool

		ranges = []

		for idx, resolution in enumerate((self.imageWidth, self.imageHeight)):
			box_len = int(resolution / self.multi)
			resolution_ranges = []
			start = 0
			for x in range(self.multi + 1):
				end = box_len * (x + 1)
				if end >= resolution:
					resolution_ranges.append((x * box_len, self.imageWidth))
				else:
					resolution_ranges.append((start, end))
					start = end

			ranges.append(resolution_ranges)

		# ranges = list(map(lambda y: (ranges[0], y), ranges[1]))
		xy_ranges = []

		for x_ranges in ranges[0]:
			for y_ranges in ranges[1]:
				xy_ranges.append((x_ranges, y_ranges))

		print(ranges)
		print(xy_ranges)

		pool = ThreadPool(processes=len(xy_ranges))

		parts = [x for x in pool.map(self.multiCalc, xy_ranges)]

		# parts =
		# for x, y in ranges:
		# 	print(x, y)

		pool.close()
		pool.join()
		pool.terminate()

		print(parts)

		for part in parts:
			for xy, color in part:
				self.image.putpixel(xy, color)

		return

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
	sphere_pos = Vector(0, 10, 175)
	sphere_pos1 = Vector(20, 5, 175)
	sphere_pos2 = Vector(-20, 5, 175)

	resolution = 300, 200
	aratio = resolution[0] / resolution[1]

	camera = Camera(
			origin=Vector(0, 10, 0),
			up=Vector(0, 1, 0),
			focus=Vector(0, 10, 40),
			fov=120,
			aratio=aratio
	)

	rc = RayCaster(resolution=resolution, camera=camera)
	rc.add(Sphere(sphere_pos, 25, COLORS.WHITE))
	rc.add(Sphere(sphere_pos1, 20, COLORS.BLUE))
	rc.add(Sphere(sphere_pos2, 20, COLORS.BLUE))

	rc.castRays()
	rc.export()
