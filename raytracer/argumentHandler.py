import re

from raytracer.objects import Color

class ArgsHandler:

	def __init__(self, argv):
		if ".py" in argv[0]:
			self.argv = argv[1:]
		else:
			self.argv = argv

		if len(self.argv) > 0:
			self._argvFormatted = self._formatArgv()
		else:
			self._argvFormatted = {}

	def _formatArgv(self):
		# pattern_int = "^-(\w+)=([0-9]+)"
		# pattern_int_int = "^-(\w+)=([0-9]+),([0-9]+)"
		# pattern_flag = "^-(\w+)(\n)?$"
		# pattern_list = "^-(\w+)=\[(([0-9]+),){2}([0-9]+)\]"
		# pattern_str = "^-(\w+)=(\w+)"
		#
		# lst = [
		# 	pattern_int,
		# 	pattern_int_int,
		# 	pattern_flag,
		# 	pattern_list,
		# 	pattern_str,
		# ]
		#
		# concatted = "|".join(list(map(lambda x: "{}".format(x), lst)))

		concatted = "-(\w+)[=]?(.*)?"

		args = {}

		for line in self.argv:
			res = re.match(concatted, line)
			key_value = list(filter(lambda x: x is not None, res.groups()))

			if len(key_value) <= 0: continue

			if len(key_value) < 2:
				key_value.append(True)

			k, v = key_value
			args[k] = v

		print(args)

		return args

	def getRes(self) -> list:
		ret = self._argvFormatted.get("res", None)

		if ret:
			return list(map(int, ret.split(",")))
		return [400, 400]

	def getQuality(self) -> int:
		ret = self._argvFormatted.get("quality", 75)
		return int(ret)

	def getFType(self) -> str:
		ret = self._argvFormatted.get("ftype", None)
		return ret

	def getDirOut(self) -> str:
		ret = self._argvFormatted.get("dirout", None)
		return ret

	def getProcesses(self):
		max = 25
		ret = self._argvFormatted.get("processes", 4)

		if ret > max: return max
		return int(ret)

	def isShow(self) -> bool:
		return "noshow" in self._argvFormatted.keys()

	def isExport(self) -> bool:
		return "export" in self._argvFormatted.keys()

	def getReflection(self) -> float:
		ret = self._argvFormatted.get("reflection", 0.3)
		return float(ret)

	def getRecursiveDepth(self) -> int:
		ret = self._argvFormatted.get("rdepth", 3)
		return int(ret)

	def getLightIntensity(self) -> float:
		ret = self._argvFormatted.get("lightintensity", 1)
		return float(ret)

	def getMulti(self) -> int:
		ret = self._argvFormatted.get("multi", 4)
		return int(ret)

	def getLightPos(self) -> list:
		ret = self._argvFormatted.get("lightpos", None)
		if ret:
			return eval(ret)
		return [50, 175, 20]

	def getLightColor(self) -> Color:
		ret = self._argvFormatted.get("lightcolor", None)
		if ret:
			return Color(eval(ret))
		return Color(r=Color._MAX, g=Color._MAX, b=Color._MAX)

	def getFloorMaterial(self):
		ret = self._argvFormatted.get("floormat", "")
		return ret

	def getSphereColors(self):
		from raytracer.coloring import materialsContainer
		from random import randint
		ret = self._argvFormatted.get("spherecolors", None)

		keys = list(materialsContainer.keys())
		get_random = lambda idx: materialsContainer[keys[idx]]

		if ret:
			ret_str = ret.replace(",", "\",\"").replace("\"\"", "\"\"").replace("(", "(\"").replace(")", "\")")

			ret_lst = list(eval(ret_str))
			for idx, colName in enumerate(ret_lst):
				length = len(materialsContainer.keys())
				random_idx = randint(0, length * randint(1, length)) % length
				if colName is "":
					ret_lst[idx] = keys[random_idx]

			ret_lst = [materialsContainer[col] for col in ret_lst]
			return ret_lst

		return [
			materialsContainer["red"],
			materialsContainer["blue"],
			materialsContainer["green"]
		]

	def __getitem__(self, item):
		return self._argvFormatted.get(item, None)
