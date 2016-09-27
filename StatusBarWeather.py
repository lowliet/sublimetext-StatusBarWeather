#
#    Made by lowliet
#    https://github.com/lowliet
#

from datetime import datetime
import xml.etree.ElementTree as et

import sublime, sublime_plugin
import urllib.request, urllib.error, urllib.parse

class StatusBarWeather(sublime_plugin.EventListener):
	def on_activated(self, view):
		self.display_weather(view)

	def load_settings(self):
		settings = sublime.load_settings('StatusBarWeather.sublime-settings')
		self._code = settings.get('code', 'UKXX0085').upper()
		self._unit = settings.get('unit', 'c').lower()
		self._format = settings.get('format', "[City], [Text], [Temp] Celcius")
		if self._unit != 'c' and self._unit != 'f': self._unit = 'c'
		self._debug = settings.get('debug', False)
		if self._debug: print("StatusBarWeather | Settings: {0}, {1}, {2} | {3}".format(self._code, self._unit, self._debug, self.time()))

	def fetch_weather(self):
		if hasattr(self, '_debug') and self._debug: print("StatusBarWeather | Fetching weather data | {0}".format(self.time()))
		if not hasattr(self, '_code') or not hasattr(self, '_unit') or not hasattr(self, '_format'):
			print("StatusBarWeather | Settings not loaded, reload plugin | {0}".format(self.time()))
		else:
			self._data = Weather(self._code, self._unit).get_weather()

	def display_weather(self, view, async = True):
		self.load_settings()
		if not hasattr(self, '_data') and async: self.fetch_weather()
		if hasattr(self, '_data') and sublime.active_window():
			sublime.active_window().active_view().set_status(self._STATUS_KEY, self.format_data(self._data, self._format))

	def time(self):
		return datetime.now().strftime('%H:%M:%S')

	def format_data(self, data, format):
		""" Returns weather data as formated string """
		for key, data in data.items():
			format = format.replace('[' + key + ']', data)
		if len(data) == 0:
			print("StatusBarWeather | Cannot fetch weather, check settings")
			format = ""
		return format

	_STATUS_KEY = "z_statusweather"

class Weather():
	""" Class providing weather service """
	def __init__(self, code, unit):
		""" Constructor """
		# self._url = "http://weather.yahooapis.com/forecastrss?p={0}&u={1}".format(code, unit)
		self._url = "https://query.yahooapis.com/v1/public/yql?format=xml&q=SELECT%20*%20FROM%20weather.forecast%20WHERE%20u=%27{1}%27%20AND%20woeid%20=%20%27{0}%27".format(code, unit)

	def _get_node(self, root, name, node = ''):
		""" Retrieves node """
		# return root.find(('channel/' + node + '{%s}' + name) % "http://xml.weather.yahoo.com/ns/rss/1.0")
		return root.find(('results/channel/' + node + '{%s}' + name) % "http://xml.weather.yahoo.com/ns/rss/1.0")

	def get_weather(self):
		""" Returns weather information in dictionary """
		data = { }
		try:
			root = et.fromstring(urllib.request.urlopen(self._url).read())
			weather_data = self._get_node(root, "condition", "item/")
			if weather_data is not None:
				data["Temp"] = weather_data.get('temp')
				data["Text"] = weather_data.get('text')
			weather_data = self._get_node(root, "location")
			if weather_data is not None:
				data["City"] = weather_data.get('city')
				data["Country"] = weather_data.get('country')
			weather_data = self._get_node(root, "units")
			if weather_data is not None:
				if weather_data.get('temperature') == "C": data["Unit"] = u'\N{DEGREE SIGN}C';
				else: data["Unit"] = "F";
			weather_data = self._get_node(root, "astronomy")
			if weather_data is not None:
				data["Sunrise"] = weather_data.get('sunrise')
				data["Sunset"] = weather_data.get('sunset')
			weather_data = self._get_node(root, "atmosphere")
			if weather_data is not None:
				data["Pressure"] = weather_data.get('pressure')
				data["Humidity"] = weather_data.get('humidity')
		except Exception as e:
			pass
		return data