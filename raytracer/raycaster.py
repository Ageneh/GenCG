from raytracer.objects import Ray


class COLORS:
	class Color:

		def __init__(self, r=0, g=0, b=0):
			self.rgb = r, g, b

		def __repr__(self):
			return "Color({})".format(",".join(map(repr, self.rgb)))

	BLACK = Color()
	BG_COLOR = BLACK
	RED = Color(r=255)
	GREEN = Color(g=255)
	BLUE = Color(b=255)


class RayCaster:

	# TODO: add image lib

	# TODO: implement illumination

	# TODO: implement transformation

	# TODO: implement recursive ray-casting

	# TODO: implement reflections

	# TODO: textures

	def __init__(self, camera, objects):
		self.objects = objects
		self.imageWidth = camera.width
		self.imageHeight = camera.height
		self.image = None
		pass

	def calcRay(self, x, y) -> Ray:
		# TODO: implement ray calculation based on pixel
		return Ray(None, None)

	def castRays(self):
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

				self.image.putpixel((x, y), color)

		pass
