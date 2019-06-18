from sys import argv

from open_gl.OBJParser import OBJParser
from open_gl.RenderWindow import RenderWindow

FAIL = '\033[91m'
ENDC = '\033[0m'


def err():
    print FAIL + "\nNo object found!\nPlease pass filepath of obj-file as argument.\n" + ENDC
    exit(1)


if __name__ == '__main__':
    fpath = argv[1] if len(argv) > 2 else err()

    objparser = OBJParser(fpath)
    objparser.parse()

    rw = RenderWindow()
    rw.run(objparser.vbo())
