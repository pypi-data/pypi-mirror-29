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