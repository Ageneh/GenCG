from multiprocessing.pool import ThreadPool

from raytracer.objects import Camera, Ray, Vector
from raytracer.raycaster import RayCaster

if __name__ == '__main__':
	ray = Ray(Vector(0, 1, 2), Vector(0, 1, 6))
	print(ray, "-", ray.pointAtParameter(1), "-", ray.pointAtParameter(2))

	sphere_pos = Vector(0, 20, 550)
	camera = Camera(
			origin=Vector(0, 20, -200),
			up=Vector(0, 1, 0),
			focus=sphere_pos,
			fov=45,
			aratio=10 / 16
	)

	thread = ThreadPool(processes=1)

	rc = RayCaster(camera=camera)
	rc.__add__()

	rc.castRays()
	rc.export()
