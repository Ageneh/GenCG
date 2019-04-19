from raytracer.objects import Camera, Point, Sphere

objects = []

p1 = Point(3, 2, 1)
p2 = Point(3, 1, 1)
camera = Camera(p1, 120, 1280, 10 / 16)

p3 = p1 + p2

circle1 = Sphere(p1, 30)

# print(p1, p2)
# print(p1 + p2)
# print(p1 * p2)
# print(p1 * 2)
print(p3, p3.normalized())
print(p2.length())
print(circle1, circle1.normalAt(p1 * 4))
