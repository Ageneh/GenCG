from numpy import subtract, cross


class OBJParser:

    def __init__(self, fpath):
        self.fpath = fpath
        self._obj = {}

    def getobj(self):
        return self._obj

    def parse(self):
        obj = None

        def calcnormal():
            return

        def face(comp):
            # face line := v/vt/n;
            # if not texture: v//n
            # if not normal: v
            full_face = []

            for group in comp[1:]:
                tex = None
                vertex = None
                normal = None

                data = group.split("/")

                if "//" in group:
                    # not texture given
                    vertex = int(data[0])
                    normal = int(data[2])
                elif len(data) == 1:
                    # only vertex given
                    vertex = int(data[0])
                else:
                    vertex = int(data[0])
                    tex = int(data[1])
                    normal = int(data[2])

                full_face.append([vertex, tex, normal])

            return full_face

        def vertex(comp):
            """Return a list which defines a vertex."""
            v = list(map(float, comp[1:]))
            return v

        def vertexnormal(comp):
            """Return a list which defines a vertex."""
            vn = list(map(float, comp[1:]))
            return vn

        def vertextex(comp):
            return "Texture"

        # Vertex v
        # Tex vt,
        # Normale vn
        # Face f

        types = {
            "v": vertex,
            "vt": vertex,
            "vn": vertexnormal,
            "f": face,
        }

        content = {
            "v": [],
            "vt": [],
            "vn": [],
            "f": [],
        }

        with open(self.fpath) as file:
            for line in file:
                comp = line.split()
                if not comp or comp[0] not in types: continue

                res = types[comp[0]](comp)
                content[comp[0]].append(res)

        self._obj = OBJParser._assemblefaces(content)

        return self._obj

    @staticmethod
    def _calcnormal(face, vertices):
        mid, v1, v2 = list(map(lambda x: vertices[x[0] - 1], face))

        v1_v2, v1_v3 = subtract(v1, mid), subtract(v2, mid)

        return list(cross(v1_v2, v1_v3))

    @staticmethod
    def _assemblefaces(content):
        # fill faces with normals if they miss any

        _faces = []

        faces = content["f"]
        vertices = content["v"]
        textures = content["vt"]
        normals = content["vn"]

        for idx, _face in enumerate(faces):
            # for each unfinished face
            # get all the referenced values and add to face

            points = [x[0] for x in _face]

            _calculatedNormal = None

            _assembledentry = []
            for idx, _vertix in enumerate(_face):
                vertexidx, texidx, normalidx = _vertix
                _vertex = vertices[vertexidx - 1] if vertexidx else None
                _texture = textures[texidx - 1] if texidx else None

                if normalidx:
                    _normal = normals[normalidx - 1]
                elif _calculatedNormal:
                    _normal = _calculatedNormal
                else:
                    # calculate normal for vertex by using all three points of face
                    _normal = OBJParser._calcnormal(_face, vertices)
                    _calculatedNormal = _normal

                _assembledentry.append([_vertex, _texture, _normal])

            _faces.append(_assembledentry)

        return _faces
