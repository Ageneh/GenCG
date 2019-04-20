import random

from raytracer.objects import Vector

print(random.uniform(0.05, 0.1))

avg = Vector(0, 0, 0)
rays = [Vector(1, 1, 1) for r in range(3)]

for v in rays:
	avg = avg + v

print(rays, avg, avg / 3)
