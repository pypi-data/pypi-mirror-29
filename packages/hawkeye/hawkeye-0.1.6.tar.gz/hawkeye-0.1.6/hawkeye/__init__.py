from time import strftime

__author__ = "Todd Jarolimek II"
__version__ = "0.1.6"

# from .functions import *
# from .location import *
# from .weather import *
# from .dataobject import *
"""
.1 Data Object
"""
class DataObject:

	def __init__(self, filename, obj):
		import json
		self._filename = filename
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

"""
2. Location
"""
class Location:

	def __init__(self):
		self._url = "http://freegeoip.net/json"

	def get_current_location(self):
		"""
		output: database
		"""
		from hawkeye import get_data

		data = get_data(self._url)
		# returns: {}
		return data

"""
3. Weather
"""
class NOAA:

	def __init__(self, latitude, longitude, query):
		self._latitude = latitude
		self._longitude = longitude
		self._query = query

	def get_current(self):
		from hawkeye import get_data

		base_url = 'http://api.weather.gov'

		# Metadata query
		query = {}
		query["metadata"] = "/points/" + str(latitude)+ "," + str(longitude)
		query["forecast"] = {}
		query["forecast"]["current"] = query["metadata"] + "/forecast"
		query["forecast"]["hourly"] = query["forecast"]["current"] + "/hourly"
		query["stations"] = query["metadata"] + "/stations"
		query["kmco"] = "/stations/kmco/observations/current"
		query["kmlb"] = "/stations/kmlb/observations/current"
		query["zone-alerts"] = "/alerts/active/zone/FLZ045"
		query["area-alerts"] = "/alerts/active/area/FL"
		query["test"] = "/alerts/active/zone/OHC001"
		query["all-alerts"] = "/alerts/active/count"

		# My zone: FLZ045

		url = base_url + query
		data = get_data(url)

		return data

"""
4. FUNCTIONS
"""

#1
def data_to_csv(data_series, filename):
	import csv
	with open(filename, "w") as csvfile:
		_write = csv.writer(csvfile, lineterminator="\n")
		for key in data_series.keys():
			_write.writerow([key, data_series[key]])
#2
def index_keys(data_series):
	for index, key in enumerate(list(data_series.keys())):
		print(str(index) + "\t" + key)
#3
def index_key_list(key_list):
	indexed_key_list = []
	for i,v in enumerate(key_list):
		indexed_key_list.append((i, v))

	return indexed_key_list
#4
def tuple_key_data(data_series):
	return_list = []
	for key in enumerate(list(data_series.keys())):
		return_list.append((key, data_series[key]))

	return return_list
#5
def list_to_str(pylist, delimiter):
	pylist_str = ""
	for i in range(len(pylist)):
		if type(i) != type("str"):
			pylist[i] = str(pylist[i])
		if i == (len(pylist) - 1):
			pylist_str += pylist[i]
		else:
			pylist_str += pylist[i]
			pylist_str += delimiter
	return pylist_str
#6
def string_to_char_list(string):
	def main(string):
		index = 0
		char_list = []
		for char in string:
			char_list += char

		return char_list

	if type(string) == type([]):
		string_array = string
		return_array = []
		for string in string_array:
			return_array.append(main(string))
		return return_array
	else:
		return main(string)
#7
def list_from_data(charset):
	pylist = []
	for key in charset.keys():
		temp = charset[key]
		for char in temp:
			pylist.append(char)

	return pylist

def std_datetime():
	from time import strftime
	return strftime("%Y-%m-%d %H:%M:%S")

def quick_JSON(filename):
	import json
	json_object = {"quick-init": std_datetime()}
	
	return json_object

def get_data(url):

	import requests
	import json

	request = requests.get(url)
	data = json.loads(request.text)

	return data

def navigate(data):
	while(True):
		try:
			key_list = list(data.keys())
			for i,v in enumerate(key_list):
				print(str(i) + "\t" + str(v))
			conin = input(">>>")
			data = data[key_list[int(conin)]]
		except:
			print("That's the end of the tree.")
			break









