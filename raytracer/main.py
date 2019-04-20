from multiprocessing.pool import ThreadPool

from raytracer.objects import Camera, Ray, Sphere, Vector
from raytracer.raycaster import COLORS, RayCaster

if __name__ == '__main__':
	ray = Ray(Vector(0, 1, 2), Vector(0, 1, 6))
	print(ray, "-", ray.pointAtParameter(1), "-", ray.pointAtParameter(2))

	wRes = hRes = 200

	c_pos = Vector(0, 20, -100)  # camera position
	focus = Vector(0, 0, 250)
	up = Vector(0, 1, 0)
	fov = 30
	height_mm = 140
	ratio = 10 / 16
	camera = Camera(c_pos, up, focus, fov, height_mm, ratio)

	sphere_pos = Vector(0, 20, 550)

	objects = [
		Sphere(sphere_pos, 30, color=COLORS.BLUE)
	]

	thread = ThreadPool(processes=1)

	rc = RayCaster(wRes, hRes, camera, objects)

	rc.castRays()
	rc.export()
