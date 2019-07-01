from numpy import subtract, cross, divide, array, concatenate, median, add, multiply


class OBJParser:

    # DONE
    def __init__(self, fpath):
        self.fpath = fpath
        self._obj = {}
        self._content = {}
        self.bbox = [[None] * 3, [None] * 3]  # [min, max]
        self._vbo = []

    # DONE
    def getobj(self):
        # return faces ob object
        return self._obj

    # DONE
    def getobj_np(self):
        # return faces ob object as np.array
        _obj = []

        for face in self._obj:
            points = []
            for vertex in face:
                v, vt, vn = list(map(array, vertex))
                points.append(array([v, vt, vn]))

            _obj.append(array(points))

        return array(_obj)

    # DONE
    def calcboundingbox(self, vertex):
        # calculate bounding box
        for idx, axis in enumerate(vertex):
            if not self.bbox[1][idx] or axis > self.bbox[1][idx]:
                self.bbox[1][idx] = axis
            if not self.bbox[0][idx] or axis < self.bbox[0][idx]:
                self.bbox[0][idx] = axis

    # DONE
    def parse(self):

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
            self.calcboundingbox(v)
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
        self._content = content

        return self._obj

    # DONE
    def calcmidofobj(self):
        # center = divide(subtract(self.bbox[1], self.bbox[0]), 2)
        # print "subtracted", center
        center = list(map(median, zip(self.bbox[1], self.bbox[0])))
        print "median", center
        self._center = center
        return self._center

    # DONE
    def scaletocanonical(self):
        longest = max(self.bbox[0])

        _scaled = []
        for face in self.getobj():
            _s = []
            for point in face:
                vertex, tex, normal = point
                vertex = multiply(vertex, 2 / abs(longest * 2))
                _s.append([vertex, tex, normal])
            _scaled.append(_s)
        return _scaled

    # DONE
    def scaletofit(self):
        scale_factor = max(self.bbox[:2])
        scaled_points = []

        for face in self._obj:
            scaled_face = []
            for point in face:
                vertex, tex, normal = point
                vertex = list(divide(vertex, scale_factor))
                scaled_face.append([vertex, tex, normal])
            scaled_points.append(scaled_face)

        self._obj = scaled_points

        return scaled_points

    # DONE
    def tocenter(self):
        center = self.calcmidofobj()

        centered = []

        for face in self.getobj():
            _moved = []
            for point in face:
                vertex, tex, normal = point
                vertex = list(subtract(vertex, center))
                _moved.append([vertex, tex, normal])
            centered.append(_moved)

        return centered

    def _calcbbox(self):
        self.bbox = [[None] * 3, [None] * 3]  # [min, max]
        for vertex in self._content["v"]:
            self.calcboundingbox(list(vertex))
        return self.bbox

    # DONE
    def toorigin(self):
        center = self.calcmidofobj()
        self.bbox = [list(subtract(box, center)) for box in self.bbox]
        moveUp = [0, (self.bbox[1][1] - self.bbox[0][1]) / 2, 0]
        centered = []

        for face in self.getobj():
            _moved = []
            for point in face:
                vertex, tex, normal = point
                vertex = list(add(vertex, add(center, moveUp)))
                _moved.append([vertex, tex, normal])
            centered.append(_moved)

        return centered

    # DONE
    def getboundingbox(self):
        return self.bbox

    # DONE
    def vbo(self):
        vbo = []

        self._obj = self.toorigin()
        self._obj = self.scaletocanonical()
        # self._obj = self.tocenter()

        for face in self._obj:
            for v, t, n in face:
                vbo.append(concatenate((v, n), axis=None))
        self._vbo = vbo
        return self._vbo

    # DONE
    @staticmethod
    def _calcnormal(face, vertices):
        mid, v1, v2 = list(map(lambda x: vertices[x[0] - 1], face))
        v1_v2, v1_v3 = subtract(v1, mid), subtract(v2, mid)
        return list(cross(v1_v2, v1_v3))

    # DONE
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
            _calculatedNormal = None

            _assembledentry = []
            for idx, _vertix in enumerate(_face):
                vertexidx, texidx, normalidx = _vertix
                _vertex = vertices[vertexidx - 1] if vertexidx else None
                _texture = textures[texidx - 1] if texidx else None

                if normalidx:
                    _normal = normals[normalidx - 1]
                    _assembledentry.append([_vertex, _texture, _normal])
                else:
                    # calculate normal for vertex by using all three points of face
                    _normal = OBJParser._calcnormal(_face, vertices)
                    _calculatedNormal = _normal
                    # set normal for all three faces
                    break

            if _calculatedNormal:
                for idx, _vertix in enumerate(_face):
                    vertexidx, texidx, normalidx = _vertix
                    _vertex = vertices[vertexidx - 1] if vertexidx else None
                    _texture = textures[texidx - 1] if texidx else None
                    _normal = _calculatedNormal
                    _assembledentry.append([_vertex, _texture, _normal])

            _faces.append(_assembledentry)

        return _faces
