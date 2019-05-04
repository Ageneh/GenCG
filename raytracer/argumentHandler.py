import re

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

	def getRes(self):
		ret = self._argvFormatted.get("res", None)

		if ret:
			return list(map(int, ret.split(",")))
		return [400, 400]

	def getQuality(self):
		ret = self._argvFormatted.get("quality", 75)
		return int(ret)

	def getDirOut(self):
		ret = self._argvFormatted.get("dirout", None)
		return ret

	def getMulti(self):
		ret = self._argvFormatted.get("multi", 4)
		return int(ret)

	def getReflection(self):
		ret = self._argvFormatted.get("reflection", 0.3)
		return float(ret)

	def getProcesses(self):
		ret = self._argvFormatted.get("processes", 4)
		return int(ret)

	def getRecursiveDepth(self):
		ret = self._argvFormatted.get("rdepth", 3)
		return int(ret)

	def getLightIntensity(self):
		ret = self._argvFormatted.get("lightintensity", 1)
		return float(ret)

	def getFloorMaterial(self):
		ret = self._argvFormatted.get("floormat", "")
		return ret

	def isShow(self):
		return "noshow" in self._argvFormatted.keys()

	def isExport(self):
		return "export" in self._argvFormatted.keys()

	def __getitem__(self, item):
		return self._argvFormatted.get(item, None)
