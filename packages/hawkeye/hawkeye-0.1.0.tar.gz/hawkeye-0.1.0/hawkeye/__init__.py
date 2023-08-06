import json
from time import strftime

"""
list2str
	Usage: Converts a python list to a string.
	- Ensures list values are of string type.
	- List values are seperated exactly by 'delimiter'.
		-- No spaces are automatically added.

Future modifications: 
	- Make delimiter optional arguement, seperate by single space if not present.
"""

def data2csv(data, filename):
	import csv
	with open(filename, "w") as csvfile:
		_write = csv.writer(csvfile, lineterminator="\n")
		for key in data.keys():
			_write.writerow([key, data[key]])

def key2List(data, return_type):
	key_list = []
	for key in data.keys():
		key_list.append(key)

	if return_type == "p":
		return print(key_list)
	else:
		return key_list

def printKey(data):
	count = 1
	for key in data.keys():
		print(str(count) + "\t" + key)
		count += 1

def indexKeyList(key_list):
	indexed_key_list = []
	for i,v in enumerate(key_list):
		indexed_key_list.append((i, v))

	return indexed_key_list

def tupleKeyData(data):
	key_list = key2List(data, return_type="")
	return_list = []
	for key in key_list:
		return_list.append((key, data[key]))

	return return_list

def list2str(pylist, delimiter):
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

def openData(filename):
	with open(filename, "r") as file:
		dic = json.load(file)
	return dic

def saveData(dictionary, filename):
	with open(filename, "w") as file:
		json.dump(dictionary, file)
		file.close()
	return True

def checkSave(saveDic_return):
	if saveDic_return == True:
		print("Changes saved.")
	else:
		print("A problem was encountered in the save process.")

def printData(dictionary):
	print(json.dumps(dictionary, sort_keys=True, indent=2))

def initDate(dic):
	date = strftime("%m-%d-%y")
	time = strftime("%H:%M:%S")
	if date not in dic["init-date"]:
		for cat in dic.keys():
			dic[cat][date] = {time: "Daily initialization."}
		print("Daily initialization complete.")
	return dic
	
def str2charList(string):
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

def listFromData(charset):
	pylist = []
	for key in charset.keys():
		temp = charset[key]
		for char in temp:
			pylist.append(char)

	return pylist

# def updateData(datafile)

def GetDataFromURL(url):

	import requests
	import json

	request = requests.get(url)
	data = json.loads(request.text)

	return data

def INIT_DataObject(filename):
	dataObject = {
		"properties": {
			"initialized": {
				"date": strftime("%Y-%m-%d"),
				"time": strftime("%H:%M:%S")
			}
		}
	}

	save_file = saveData(dataObject, filename)
	check_save = checkSave(save_file)

	return dataObject

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

def AVGetData(function, symbol, interval, output_size, data_type):
	# interval, options: 1min | 5min | 15min | 30min | 60min
	# *args[0] = output_size, options: compact (default) | full
	# *args[1] = data_type, options: json (default) | csv
	function = "function=" + function
	symbol = "&symbol=" + symbol
	interval = "&interval=" + interval
	output_size = "&outputsize=" + output_size
	data_type = "&datatype=" + data_type

	base_url = "https://www.alphavantage.co/query?"
	apikey = "&apikey=3DZ3HMSX2HRWQDXM"
	query = base_url + function + symbol + interval + output_size + data_type + apikey
	rawdata = GetDataFromURL(query)

	return rawdata

def AVGetDataDaily(function, symbol, output_size, data_type):
	# interval, options: 1min | 5min | 15min | 30min | 60min
	# *args[0] = output_size, options: compact (default) | full
	# *args[1] = data_type, options: json (default) | csv
	function = "function=" + function
	symbol = "&symbol=" + symbol
	output_size = "&outputsize=" + output_size
	data_type = "&datatype=" + data_type

	base_url = "https://www.alphavantage.co/query?"
	apikey = "&apikey=3DZ3HMSX2HRWQDXM"
	query = base_url + function + symbol + output_size + data_type + apikey
	rawdata = GetDataFromURL(query)

	return rawdata

"""
features to add:
- alert for currently watched stocks
- report 2min, 5min differences

"""

def AVGetSMA(function, symbol, interval, time_period, series_type):
	function = "function=" + function
	symbol = "&symbol=" + symbol
	interval = "&interval=" + interval
	time_period = "&time_period=" + time_period
	series_type = "&series_type=" + series_type

	base_url = "https://www.alphavantage.co/query?"
	apikey = "&apikey=3DZ3HMSX2HRWQDXM"
	query = base_url + function + symbol + interval + time_period + series_type + apikey
	data = GetDataFromURL(query)

	return data

# def AlphaVantageGetCurrentValue(propertiesDict):

def AVData2Eagle(filename):
	#Generate report each couple of minutes, make callabl
	rawdata_location = filename + ".txt"
	rawdata = openData(rawdata_location)
	eagle_filename = init_DataObject(filename + ".el")
	data = openData(eagle_filename)

	key_list = []
	key_list = key2List(rawdata, return_type = "")

	# key-text: Meta Data
	meta = rawdata[key_list[0]]
	# key-text: Technical Analysis: SMA
	data = rawdata[key_list[1]]

	# parents: (0, meta), (1, data)
	key_list = []
	datetime = []
	for key in data.keys():
		datetime.append(key)
		key = key.split(" ")
		date = key[0]
		if date not in date_array:
			date_array.append(date)

	for date in date_array:
		amd[date] = {}
		for key in data.keys():
			_key = key.split(" ")
			if _key[0] == date:
				data[date][_key[1]] = data[key]
	"""
	date array:
	values: '2018-02-26', '2018-02-23', ..., '2018-02-12'

	print(date_array) """

	_save = saveData(data, eagle_filename)
	return data

def GetCurrentLocation():
	"""
	output: database
	"""
	import requests
	import json

	url = 'http://freegeoip.net/json'
	request = requests.get(url)
	data = json.loads(request.text)

	return data

def NOAAGetCurrent(latitude, longitude, query_key):
	import requests
	import json

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

	url = base_url + query[query_key]
	request = requests.get(url)
	data = json.loads(request.text)

	return data