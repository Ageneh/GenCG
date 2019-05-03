import multiprocessing
from datetime import datetime
from multiprocessing import Manager, Process

from PIL import Image

from raytracer.coloring import *
from raytracer.objects import Camera, HitPointData, Light, Plane, Ray, Sphere, Triangle, Vector


class RayTracer:

	# DONE
	def export(self, start, end):
		self.image = Image.new("RGB", (self.resW, self.resH))

		duration = end - start
		time1 = "-".join([str(start.year), str(start.month), str(start.day)])
		time2 = ":".join([str(start.year), str(start.hour), str(start.minute)])
		directory = "../renders/"
		fname = "{}_{}-fov{}-res{}x{}".format(time1, time2, str(self.camera.fov), str(self.resW), str(self.resH))

		# image
		img_fname = directory + fname + ".jpg"

		for xy, color in self.pixels:
			self.image.putpixel(xy, color)

		if self._export:
			from os import path, mkdir
			if not path.isdir(directory):
				mkdir(directory)

			self.image.save(img_fname, "JPEG", quality=99)

			# log
			with open(directory + "render-logs" + ".log", "a+") as file:
				file.write("image: {}".format(img_fname.replace("..", ".")))
				file.write("\n")

				file.write("time: {}".format(duration))
				file.write("\n")

				file.write("resolution: {} x {} px".format(str(self.resW), str(self.resH)))
				file.write("\n")

				file.write("aspect ratio: {}".format(str(self.camera.aratio)))
				file.write("\n")

				file.write("multi: {}".format(str(self.multi)))
				file.write("\n")

				file.write("reflection: {}".format(str(self.reflection)))
				file.write("\n")

				file.write("max depth level: {}".format(str(self.maxlevel)))
				file.write("\n")

				file.write("camera: {}".format(str(self.objects)))
				file.write("\n")

				file.write("light: {}".format(str(self.camera)))
				file.write("\n")

				file.write("objects: {}".format(str(self.objects)))
				file.write("\n\n")
				file.write("# " * 20)
				file.write("\n\n")

		self.image.show("Image")
		return

	# DONE
	def start(self):
		start = datetime.now()

		self.castrays()

		end = datetime.now()
		print("Time needed:", end - start)
		self.export(start, end)

	def castrays(self):
		if not self.multi:
			for x in range(self.resW):
				for y in range(self.resH):
					self.compute(x, y)
			return

		part_width = int(self.resW / self.multi)
		parts = [[part_width * p - part_width, part_width * p - 1] for p in range(1, self.multi + 1)]
		parts[-1][-1] = self.resW - 1

		processes = []
		i = 0

		values_pixels = []
		length = self.resH

		lst = Manager().list()
		for x_start, x_end in parts:
			process = Process(target=self.compute_multi,
							  args=(x_start, x_end, lst),
							  name="render-part-{}".format(i))
			processes.append(process)
			i += 1

		for p in processes: p.start()
		for p in processes:
			p.join()
			p.terminate()

		self.pixels = lst
		return

	# DONE
	def compute_multi(self, x_start, x_end, lst):
		print("> started", multiprocessing.current_process().name)

		for x in range(x_start, x_end + 1):
			for y in range(self.resH):
				lst.append(self.compute(x, y))

		print("> done with", x_start, x_end)
		print(">", multiprocessing.current_process().name, "waiting for rest\n")
		return lst

	# DONE
	def compute(self, x: int, y: int):
		ray = self.calcray(x, y)

		if not self.intersect(1, ray):  # no intersection
			return (x, y), black.items()

		color = self.traceray(1, ray)
		self.pixels.append(((x, y), color.items()))
		return (x, y), color.items()

	# DONE
	def __init__(self, camera: Camera, multi=0, light=None,
				 objects=[], res=(200, 200), maxlevel=5, reflection=1.0, export=False):
		# ShareManager.register('SharedData', self)
		self.pixels = []
		self.camera = camera
		if multi and multi >= 2:
			self.multi = multi
		else:
			self.multi = False
		self.light = light
		self.objects = objects
		self.resW, self.resH = res
		self.pxWidth = self.camera.width / (self.resW - 1)
		self.pxHeigth = self.camera.height / (self.resH - 1)
		self.image = None
		self.maxlevel = maxlevel
		self.reflection = reflection
		self.__mindist = .0001
		self._export = export


	# DONE
	def traceray(self, level: int, ray: Ray):
		hitPointData = self.intersect(level, ray)

		if hitPointData:
			return self.shade(level, hitPointData)
		return black

	# DONE
	def calcray(self, x: int, y: int):
		xcomp = self.camera.s.scale(x * self.pxWidth - self.camera.width / 2)
		ycomp = self.camera.u.scale(y * self.pxHeigth - self.camera.height / 2)
		return Ray(self.camera.origin, self.camera.f + xcomp + ycomp)

	# DONE
	def intersect(self, level: int, ray: Ray):
		if level >= self.maxlevel:  # if not intersection has been found after depth of maxlevel
			return None

		maxdist = float("inf")
		object = None
		for obj in self.objects:
			hitdist = obj.intersectionparameter(ray)
			if not hitdist:
				continue

			# on intersection with obj
			if self.__mindist < hitdist < maxdist:
				maxdist = hitdist
				object = obj

		if not object: return None

		return HitPointData(object=object, ray=ray, distance=maxdist)

	# DONE
	def objectbetween(self, hpd: HitPointData):
		for obj in self.objects:
			if obj == hpd.object:
				continue

			ray_tolight = Ray(hpd.intersection, self.light.origin - hpd.intersection)
			dist = obj.intersectionparameter(ray_tolight)
			if dist and dist > self.__mindist:
				return True
		return False

	# DONE
	def shade(self, level: int, hpd: HitPointData) -> Color:
		directcolor = self.com_directlight(hpd)
		reflectedray = Ray(hpd.intersection, hpd.reflected)
		reflectcolor = self.traceray(level + 1, reflectedray)

		if self.objectbetween(hpd):
			return self.com_shadedcolor(hpd)

		return directcolor + self.reflection * reflectcolor

	# DONE
	def com_shadedcolor(self, hpd: HitPointData):
		intersection = hpd.intersection
		object = hpd.object
		return object.material.calccolor(p=intersection, shaded=True)

	# DONE
	def com_directlight(self, hpd: HitPointData) -> Color:
		ray, object, distance, intersection, normal, reflected = hpd.data()

		tolight = intersection.vectorto(self.light.origin).normalized()
		tolight_r = tolight.reflect(normal).normalized()
		d = ray.direction

		# phi := <l, n>
		phi = tolight.dot(normal)

		# theta := <lr, -d>
		theta = tolight_r.dot(-1 * d)

		return object.material.calccolor(
				phi=phi,
				theta=theta,
				intensity=self.light.intensity,
				p=intersection)


if __name__ == '__main__':
	up = Vector(0, -1, 0)
	fov = 20
	radius = 30
	side = radius + 20
	z = 100
	top = 70
	_res = 500, 500
	plane_y = -(radius + 10)

	focus = Vector(0, 35, z)
	camera = Camera(Vector(0, 45, -75), up, focus, fov, res=_res)
	light = Light(Vector(50, 175, 20), white, intensity=1.0)

	sp0 = Sphere(Vector(side, 0, z), radius, green_mat)
	sp1 = Sphere(Vector(0, top, z), radius, blue_mat)
	sp2 = Sphere(Vector(-side, 0, z), radius, red_mat)

	objects = [
		sp0, sp1, sp2,
		Plane(Vector(0, -40, 0), up * -1, checkerboard_tex.setsize(15)),
		Triangle(sp0.center, sp1.center, sp2.center, material=yellow_mat),
	]

	rt = RayTracer(
			camera=camera,
			light=light,
			objects=objects,
			res=_res,
			reflection=0.2,
			maxlevel=4,
			multi=0,
			export=True
	)

	rt.start()
