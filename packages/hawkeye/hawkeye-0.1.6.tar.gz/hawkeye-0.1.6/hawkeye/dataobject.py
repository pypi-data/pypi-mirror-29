class DataObject:

	def __init__(self, filename, obj):
		import json
		from hawkeye import quick_JSON
		self._filename = filename + ".json"
		if obj == False:
			self._object = quick_JSON(self._filename)
		self._object = obj
		self._lastSave = None
	# 	self._property = []
	# 	self._propertyDict = {}

	# def add_property(self, new_property):
	# 	self._property.append(new_property)
	# 	index = str(len(_property) - 1)
		
	def merge(self, *args):
		for arg in args:
			self._object = {**self._object, **arg}

		return True

	def current(self):
		return self._object

	def open(self):
		with open(self._filename, "r") as file:
			self._object = json.load(file)
		return True

	def save(self):
		with open(self._filename, "w") as file:
			json.dump(self._object, file)
		return True

	def print(self):
		print(json.dumps(data, sort_keys=True, indent=2))