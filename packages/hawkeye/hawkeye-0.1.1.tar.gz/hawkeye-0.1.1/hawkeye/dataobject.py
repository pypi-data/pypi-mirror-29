class DataObject:

	def __init__(self, filename, obj):
		import json
		self._filename = filename
		self._object = obj
		self._lastSave = None

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