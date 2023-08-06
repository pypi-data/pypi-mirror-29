"""
FUNCTIONS
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

