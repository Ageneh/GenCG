from sys import argv

from open_gl.OBJParser import OBJParser

if __name__ == '__main__':
	if len(argv) < 2:
		fpath = "./objects/cow.obj"
	else:
		fpath = argv[1]

	objparser = OBJParser(fpath)
	objparser.parse()

	print("center: {}".format(objparser.midofobj()))
	print("normal: {}".format(objparser.getobj()[:1]))
	print("normal: {}".format(objparser.getobj_np()[:1]))
	print("scaled: {}".format(objparser.scaletofit()[:1]))
	print("moved: {}".format(objparser.tocenter()[:1]))
	print("VBO: {}".format(objparser.vbo()[:1]))
