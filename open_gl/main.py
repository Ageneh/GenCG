from sys import argv

from open_gl.OBJParser import OBJParser

if __name__ == '__main__':
	if len(argv) < 2:
		fpath = "./objects/cow.obj"
	else:
		fpath = argv[1]

	objparser = OBJParser(fpath)
	objparser.parse()
