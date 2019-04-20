import datetime
import random

from PIL import Image

from raytracer.objects import COLORS, Ray, Vector


class RayCaster:

	# TODO: implement illumination

	# TODO: implement transformation

	# TODO: implement recursive ray-casting

	# TODO: implement reflections

	# TODO: textures

	def __init__(self, wRes, hRes, camera, objects):
		'''
		:param wRes: width of the output image
		:param hRes: height of the output image
		:param camera: the scene camera
		:param objects: a collection of all object of the scene
		'''
		self.objects = objects
		self.imageWidth = wRes
		self.imageHeight = hRes
		self.image = Image.new("RGB", (self.imageWidth, self.imageHeight))
		self.camera = camera

		self.times = []

		self.pixelWidth = self.camera.width / (self.imageWidth - 1)
		self.pixelHeight = self.camera.height / (self.imageHeight - 1)
		pass

	def calcRay(self, x, y):
		# TODO: implement ray calculation based on pixel

		s = self.camera.s
		u = self.camera.u  # up
		e = self.camera.position  # eye
		f = self.camera.f  # focus

		xcomp = s.scale(x * self.pixelWidth - self.imageWidth / 2)
		ycomp = u.scale(y * self.pixelHeight - self.imageHeight / 2)
		# ray = Ray(e, f + xcomp + ycomp)  # evtl . mehrere Strahlen pro Pixel
		return self.rays(e, f, xcomp, ycomp)  # evtl . mehrere Strahlen pro Pixel

	def rays(self, e, f, xcomp, ycomp, raycount=1):
		if raycount == 1:
			return Ray(e, f + xcomp + ycomp)

		# TODO: multiple rays per pixel

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
		return avg_ray

	# TODO: multiprocessed rayscasting

	def castRays(self):
		start = datetime.datetime.now()
		print("Casting start: {}".format(start))

		for x in range(self.imageWidth):
			for y in range(self.imageHeight):
				ray = self.calcRay(x, y)
				maxdist = float("inf")
				color = COLORS.BG_COLOR

				for object in self.objects:
					hitdist = object.intersectionParameter(ray)
					if hitdist != 0:
						if hitdist < maxdist:
							maxdist = hitdist
							color = object.colorAt(ray)
					else:
						print("NO", color.value())

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
