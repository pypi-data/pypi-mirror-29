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