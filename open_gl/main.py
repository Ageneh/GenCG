from sys import argv

from open_gl.OBJParser import OBJParser
from open_gl.RenderWindow import RenderWindow

if __name__ == '__main__':
    fpath = argv[1] if len(argv) > 2 else "./objects/cow.obj"
    fpath = argv[1] if len(argv) > 2 else "./objects/squirrel.obj"

    objparser = OBJParser(fpath)
    objparser.parse()

    rw = RenderWindow()
    rw.run(objparser.vbo())
