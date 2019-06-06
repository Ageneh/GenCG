class OBJParser:

	def __init__(self, fpath):
		self.fpath = fpath

	def getobj(self):
		pass

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
	def _calcnormal(v, vertices):
		return v

	@staticmethod
	def _assemblefaces(content):
		faces = []

		faces = content["f"]
		vertices = content["v"]
		textures = content["vt"]
		normals = content["vn"]

		for entry in faces:
			# for each unfinished face
			# get all the referenced values and add to face

			_assembledentry = []

			for _face in entry:
				vertexidx, texidx, normalidx = _face

				_vertex = vertices[vertexidx - 1] if vertexidx else None
				_texture = textures[texidx - 1] if texidx else None
				_normal = normals[normalidx - 1] if normalidx else OBJParser._calcnormal(None, None)

				_assembledentry.append([_vertex, _texture, _normal])
		return faces
